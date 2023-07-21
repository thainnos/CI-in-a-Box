import argparse
import base64
import subprocess
import xml.etree.ElementTree as ET

from typing import Tuple

import xml_helpers

import ca


def change_setting_private_network_to_wan(root: ET.Element, block: bool) -> bool:
    """
    Allows/Denys private networks to connect to wan.

    Args:
        root (ET.Element): The xml root of a opnsense config file.
        block (bool): The action to take.

    Returns:
        bool: The change status
    """
    wan = root.find("./interfaces/wan")
    private = wan.find("./blockpriv")

    if private is not None and not block:
        # Allow traffic from private networks to wan
        wan.remove(private)
        return True

    if private is None and block:
        # Block traffic from private networks to wan
        xml_elem = ET.Element("blockpriv")
        xml_elem.text = 1
        wan.insert(7, xml_elem)
        return True

    return False


def xml_elem(root: ET.Element, disable: bool) -> bool:
    """Disables the reply_to directive for all wan interfaces.

    Doing this breaks Multi-Wan Setups, but a Multi-Wan setup
    is not in scope for the CIinaBox Automation.

    Args:
        root (ET.Element): The root element of an opnsense config.
        disable (bool): Disable the reply_to directive.

    Returns:
        bool: The change status.
    """
    system = root.find("./system")

    disable_reply_element_names = [
        "disablereplyto",
        "maximumstates",
        "maximumfrags",
        "aliasesresolveinterval",
        "maximumtableentries",
    ]

    changed = False

    for elem_name in disable_reply_element_names:
        xml_elem = system.find(f"./{elem_name}")

        if disable and xml_elem is None:
            # Create elem_name
            xml_elem = ET.SubElement(system, elem_name)
            if elem_name == "disablereplyto":
                xml_elem.text = "yes"
            changed = True

        elif disable and elem_name == "disablereplyto" and xml_elem.text is None:
            # Create disablereplyto element.
            xml_elem = ET.SubElement(system, elem_name)
            xml_elem.text = "yes"
            changed = True

        elif not disable and xml_elem is not None:
            # Remove the xml element.
            system.remove(xml_elem)
            changed = True

    return changed


def create_user_client_certificates(root: ET.Element) -> bool:
    """Creates ssl client certificates for all users in root.

    Args:
        root (ET.Element): The root of an opnsense config file.

    Returns:
        bool: The change status.
    """
    user_list = root.findall("./system/user")
    ciinabox_ca, _ = ca.CertificateAuthorityBuilder().from_xml_root(root)

    original_length = len(ciinabox_ca.certs)

    for user in user_list:
        name = user.find("name").text
        description = f"CIinaBox VPN Cert - {name}"

        cert_elem = user.find("cert")
        user_has_cert = cert_elem is not None
        if user_has_cert:
            if cert_elem.text is None:
                # remove empty cert element.
                user.remove(cert_elem)
                user_has_cert = False

        # Create a cert if it doesn't exist.
        if not user_has_cert:
            # Generate a signed certificate and add it to the user.
            cert_index = ciinabox_ca.generate_cert(
                subject=f"/emailAddress={name}@ciinabox.demo/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN={name}",
                comment=description,
                url=None,
                ip_addresses=None,
                server_cert=False,
            )
            refid = ciinabox_ca.certs[cert_index].refid
            cert = ET.SubElement(user, "cert")
            cert.text = refid

    if original_length != len(ciinabox_ca.certs):
        # At least one certificate was added.
        ciinabox_ca.add_to_xml_root(root)
        return True
    return False


def create_openvpn_interface(root: ET.Element) -> bool:
    """Creates an openvpn interface.

    Args:
        root (ET.Element): The root of an opnsense config file.

    Returns:
        bool: The change status.
    """
    openvpn_interface = ET.fromstring(
        """
        <openvpn>
            <internal_dynamic>1</internal_dynamic>
            <enable>1</enable>
            <if>openvpn</if>
            <descr>OpenVPN</descr>
            <type>group</type>
            <virtual>1</virtual>
        </openvpn>
        """
    )
    xml_interfaces = root.find("interfaces")
    current_openvpn_interface = xml_interfaces.find("openvpn")

    if current_openvpn_interface is None:
        xml_interfaces.append(openvpn_interface)
        return True

    xml_helpers.indent(current_openvpn_interface)
    xml_helpers.indent(openvpn_interface)

    if ET.tostring(current_openvpn_interface) != ET.tostring(openvpn_interface):
        xml_interfaces.append(openvpn_interface)
        return True
    return False


def create_openvpn_firewall_rules(root: ET.Element) -> bool:
    """Creates the firewall rules for openvpn.

    Args:
        root (ET.Element): The root of an opnsense config file.

    Returns:
        bool: The change status.
    """
    openvpn_wan_rule = ET.fromstring(
        """
        <rule>
            <descr>OpenVPN CIinaBox VPN allow client access</descr>
            <direction>in</direction>
            <source>
                <any>1</any>
            </source>
            <destination>
                <network>wanip</network>
                <port>1194</port>
            </destination>
            <interface>wan</interface>
            <protocol>udp</protocol>
            <ipprotocol>inet46</ipprotocol>
            <type>pass</type>
            <enabled>on</enabled>
            <created>
                <username>root@172.16.3.5</username>
                <time>1668782935.994</time>
                <description>/wizard.php made changes</description>
            </created>
        </rule>
        """
    )
    openvpn_internal_rule = ET.fromstring(
        """
        <rule>
            <descr>OpenVPN CIinaBox VPN</descr>
            <source>
                <any>1</any>
            </source>
            <destination>
                <any>1</any>
            </destination>
            <interface>openvpn</interface>
            <type>pass</type>
            <enabled>on</enabled>
            <created>
                <username>root@172.16.3.5</username>
                <time>1668782935.994</time>
                <description>/wizard.php made changes</description>
            </created>
        </rule>
        """
    )
    xml_filter = root.find("filter")
    current_firewall_rules = xml_filter.findall("rule")
    changed = False

    current_wan_rule = list(
        filter(
            lambda rule: rule.find("descr").text
            == "OpenVPN CIinaBox VPN allow client access",
            current_firewall_rules,
        )
    )
    current_internal_rule = list(
        filter(
            lambda rule: rule.find("descr").text == "OpenVPN CIinaBox VPN",
            current_firewall_rules,
        )
    )
    if not current_wan_rule:
        xml_filter.append(openvpn_wan_rule)
        changed = True

    if not current_internal_rule:
        xml_filter.append(openvpn_internal_rule)
        changed = True

    return changed


def create_openvpn_gateways(root: ET.Element) -> bool:
    """Creates the gateways for openvpn.

    Args:
        root (ET.Element): The root of an opnsense config file.

    Returns:
        bool: The change status.
    """
    new_gateway_v6 = ET.fromstring(
        """
        <gateway_item>
            <interface>wan</interface>
            <gateway>dynamic</gateway>
            <name>WAN_DHCP6</name>
            <priority>254</priority>
            <weight>1</weight>
            <ipprotocol>inet6</ipprotocol>
            <interval/>
            <descr>Interface WAN_DHCP6 Gateway</descr>
            <monitor_disable>1</monitor_disable>
            <defaultgw>1</defaultgw>
        </gateway_item>
        """
    )
    new_gateway_v4 = ET.fromstring(
        """
        <gateway_item>
            <interface>wan</interface>
            <gateway>dynamic</gateway>
            <name>WAN_DHCP</name>
            <priority>254</priority>
            <weight>1</weight>
            <ipprotocol>inet</ipprotocol>
            <interval/>
            <descr>Interface WAN_DHCP Gateway</descr>
            <monitor_disable>1</monitor_disable>
            <defaultgw>1</defaultgw>
        </gateway_item>
        """
    )
    xml_gateways = root.find("gateways")
    current_gateways = xml_gateways.findall("gateway_item")
    empty_elements = list(
        filter(
            lambda rule: rule.find("name") is None,
            current_gateways,
        )
    )
    elements_with_content = list(
        filter(
            lambda rule: rule.find("name") is not None,
            current_gateways,
        )
    )

    current_gateway_v6 = list(
        filter(
            lambda rule: rule.find("name").text == "WAN_DHCP6",
            elements_with_content,
        )
    )
    current_gateway_v4 = list(
        filter(
            lambda rule: rule.find("name").text == "WAN_DHCP",
            elements_with_content,
        )
    )

    changed = False
    if empty_elements:
        for empty_elem in empty_elements:
            xml_gateways.remove(empty_elem)
        changed = True

    if not current_gateway_v6:
        xml_gateways.append(new_gateway_v6)
        changed = True

    if not current_gateway_v4:
        xml_gateways.append(new_gateway_v4)
        changed = True

    return changed


def create_openvpn_server(root: ET.Element) -> bool:
    changed = False
    # Check if the vpn server already exists.
    openvpn_xml = root.find("openvpn")
    if openvpn_xml is None:
        openvpn_xml = ET.SubElement(root, "openvpn")
        changed = True
    else:
        openvpn_xml_servers = openvpn_xml.findall("openvpn-server")
        if openvpn_xml_servers:
            empty_servers = list(
                filter(
                    lambda server: server.find("description") is None,
                    openvpn_xml_servers,
                )
            )
            for empty_server in empty_servers:
                openvpn_xml.remove(empty_server)

            if empty_servers:
                changed = True
                # Get the list without empty servers.
                openvpn_xml_servers = openvpn_xml.findall("openvpn-server")

            matching_servers = list(
                filter(
                    lambda server: server.find("description").text == "CIinaBox VPN",
                    openvpn_xml_servers,
                )
            )
            if matching_servers:
                return changed

    # Create a new VPN server.

    # Get the ca refid.
    ca_xml_list = root.findall("ca")
    ciinabox_ca = list(
        filter(
            lambda ca: ca.find("descr") is not None
            and ca.find("descr").text == "CIinaBox Certificate Authority",
            ca_xml_list,
        )
    )
    ca_ref = ciinabox_ca[0].find("refid").text
    # Get the vpn cert refid.
    cert_xml_list = root.findall("cert")
    ciinabox_vpn = list(
        filter(
            lambda cert: cert.find("descr") is not None
            and cert.find("descr").text == "CIinaBox VPN",
            cert_xml_list,
        )
    )
    vpn_cert_ref = ciinabox_vpn[0].find("refid").text
    # Create the static key.
    static_key = subprocess.getoutput("openvpn --genkey --secret /dev/stdout")
    static_key_encoded = base64.b64encode(static_key.encode("ascii")).decode("utf-8")
    # Create and add the xml for the server.
    openvpn_xml.append(
        ET.fromstring(
            f"""
            <openvpn-server>
                <vpnid>1</vpnid>
                <authmode>Local Database</authmode>
                <mode>server_tls_user</mode>
                <caref>{ ca_ref }</caref>
                <certref>{ vpn_cert_ref }</certref>
                <protocol>UDP</protocol>
                <interface>wan</interface>
                <local_port>1194</local_port>
                <description>CIinaBox VPN</description>
                <tls>{ static_key_encoded }</tls>
                <tlsmode>auth</tlsmode>
                <dh_length>4096</dh_length>
                <tunnel_network>10.10.0.0/24</tunnel_network>
                <local_network>172.16.0.0/12</local_network>
                <dynamic_ip>on</dynamic_ip>
                <pool_enable>on</pool_enable>
                <crypto>AES-256-CBC</crypto>
                <digest>SHA512</digest>
            </openvpn-server>
            """
        )
    )
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ensure a OPNsense config.xml file contains a ca and a vpn certificate."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help='the path of the config.xml file, e.g. "./config.xml" or "/home/user/config.xml".',
    )
    parser.add_argument(
        "--output",
        type=str,
        help="the output file for the xml (default: the config.xml file).",
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.config_path

    config_xml_tree, config_xml_root = xml_helpers.get_xml_tree(args.config_path)
    changed = xml_elem(config_xml_root, True)
    changed = change_setting_private_network_to_wan(config_xml_root, False) or changed
    changed = create_user_client_certificates(config_xml_root) or changed
    changed = create_openvpn_interface(config_xml_root) or changed
    changed = create_openvpn_firewall_rules(config_xml_root) or changed
    changed = create_openvpn_gateways(config_xml_root) or changed
    changed = create_openvpn_server(config_xml_root) or changed

    if changed:
        xml_helpers.indent(config_xml_root)
        config_xml_tree.write(args.output)
        print("The vpn configuration was changed.")
