import os
import subprocess
import tempfile
import base64
import ipaddress

import xml.etree.ElementTree as ET

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from typing import List, Union, Tuple

import cryptography_helpers
import xml_helpers


class CertificateWrapper:
    def __init__(
        self,
        cert: Union[x509.Certificate, None] = None,
        key: Union[rsa.RSAPrivateKey, None] = None,
        refid: Union[str, None] = None,
    ):
        """
        Generates a wrapper for a certificate and its private key.

            Parameters:
                cert : x509.Certificate | None
                    The certificate (default: None).

                key : rsa.RSAPrivateKey | None
                    The key (default: None).

                refid : str | None
                    The xml refid (default: None).

            Returns:
                CertificateWrapper
        """
        self.cert = cert
        self.key = key
        self.refid = refid

    def from_xml(self, root: ET.Element):
        """ """
        self.cert = cryptography_helpers.load_certificate_from_b64encoded_string(
            root.find("crt").text
        )
        self.key = cryptography_helpers.load_private_key_from__b64encoded_string(
            root.find("prv").text
        )
        self.refid = root.find("refid").text
        return self

    def get_cert(self) -> x509.Certificate:
        """
        Returns the x509 certificate stored in the wrapper.

            Returns:
                x509.Certificate
        """
        return self.cert

    def get_key(self) -> rsa.RSAPrivateKey:
        """
        Returns the private key stored in the wrapper.

            Returns:
                rsa.RSAPrivateKey
        """
        return self.key

    def add_contents_to_xml(self, root: ET.Element, refid: str = None) -> str:
        """
        Fills the contents of a cert or ca xml Element.

            Parameters:
                root : ET.Element
                    A ca or cert xml Element.

                refid : str
                    The refid of this Certificate (default: None).

            Returns:
                str
                    The refid of this Certificate.
        """
        # Create the xml elements
        refid_xml = ET.SubElement(root, "refid")
        descr_xml = ET.SubElement(root, "descr")
        crt_xml = ET.SubElement(root, "crt")
        prv_xml = ET.SubElement(root, "prv")

        # Fill the text of the xml elements
        if refid is None:
            refid = cryptography_helpers.get_php_uniqid()
        refid_xml.text = refid

        description = cryptography_helpers.get_cert_description_or_None(self.cert)
        if description is None:
            description = "CIinaBox"
        descr_xml.text = description

        crt_xml.text = base64.b64encode(
            self.cert.public_bytes(serialization.Encoding.PEM)
        ).decode("utf-8")

        prv_xml.text = base64.b64encode(
            self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        ).decode("utf-8")

        return refid


class CertificateAuthority:
    """
    Contains a CA with all its signed certificates.

        Methods:
            vpn_cert_exists(): bool
                Checks if this CA has a stored VPN certificate.

            generate_cert(): None
                Generates a new Certificate signed by this CA.

            add_to_xml_root(): None
                Stores the CA and its certificates in a ET.Element.
    """

    def __init__(
        self,
        certificate: CertificateWrapper,
        certs: List[CertificateWrapper] = None,
        refid: Union[str, None] = None,
    ):
        """
        Set the parameters of a CA.

            Parameters:
                certificate : CertificateWrapper
                    A CertificateWrapper Instance containing
                    a ca certifikate and key.

                certs : List[CertificateWrapper]
                    A list of CertificateWrappers belonging
                    to this CA.

                refid : str | None
                    The uniqid used in the xml file as the refid.

            Returns:
                CertificateAuthority
        """
        self.certificate = certificate

        if certs is None:
            certs = []
        self.certs = certs

        self.refid = refid

    def has_cert(self, description: str = "CIinaBox VPN") -> bool:
        """
        Checks if a vpn certificate signed by this CA exists.

            Parameters:
                description : str
                    The nsComment of the Certificate (default: "CIinaBox VPN").

            Returns:
                exists : bool
                    Bool describing if a vpn cert exists.
        """
        for cert in self.certs:
            cert_description = cryptography_helpers.get_cert_description_or_None(
                cert.get_cert()
            )
            if cert_description is not None and cert_description == description:
                return True
        return False

    def generate_cert(
        self,
        validity_in_days: int = 1095,
        subject: str = "/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN=ciinabox-vpn",
        comment: str = "CIinaBox VPN",
        url: str = None,
        ip_addresses: List[ipaddress.IPv4Address] = None,
    ) -> int:
        """
        Generates a certificate signed by this CA.

        Parameters:
            validity_in_days : int
                The duration the CA will be valid for in days (default: 1095).

            subject : str
                A x509 subject in a string. Each Attribute (C,ST,L,O,OU,CN) in the
                string is preceeded by a '/' and after each Attibute is a '='
                followed by the value of the attribute (default:
                "/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN=ciinabox-vpn").

            comment : str
                The nsComment to be added to the certificate
                (default: "CIinaBox VPN").

            url : str | None
                The URL this certificate should be valid for (default: None).

            ip_addresses: List[ipaddress.IPv4Address] | None
                The ip addresses this certificate should be valid for (default: None).

        Returns:
            int :
                The index of the certificate in self.certs.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Store the paths to all the files needed.
            private_key_path = os.path.join(tmpdir, "key.pem")
            csr_path = os.path.join(tmpdir, "cert.csr")
            extfile_path = os.path.join(tmpdir, "extfile.cnf")
            certificate_path = os.path.join(tmpdir, "cert.pem")

            # Write the ca key and certificate to a file so they can be used
            # by openssl for the certificate generation.
            ca_private_key_path = os.path.join(tmpdir, "ca-key.pem")
            with open(ca_private_key_path, "w") as private_key_file:
                private_key_file.write(
                    self.certificate.get_key()
                    .private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                    .decode("utf-8")
                )

            ca_certificate_path = os.path.join(tmpdir, "ca-cert.pem")
            with open(ca_certificate_path, "w") as certificate_file:
                certificate_file.write(
                    self.certificate.get_cert()
                    .public_bytes(serialization.Encoding.PEM)
                    .decode("utf-8")
                )

            # Generate the server key and a CSR.
            subprocess.run(
                f'openssl req -nodes -new -subj "{subject}"'
                f" -newkey rsa:4096 -sha512 -keyout {private_key_path} -out {csr_path}",
                shell=True,
                check=True,
            )

            # Create an extfile with the config for the certificate.
            with open(extfile_path, "w") as extfile:
                extfile.write(
                    f"basicConstraints=CA:FALSE\nnsCertType=server\n"
                    f'nsComment="{comment}"\nsubjectKeyIdentifier=hash\n'
                    "authorityKeyIdentifier=keyid,issuer\n"
                    "extendedKeyUsage=serverAuth,1.3.6.1.5.5.8.2.2\n"
                    f"keyUsage=digitalSignature,keyEncipherment"
                )
                if url is not None or ip_addresses is not None:
                    alt_name_str = '\nsubjectAltName="'
                    firstWrite = True  # For handling the first ',' correctly.

                    if url is not None:
                        alt_name_str += f"DNS:{url}"
                        firstWrite = False

                    for ip_address in ip_addresses:
                        if firstWrite:
                            alt_name_str += f"IP:{ip_address}"
                            firstWrite = False
                            continue

                        alt_name_str += f", IP:{ip_address}"

                    alt_name_str += '"'
                    extfile.write(alt_name_str)

            # Create the cert for the server
            subprocess.run(
                f"openssl x509 -req -sha512 -days {validity_in_days} -in {csr_path} -CA {ca_certificate_path}"
                f" -CAkey {ca_private_key_path} -out {certificate_path} -extfile {extfile_path} -CAcreateserial",
                shell=True,
                check=True,
            )

            # Read the certificate and private key from the generated
            # files and store it.
            certificate = CertificateWrapper(
                cryptography_helpers.load_certificate_from_file(certificate_path),
                cryptography_helpers.load_private_key_from_file(private_key_path),
            )
            self.certs.append(certificate)

            return len(self.certs) - 1

    def add_to_xml_root(self, root: ET.Element) -> None:
        """
        Adds this CA and its certificates to a ET.Element.

        The ca will be added in a ca element in the top level
        and the certificates will each be added in the top
        level in a cert element.

            Parameters:
                root : ET.Element
                    The root ET.Element of a OPNsense config.

            Returns:
                None
        """
        changed = False
        is_new_ca = True

        if self.refid is not None:
            # Check if this ca already exists in the root.
            ca_list = root.findall("./ca")
            ca_xml = xml_helpers.get_refid_match_from_list(ca_list, self.refid)
            if ca_xml is not None:
                is_new_ca = False

        if is_new_ca:
            # Create the ca xml element and fill it with the
            # certificate, private key, description and refid.
            ca_xml = ET.SubElement(root, "ca")
            refid = self.certificate.add_contents_to_xml(ca_xml)
            self.refid = refid

            changed = True

        # Do the same for the certificate
        counter = 0
        if not is_new_ca:
            existing_xml_certificates = root.findall("cert")

        for cert in self.certs:
            cert_xml = ET.Element("cert")
            _ = cert.add_contents_to_xml(cert_xml)

            # Add the refid of the ca to the cert xml element.
            caref_xml = ET.Element("caref")
            caref_xml.text = self.refid
            cert_xml.insert(2, caref_xml)

            # Check if this certificate already exists.
            if not is_new_ca:
                old_cert_xml = xml_helpers.get_cert_elem_match_from_list(
                    existing_xml_certificates, cert_xml
                )
                if old_cert_xml is not None:
                    continue

            root.append(cert_xml)
            counter += 1

        # Add the serial field to the ca xml element.
        # The serial field contains the number of certs
        # signed by this ca.
        if is_new_ca:
            serial_xml = ET.SubElement(ca_xml, "serial")
        else:
            serial_xml = ca_xml.find("serial")
        serial_xml.text = str(counter)

    def write_root_cert_to_disk(self, path):
        with open(path, "wb") as file:
            file.write(self.certificate.cert.public_bytes(serialization.Encoding.PEM))


class CertificateAuthorityBuilder:
    """
    Creates a CertificateAuthority instance.

    The Certificate Authority can either be created
    or loaded from a ET.Element.

        Methods:
            from_xml_root() : CertificateAuthority
                Loads a CA from a ET.Element.

            create() : CertificateAuthority
                Generates a new CA.
    """

    def from_xml_root(self, root: ET.Element) -> Tuple[CertificateAuthority, bool]:
        """
        Loads a CIinaBox CertificateAuthority from an opnsense xml config.

        In the case that there is no existing CIinaBox Certificate Authority
        entry in the xml, a new Certificate Authority will be created.

            Parameters:
                root : ET.ELement
                    The root ET.Element of a OPNsense config.

            Returns:
                CertificateAuthority :
                    The CIinaBox CA.
                bool :
                    The change status.
        """
        certificates = root.findall("./cert")
        authorities = root.findall("./ca")

        # Remove all empty elements.
        if authorities:
            empty_elements = list(
                filter(lambda x: x.find("./refid") is None, authorities)
            )

            for elem in empty_elements:
                root.remove(elem)

            if empty_elements:
                # Renew the ca list since empty elements were removed.
                authorities = root.findall("./ca")

        try:
            ciinabox_ca = list(
                filter(
                    lambda a: a.find("descr").text == "CIinaBox Certificate Authority",
                    authorities,
                )
            )[0]
        except IndexError:
            return self.create(), True

        ca_wrapper = CertificateWrapper(None, None).from_xml(ciinabox_ca)
        refid = ciinabox_ca.find("refid").text
        ciinabox_ca = CertificateAuthority(ca_wrapper, None, refid)

        # Get the certificates signed by this ca.
        signed_certs = list(
            filter(
                lambda cert: cert.find("./caref") is not None
                and cert.find("./caref").text == refid,
                certificates,
            )
        )
        for cert in signed_certs:
            # Add all certificates to the CertificateAuthority Instance.
            ciinabox_ca.certs.append(CertificateWrapper(None, None).from_xml(cert))

        return ciinabox_ca, False

    def create(
        self,
        validity_in_days: int = 1095,
        subject: str = "/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN=ciinabox-ca",
        comment: str = "CIinaBox Certificate Authority",
    ) -> CertificateAuthority:
        """
        Creates a self-signed CertificateAuthority.

        Parameters:
            validity_in_days : int
                The duration the CA will be valid for in days (default: 1095).

            subject : str
                A x509 subject in a string. Each Attribute (C,ST,L,O,OU,CN) in the
                string is preceeded by a '/' and after each Attibute is a '='
                followed by the value of the attribute (default:
                "/C=DE/ST=Bavaria/L=Augsburg/O=HSA_innos/OU=CIinaBox/CN=ciinabox-ca").

            comment : str
                The nsComment to be added to the certificate
                (default: "CIinaBox Certificate Authority").

        Returns:
            CertificateAuthority
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            private_key_path = os.path.join(tmpdir, "key.pem")
            certificate_path = os.path.join(tmpdir, "cert.pem")

            # Create the x509 cert and the private key by using openssl.
            subprocess.run(
                f"openssl req -x509 -nodes -days {validity_in_days} -newkey rsa:4096 -sha512"
                f' -keyout {private_key_path} -out {certificate_path} -subj "{subject}"'
                f" -addext \"nsComment='{comment}'\""
                ' -addext "keyUsage=critical,digitalSignature,keyCertSign,cRLSign"',
                shell=True,
                check=True,
            )

            # Read the certificate and private key
            # from the generated files.
            certificate = CertificateWrapper(
                cryptography_helpers.load_certificate_from_file(certificate_path),
                cryptography_helpers.load_private_key_from_file(private_key_path),
            )

            # Remove the key and certificate
            os.remove(private_key_path)
            os.remove(certificate_path)

            # Create the CertificateAuthority and return it.
            return CertificateAuthority(certificate, certs=None, refid=None)
