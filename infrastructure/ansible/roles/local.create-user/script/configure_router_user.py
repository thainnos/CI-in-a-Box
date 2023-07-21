import argparse
import base64
import json
from typing import List

import xml.etree.ElementTree as ET

import bcrypt

import xml_helpers


def consume_next_uid(root: ET.Element) -> int:
    """
    Returns the next uid and raises the xml nextuid field by one.

        Parameters:
            root : ET.Element
                The xml root of a opnsense config file.

        Returns:
            int :
                The currently usable uid.
    """
    next_uid_xml = root.find("./system/nextuid")
    uid = int(next_uid_xml.text)
    next_uid_xml.text = str(uid + 1)

    return uid


class User:
    def __init__(
        self,
        name: str,
        password: str,
        scope: str = "user",
        uid: int = None,
    ) -> None:
        """
        Creates a user instance.

            Parameters:
                name : str
                    The username of this user.

                password : str
                    The unhashed password of this user.

                scope : str
                    The access scope of this user (default: "user").

                uid : int | None

            Returns:
                None
        """
        self.name = name
        self.password = password
        self.scope = scope
        self.uid = str(uid)

    def to_xml(self) -> ET.Element:
        """
        Returns a user xml Element representing this instance.

            Parameters:
                None

            Returns:
                ET.Element :
                    The user xml element representing this instance.
        """
        hashed_password = bcrypt.hashpw(
            self.password.encode(encoding="UTF-8"), bcrypt.gensalt()
        ).decode("ascii")

        return ET.fromstring(
            "<user>"
            f"<name>{ self.name }</name>"
            f"<scope>{ self.scope }</scope>"
            f"<password>{ hashed_password }</password>"
            "<descr/><expires/><authorizedkeys/><ipsecpsk/><otp_seed/>"
            f"<uid>{ self.uid }</uid>"
            "</user>"
        )

    def user_exists(self, root: ET.Element) -> bool:
        """
        Checks if the user is already in a opnsense config.

        A user is counted as already in the config if it
        either has the same uid as the class instance or
        it's xml is the same as the xml the class generates.

            Parameters:
                root : ET.Element
                    The root ET.Element of the opnsense config.

            Returns:
                bool :
                    The existance of the user in the config.
        """
        user_list = root.findall("./system/user")

        # Check if a user with the same name exists.
        matches = list(
            filter(lambda user: user.find("name").text == self.name, user_list)
        )
        if matches:
            return True

        return False


def configure_users(root: ET.Element, user_list: List[User]) -> bool:
    """
    Configures the users in a opnsense config.

        Parameters:
            root : ET.Element
                The root ET.Element of the opnsense config.

            users : List[User]
                The users the opnsense config will contain.

        Returns:
            changed : bool
                The change status to the users.
    """
    changed = False
    for user in user_list:
        if not user.user_exists(root):
            root.find("./system").append(user.to_xml())
            changed = True

    return changed


def get_user_list_from_json(
    root: ET.Element,
    json_str: str,
) -> List[User]:
    """
    Creates a list of User instances from a json string.

    Parameters:
        root : ET.Element
            The root element of a opnsense config.xml file.
        json_str : str
            A json string containing an array of dictionaries
            with the required keys "name" and "password" and
            the optional keys "scope" and "uid".

    Returns:
        List[User] :
            An array of User instances.
    """
    loaded_json = json.loads(json_str)

    user_list = []
    for entry in loaded_json:
        name = entry["name"]
        password = entry["password"]
        # Set the scope to the default if no scope is provided.
        scope = entry["scope"] if entry.get("scope") else "user"
        uid = entry.get("uid") or consume_next_uid(root)

        user_list.append(User(name, password, scope, uid))

    return user_list


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
        "--users",
        type=str,
        help="the the users to be created (default: None).",
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.config_path

    config_xml_tree, config_xml_root = xml_helpers.get_xml_tree(args.config_path)

    changed = False

    if args.users is not None:
        user_list = get_user_list_from_json(config_xml_root, args.users)
        changed = configure_users(config_xml_root, user_list) or changed

    if changed:
        xml_helpers.indent(config_xml_root)
        config_xml_tree.write(args.output)
        print("The router user configuration was changed.")
