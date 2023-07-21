import os
import argparse

import xml.etree.ElementTree as ET
import xml_helpers


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
    xml_dhcpd = config_root.find("./dhcpd/lan")
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
        description="Configure the dhcp staticmaps of an OPNsense config.xml file."
    )
    parser.add_argument(
        "path",
        type=str,
        help='the path of the config.xml file, e.g. "./config.xml" or "/home/user/config.xml".',
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

    # Only add staticmaps if the directory exists.
    static_map_dir = args.static_map_dir
    if (
        static_map_dir is not None
        and os.path.exists(static_map_dir)
        and os.path.isdir(static_map_dir)
    ):
        changed = configure_dhcp_staticmaps(root, static_map_dir)

    # Write the configuration if changes occurred.
    if changed:
        print("The staticmap configuration was changed.")
        xml_helpers.indent(root)
        tree.write(args.output)
