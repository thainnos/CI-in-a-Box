import os
import ipaddress
import argparse

import xml.etree.ElementTree as ET

import xml_helpers


def configure_xml_lan_interface(
    config_root: ET.Element,
    ip_addr: ipaddress.IPv4Address = ipaddress.IPv4Address("172.16.0.1"),
    subnet: str = "12",
) -> bool:
    """
    Reconfigures the ./interfaces/lan element of a ET.Element.

        Parameters:
            config_root : ET.Element
                A ET.Element containing a ./interface/lan element.
            ip_addr : ipaddress.IPv4Address, optional
                The new lan ip address of the router (default: ipaddress.IPv4Address("172.16.0.1")).
            subnet : str, optional
                The new lan subnet (in CIDR notation) of the router (default: "12").

        Returns:
            changed : bool
                Bool describing if the ./interfaces/lan element was changed.
    """
    lan = config_root.find("./interfaces/lan")
    interface_name = config_root.find("./interfaces/lan/if").text

    new_config = f"<lan><if>{ interface_name }</if><enable>1</enable><ipaddr>{ str(ip_addr) }</ipaddr><subnet>{ subnet }</subnet><ipaddrv6>track6</ipaddrv6><subnetv6>64</subnetv6><media /><mediaopt /><track6-interface>wan</track6-interface><track6-prefix-id>0</track6-prefix-id></lan>"
    new_lan = ET.fromstring(new_config)

    # Make sure both lans have the same format.
    xml_helpers.indent(lan)
    xml_helpers.indent(new_lan)

    if ET.tostring(lan) == ET.tostring(new_lan):
        return False

    interface = config_root.find("./interfaces")
    interface.remove(lan)
    interface.insert(1, new_lan)
    return True


def configure_lan_dhcp(
    config_root: ET.Element,
    dhcp_range_start: ipaddress.IPv4Address = ipaddress.IPv4Address("172.16.3.1"),
    dhcp_range_end: ipaddress.IPv4Address = ipaddress.IPv4Address("172.16.3.254"),
):
    """
    Reconfigures the ./dhcpd/lan/range element of a ET.Element.

        Parameters:
            config_root : ET.Element
                A ET.Element containing a ./interface/lan element.
            dhcp_range_start : ipaddress.IPv4Address, optional
                The start of the lan dhcp range of the router (default: ipaddress.IPv4Address("172.16.3.1")).
            dhcp_range_end : ipaddress.IPv4Address, optional
                The end of the lan dhcp range of the router (default: ipaddress.IPv4Address("172.16.3.254")).

        Returns:
            changed : bool
                Bool describing if the ./dhcpd/lan/range element was changed.
    """
    range = config_root.find("./dhcpd/lan/range")

    new_range_text = f"<range><from>{str(dhcp_range_start)}</from><to>{str(dhcp_range_end)}</to></range>"
    new_range = ET.fromstring(new_range_text)

    # Make sure both ranges have the same format.
    xml_helpers.indent(range)
    xml_helpers.indent(new_range)

    if ET.tostring(range) == ET.tostring(new_range):
        return False

    lan = config_root.find("./dhcpd/lan")
    lan.remove(range)
    lan.insert(0, new_range)

    return True


def configure_dhcp_staticmaps(
    config_root: ET.Element,
    static_map_dir: os.path,
):
    """
    Configure the staticmap entries of a ET.Element.

        Parameters:
            config_root : ET.Element
                A ET.Element containing a ./dhcpd element.
            static_map_dir : os.path
                The path to the directory containing xml files with a staticsmap element.

        Returns:
            changed : bool
                Bool describing if the ./dhcpd element was changed.
    """
    if static_map_dir is None:
        # Nothing can be changed since no staticnap dir was supplied.
        return False

    # Get the file paths for all staticmap files.
    dir_contents = os.listdir(static_map_dir)
    static_map_files = list(
        map(lambda file: os.path.join(static_map_dir, file), dir_contents)
    )

    # Get the current dhcpd xml element and
    # all presently configured staticmaps.
    xml_dhcpd = config_root.find("./dhcpd")
    xml_static_maps = xml_dhcpd.findall("./staticmap")
    changed = False

    if xml_static_maps:
        # staticmap entries exist.
        for file in static_map_files:
            _, map_root = xml_helpers.get_xml_tree(file)

            # Check if this entry already exists.
            hostname = map_root.find("./hostname").text
            matches = list(
                filter(
                    lambda staticmap: staticmap.find("./hostname").text == hostname,
                    xml_static_maps,
                )
            )

            # Add the entry if it doesn't match any present entries.
            if not matches:
                xml_dhcpd.append(map_root)
                changed = True
    else:
        # No staticmap entries exist.
        for file in static_map_files:
            _, map_root = xml_helpers.get_xml_tree(file)
            xml_dhcpd.append(map_root)
            changed = True

    return changed


if __name__ == "__main__":
    # Use an ArgumentParser Instance for CLI.
    parser = argparse.ArgumentParser(
        description="Configure the lan interface of an OPNsense config.xml file."
    )
    parser.add_argument(
        "path",
        type=str,
        help='the path of the config.xml file, e.g. "./config.xml" or "/home/user/config.xml".',
    )
    parser.add_argument(
        "--ip",
        type=str,
        help='the new IP address of the router (default: "172.16.0.1").',
        default="172.16.0.1",
    )
    parser.add_argument(
        "--subnet",
        type=str,
        help='the new subnet of the router (default: "12").',
        default="12",
    )
    parser.add_argument(
        "--dhcp_start",
        type=str,
        help='the start of the lan dhcp range of the router (default: "172.16.3.1").',
        default="172.16.3.1",
    )
    parser.add_argument(
        "--dhcp_end",
        type=str,
        help='the end of the lan dhcp range of the router (default: "172.16.3.1").',
        default="172.16.3.254",
    )
    parser.add_argument(
        "--static_map_dir",
        type=str,
        help="the path to the directory containing xml files with a staticsmap element (default: None).",
        default=None,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="the output file for the xml (default: the input file).",
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.path

    tree, root = xml_helpers.get_xml_tree(args.path)

    # Configure the interface, the dhcpd and the staticmaps.
    changed = configure_xml_lan_interface(
        root,
        ipaddress.IPv4Address(args.ip),
        args.subnet,
    )
    changed = (
        configure_lan_dhcp(
            root,
            ipaddress.IPv4Address(args.dhcp_start),
            ipaddress.IPv4Address(args.dhcp_end),
        )
        or changed
    )
    # Only add staticmaps if the directory exists.
    static_map_dir = args.static_map_dir
    if (
        static_map_dir is not None
        and os.path.exists(static_map_dir)
        and os.path.isdir(static_map_dir)
    ):
        changed = configure_dhcp_staticmaps(root, static_map_dir) or changed

    # Write the configuration if changes occurred.
    if changed:
        print("The lan interface configuration was changed.")
        xml_helpers.indent(root)
        tree.write(args.output)
