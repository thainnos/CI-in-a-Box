import sys
from typing import List, Tuple, Union

import xml.etree.ElementTree as ET


def get_cert_elem_match_from_list(
    elem_list: List[ET.Element],
    cert_elem: ET.Element,
) -> str:
    """
    Returns None or the list elements with the same caref and prv.

        Parameters:
            root : list[ET.Element]
                A list of ET.Element.

            cert_elem : ET.Element
                A xml cert entry.

        Returns:
            ET.Element | None
                The cert Element with this refid or None.
    """
    elem_list_with_carefs = list(
        filter(lambda elem: elem.find("caref") != None, elem_list)
    )
    matches = list(
        filter(
            lambda cert: cert.find("caref").text == cert_elem.find("caref").text
            and cert.find("prv").text == cert_elem.find("prv").text,
            elem_list_with_carefs,
        )
    )

    if matches:
        return matches[0]
    return None


def get_refid_match_from_list(
    elem_list: List[ET.Element],
    refid: str,
) -> str:
    """
    Returns None or the list element with the refid.

        Parameters:
            root : list[ET.Element]
                A list of ET.Element.

            refid : str
                A php uniqid of a cert entry.

        Returns:
            ET.Element | None
                The cert Element with this refid or None.
    """
    matches = list(filter(lambda ca: ca.find("refid").text == refid, elem_list))

    if matches:
        return matches[0]
    return None


def indent(elem: ET.Element, level: int = 0) -> None:
    """
    Correctly indents the xml of elem.

        Parameters:
            elem : ET.Element
                Any ET.Element.
            level : int
                The identation amount (default: 0)

        Returns:
            None
    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_xml_tree(filename: str) -> Tuple[ET.ElementTree, ET.Element]:
    """
    Returns an xml ElementTree and root Element for the file "filename".

        Parameters:
            filename : str
                A path to a xml file.

        Returns:
            tree : ET.ElementTree
                The ElementTree for the file.

            root : ET.Element
                The root Element of the file.
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except:
        sys.stderr.write(f"Invalid file name or the file { filename } doesn't exist.\n")
        sys.exit(1)
    return tree, root
