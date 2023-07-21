import time
import math
import base64

from cryptography import x509
from cryptography.hazmat.primitives import serialization


def load_certificate_from_b64encoded_string(encoded: str):
    bytes = base64.b64decode(encoded)

    return x509.load_pem_x509_certificate(bytes)


def load_private_key_from__b64encoded_string(encoded: str):
    bytes = base64.b64decode(encoded)

    return serialization.load_pem_private_key(bytes, password=None)


def load_certificate_from_file(filename):
    with open(filename, "rb") as file:
        bytes = file.read()
    return x509.load_pem_x509_certificate(bytes)


def load_private_key_from_file(filename):
    with open(filename, "rb") as file:
        bytes = file.read()

    return serialization.load_pem_private_key(bytes, password=None)


def is_ca_cert(cert: x509.Certificate):
    try:
        return cert.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
    except:
        return False


def get_cert_description_or_None(certificate: x509.Certificate):
    description = None

    for extension in certificate.extensions:
        if type(extension.value) == x509.UnrecognizedExtension:
            description = extension.value.value
            description = description[2:]
            description = description.decode("utf-8")

    return description


def get_php_uniqid():

    m = time.time()
    s = math.floor(m)
    u = math.floor(1000000 * (m - s))

    return str("%8x%05x" % (s, u))
