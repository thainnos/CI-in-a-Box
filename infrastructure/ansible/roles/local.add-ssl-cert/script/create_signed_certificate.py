import os
import argparse
import ipaddress

from cryptography.hazmat.primitives import serialization

import ca
import xml_helpers
import cryptography_helpers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a signed certificate with the config.xml of an ciinabox router."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help='the path of the config.xml file, e.g. "./config.xml" or "/home/user/config.xml".',
    )
    parser.add_argument(
        "--common_name",
        type=str,
        help="the common name of the server, e.g. 'ciinabox-jenkins-top'",
    )
    parser.add_argument(
        "--comment",
        type=str,
        help="the nsComment of the server certificate, e.g. 'CIinaBox Jenkins Server Top'",
    )
    parser.add_argument(
        "--hostname",
        type=str,
        help="the hostname and domain of the server, e.g. 'jenkins-top.demo'",
    )
    parser.add_argument(
        "--ip_address",
        type=str,
        help="the ip address of the server, e.g. '172.16.1.3'.",
    )
    parser.add_argument(
        "--certs_dir",
        type=str,
        help="the path to the directory where the certificate and key will be stored (default: ./).",
        default="./",
    )
    args = parser.parse_args()

    # Assign arguments and validate them.
    config_path = args.config_path
    common_name = args.common_name
    comment = args.comment
    hostname = args.hostname
    ip_address = ipaddress.IPv4Address(args.ip_address)
    certs_dir = args.certs_dir

    # Extract the CA from the xml.
    config_xml_tree, config_xml_root = xml_helpers.get_xml_tree(config_path)
    ciinabox_ca, _ = ca.CertificateAuthorityBuilder().from_xml_root(config_xml_root)

    # Generate a signed certificate.
    cert_index = ciinabox_ca.generate_cert(
        subject=f"/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN={common_name}",
        comment=comment,
        url=hostname,
        ip_addresses=[ip_address],
    )
    wrapped_cert = ciinabox_ca.certs[cert_index]

    # Write the certificate to its file.
    cert = wrapped_cert.get_cert()
    cert_path = os.path.join(certs_dir, "crt.pem")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    # Write the key to its file.
    key = wrapped_cert.get_key()
    key_path = os.path.join(certs_dir, "key.pem")
    with open(key_path, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
