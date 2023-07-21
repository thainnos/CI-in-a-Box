import os
import argparse
import ipaddress

import xml.etree.ElementTree as ET

from cryptography.hazmat.primitives import serialization

import xml_helpers
from ca import CertificateAuthority, CertificateAuthorityBuilder


def set_router_web_certificate(root: ET.Element) -> bool:
    """
    Changes the web certificate used by the router.

        Parameters:
            root : ET.Element
                The root element of a opnsense xml config file.

        Returns:
            bool :
                If the routers web cert was changed.
    """
    # Get the certificate for the router web interface.
    cert_list = root.findall("./cert")
    server_certificate = list(
        filter(
            lambda cert: cert.find("./descr").text == "CIinaBox Router Web", cert_list
        )
    )

    if server_certificate:
        # Get the refid currently in use and the cert refid
        refid = server_certificate[0].find("refid")
        webgui_ssl_ref = root.find("./system/webgui/ssl-certref")

        if webgui_ssl_ref.text != refid.text:
            # Update the refid.
            webgui_ssl_ref.text = refid.text
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
        "--root_cert",
        type=str,
        default=None,
        help="the output file for the root ca certificate. The certificate will only be written if this option is set.",
    )
    parser.add_argument(
        "--certs_dir",
        type=str,
        help="the path to the directory where the certificates will be stored (default: None).",
        default=None,
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.config_path

    config_xml_tree, config_xml_root = xml_helpers.get_xml_tree(args.config_path)
    changed = False

    ciinabox_ca, changed = CertificateAuthorityBuilder().from_xml_root(config_xml_root)

    domain = ".demo"

    if not ciinabox_ca.has_cert():
        ciinabox_ca.generate_cert()
        ciinabox_ca.add_to_xml_root(config_xml_root)
        changed = True

    if not ciinabox_ca.has_cert("CIinaBox Router Web"):
        lan_ip_address = config_xml_root.find("./interfaces/lan/ipaddr").text
        if lan_ip_address is None:
            lan_ip_address = "172.16.0.1"
        ciinabox_ca.generate_cert(
            subject="/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN=ciinabox-router-web",
            comment="CIinaBox Router Web",
            url="opnsense" + domain,
            ip_addresses=[ipaddress.IPv4Address(lan_ip_address)],
        )
        ciinabox_ca.add_to_xml_root(config_xml_root)
        changed = True

    changed = set_router_web_certificate(config_xml_root) or changed

    if args.root_cert is not None:
        ciinabox_ca.write_root_cert_to_disk(args.root_cert)

    if changed:
        xml_helpers.indent(config_xml_root)
        config_xml_tree.write(args.output)
        print("The certificate configuration was changed.")
