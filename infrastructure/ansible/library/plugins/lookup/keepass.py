from __future__ import absolute_import, division, print_function
import pathlib

__metaclass__ = type

DOCUMENTATION = """
name: keepass
author: Fabian Antonio Klemm
version_added: "1.0"
short_description: Fetch a keepass db entry.
description:
    - Returns the data stored in a keepass entry.
options:
    _terms:
        description: The entry to query.
    db_file:
        description: The keepass database to use.
        type: str
    db_password:
        description: The password for the keepass database.
        type: str
    parent:
        description: The parent group of the entry.
        type: str
        default: ""
    field:
        description: The field of the entry to return.
        type: str
        default: ""
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible.module_utils.common.text.converters import to_text

from pykeepass import PyKeePass


display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        # Populate options.
        self.set_options(var_options=variables, direct=kwargs)

        # Setup
        db_file = self.get_option("db_file")
        db_password = self.get_option("db_password")
        # The db_file path is different for lookups than
        # changing the db somehow. The lookup script during
        # execution is two dirs higher.
        db_file = str(pathlib.Path(*pathlib.Path(db_file).parts[2:]))
        try:
            kp = PyKeePass(db_file, db_password)
        except Exception:
            return None

        parent = self.get_option("parent")
        if parent == "":
            parent = kp.root_group
            display.v("Parent group is the root group.")
        else:
            parent = kp.find_groups_by_name(parent, first=True)
            if parent is None:
                display.v("Parent group was not found.")
            else:
                display.v("Parent group was found.")

        # Execute Search
        return_values = []
        for term in terms:
            display.v(f"Searching for entry: {term}")
            entry = kp.find_entries(title=term, group=parent, first=True)

            # Stop if no entry was found.
            if entry is None:
                display.v("Entry doesn't exist.")
                return None

            # Store the entry values in a dict.
            entry = {
                "username": to_text(entry.username),
                "password": to_text(entry.password),
                "url": to_text(entry.url),
                "notes": to_text(entry.notes),
                "tags": to_text(entry.tags),
                "expiry_time": to_text(entry.expiry_time),
                "icon": to_text(entry.icon),
            }

            entry_field = self.get_option("field")
            if entry_field == "":
                pass
            else:
                value = entry[entry_field]
                return_values.append(value)

        return return_values
