import argparse
import base64
import json
from typing import List

import xml.etree.ElementTree as ET

import bcrypt

import xml_helpers


def configure_domain(root: ET.Element, domain: str = "demo") -> bool:
    """
    Configures the domain the router will give leases for.

        Parameters:
            root : ET.Element
                The root ET.Element of the opnsense config.

            domain : str
                The new domain of the router (default: "demo").

        Returns:
            changed : bool
                The change status to the xml Element.
    """
    domain_xml = root.find("./system/domain")
    if domain_xml.text == domain:
        return False

    domain_xml.text = domain
    return True


def change_setting_unbound_dns_for_dhcp_mappings(
    root: ET.Element, enable: bool
) -> bool:
    """Enables/Disables unbound dns for dhcp mappings.

    Args:
        root (ET.Element): The xml root of a opnsense config file.
        enable (bool): Enable unbound dns for dhcp mappings.

    Returns:
        bool: The change status.
    """
    unbound = root.find("unbound")
    xml_enabled = unbound.find("regdhcpstatic")

    if xml_enabled is None and enable:
        enable_elem = ET.Element("regdhcpstatic")
        enable_elem.text = str(1)
        unbound.insert(1, enable_elem)
        return True

    if xml_enabled and not enable:
        unbound.remove(xml_enabled)
        return True

    return False


def configure_root_user_ssh_key(root: ET.Element, ssh_key: str) -> bool:
    """Configures the root users ssh key.

    Args:
        root (ET.Element): The xml root of a opnsense config file.
        ssh_key (str): The ssh key of the root user.

    Returns:
        bool: The change status.
    """
    xml_user_list = root.findall("./system/user")
    root_user_xml: ET.Element = list(
        filter(lambda user: user.find("uid").text == "0", xml_user_list)
    )[0]

    base64_encoded_ssh_key = base64.b64encode(ssh_key.encode("ascii")).decode("ascii")
    authorized_keys = root_user_xml.find("authorizedkeys")

    if authorized_keys is None:
        authorized_keys = ET.Element("authorizedkeys")
        authorized_keys.text = base64_encoded_ssh_key
        root_user_xml.insert(7, authorized_keys)
        return True

    if authorized_keys.text is None or authorized_keys.text != base64_encoded_ssh_key:
        authorized_keys.text = base64_encoded_ssh_key
        return True

    return False


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
    parser.add_argument(
        "--ssh_key",
        type=str,
        help="the ssh public key for the root user (default: None).",
        default=None,
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.config_path

    config_xml_tree, config_xml_root = xml_helpers.get_xml_tree(args.config_path)

    changed = configure_domain(config_xml_root)

    changed = (
        change_setting_unbound_dns_for_dhcp_mappings(config_xml_root, True) or changed
    )

    if args.ssh_key is not None:
        changed = configure_root_user_ssh_key(config_xml_root, args.ssh_key) or changed

    if changed:
        xml_helpers.indent(config_xml_root)
        config_xml_tree.write(args.output)
        print("The general configuration was changed.")
