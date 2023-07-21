#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: HSAinnos HS Augsburg
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: keepass
short_description: Interact with kdbx dbs with this module.
description:
    - Create, modify, and delete keepass (kdbx) databases.
    - Can be run in check mode.
version_added: "1.0"
author: "Fabian Antonio Klemm"
options:
    db_file:
        description: 
            - The path to the database file.
        type: path
        required: True
        version_added: "1.0"
    
    db_password:
        description:
            - The password for the database.
        type: str
        required: True
        no_log: True
        vesion_added: "1.0"

    type:
        description:
            - The operation type.
        type: str    
        choices:
            - db
            - group
            - entry
        required: True
        version_added: "1.0"

    state:
        description:
            - The state of the item.
        type: str
        choices:
            - present
            - absent
        default: present
        version_added: "1.0"

    title:
        description:
            - The name of an entry or a group. 
            - Required when (type=group).
            - Required when (type=entry).
        type: str
        version_added: "1.0"

    parent:
        description:
            - The name of the parent group. 
            - If not set, the root group will be used instead.
        type: str
        version_added: "1.0"

    username:
        description:
            - The username of an entry.
            - Required when (type=entry).
        type: str
        version_added: "1.0"

    password:
        description:
            - The password of an entry.
            - Required when (type=entry).
        type: str
        no_log: True
        version_added: "1.0"

    update_password:
        description:
            - Whether to keep the password if one already exists.
        type: bool
        default: True
        version_added: "1.0.1"

    url:
        description:
            - The url of an entry.
        type: str
        version_added: "1.0"

    tags:
        description:
            - The tags of an entry.
        type: str
        version_added: "1.0"

    expiry_time:
        description:
            - The expiry_time of an entry.
        type: str
        version_added: "1.0"

    notes:
        description:
            - The notes of an entry or a group.
        type: str
        version_added: "1.0"

    icon:
        description:
            - The icon of an entry or a group.
        type: str
        version_added: "1.0"

requirements:
    - pykeepass >= 4.0
"""

EXAMPLES = r"""
- name: Ensure a database exists.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: db

- name: Ensure a database doesn't exist.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: absent
    type: db 

# This group will have the root_group as parent.
# This group will have nothing in notes and no icon.
- name: Ensure the group test exists.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: group
    title: test

# This group will have the group test as parent.
# This group will have the text Example in notes and no icon.
- name: Ensure the group test1 exists.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: group
    title: test1
    parent: test
    notes: Example

- name: Ensure the group test1 doesn't exist.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: absent
    type: group
    title: test1

# This entry will have the root_group as parent.
# This entry will have nothing in url, notes, tags, expiry_time
# or icon.
- name: Ensure the minimal entry test_entry exists.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: entry
    title: test_entry
    username: test
    password: test

# This entry will have the group test as parent.
# This entry will have the text Example in notes.
# This entry will have the url http://example.com.
- name: Ensure the entry test exists, has the parent group.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: entry
    title: test
    username: test
    password: test
    parent: test
    url: http://example.com
    notes: Example

# No changes will take place, even though another password
# was specified. Example usage:
# Using randomly generated passwords in a playbook while not
# being sure whether an entry already exists.
- name: Ensure the entry test exists, has the parent group.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: present
    type: entry
    title: test
    username: test
    password: test3,141592test
    update_password: False
    parent: test
    url: http://example.com
    notes: Example

- Ensure the entry test doesn't exist.
  keepass:
    db_file: "./db.kdbx"
    db_password: test
    state: absent
    type: entry
    title: test
"""

from ansible.module_utils.basic import *


def database_exists(data):
    import os

    filename = data["db_file"]
    password = data["db_password"]

    return (os.path.isfile(filename), filename, password)


def database_present(data, check_mode_on):
    """
    Ensures that the database is created.
    """
    from pykeepass import create_database

    db_exists, filename, password = database_exists(data)

    if not db_exists and not check_mode_on:
        # Change state.
        create_database(filename, password)

    return {
        "changed": not db_exists,
        "diff": {
            "before_state": "absent" if not db_exists else "present",
            "after_state": "present",
        },
    }


def database_absent(data, check_mode_on):
    """
    Ensures that the database doesn't exist.
    """
    db_exists, filename, _ = database_exists(data)

    if db_exists and not check_mode_on:
        # Change state.
        os.remove(filename)

    return {
        "changed": db_exists,
        "diff": {
            "before_state": "present" if db_exists else "absent",
            "after_state": "absent",
        },
    }


def group_exists(data, group_name, filename, password):
    """
    Checks if a group exists.
    """
    from pykeepass import PyKeePass

    kp = PyKeePass(filename, password)

    # Get the PyKeePass group object of the parent.
    parent = data["parent"]
    if parent is None:
        parent = kp.root_group
    else:
        parent = kp.find_groups_by_name(parent, first=True)

    # Check if the group exists.
    group = kp.find_groups(name=group_name, group=parent, first=True)
    group_present = group is not None

    return kp, group_present, parent, group


def update_group(data, group, check_mode_on):
    """
    Checks if there are differences between the
    data dict and the data stored in the group.

    returns: A dict containing all the differences.
    """
    group_changed = False
    if data["notes"] != group.notes:
        group_changed = True
        if not check_mode_on:
            group.notes = data["notes"]

    if data["icon"] != group.icon:
        group_changed = True
        if not check_mode_on:
            group.icon = data["icon"]

    # If at least one key is in changed the entry would be changed
    return group_changed


def group_present(data, check_mode_on):
    """
    Ensures a group is present.
    """
    group_name = data["title"]
    filename = data["db_file"]
    password = data["db_password"]
    kp, group_present, parent, group = group_exists(
        data, group_name, filename, password
    )

    # Set the diff to the state it would be in if
    # no entry exists so far and update it in the
    # update_group function if an entry exists.
    diff = {
        "before_state": "present" if group_present else "absent",
        "after_state": "present",
        "before_title": group.name if group_present else "absent",
        "after_title": data["title"],
        "before_parent": group.parentgroup.name if group_present else "absent",
        "after_parent": parent.name,
        "before_notes": group.notes if group_present else "absent",
        "after_notes": data["notes"],
        "before_icon": group.icon if group_present else "absent",
        "after_icon": data["icon"],
    }
    group_changed = False
    # Überprüfen, ob mindestens ein Wert anders ist,
    # wenn es die Gruppe schon gibt.
    if group_present:
        group_changed = update_group(data, group, check_mode_on)

        if group_changed and not check_mode_on:
            kp.save()

    # group_present ist true, wenn die Gruppe vorhanden ist.
    if not group_present and not check_mode_on:
        kp.add_group(
            destination_group=parent,
            group_name=group_name,
            notes=data["notes"],
            icon=data["icon"],
        )
        kp.save()

    return {
        "changed": group_changed or not group_present,
        "diff": diff,
    }


def group_absent(data, check_mode_on):
    """
    Ensures that the group is deleted.
    """
    group_name = data["title"]
    filename = data["db_file"]
    password = data["db_password"]
    kp, group_present, _, group = group_exists(data, group_name, filename, password)

    diff = {
        "before_state": "present" if group_present else "absent",
        "after_state": "absent",
        "before_title": group.name if group_present else None,
        "after_title": None,
        "before_parent": group.parentgroup.name if group_present else None,
        "after_parent": None,
        "before_notes": group.notes if group_present else None,
        "after_notes": None,
        "before_icon": group.icon if group_present else None,
        "after_icon": None,
    }

    # group_present ist True, wenn eine Gruppe existiert.
    if group_present and check_mode_on:
        kp.delete_group(group)
        kp.save()

    return {
        "changed": group_present,
        "diff": diff,
    }


def entry_exists(data, filename, password, entry_name):
    """
    Checks if an entry exists.
    """
    from pykeepass import PyKeePass

    kp = PyKeePass(filename, password)

    # Get the PyKeePass group object of the parent.
    parent = data["parent"]
    if parent is None:
        parent = kp.root_group
    else:
        parent = kp.find_groups_by_name(parent, first=True)

    # Check if the entry exists.
    entry = kp.find_entries(title=entry_name, group=parent, first=True)
    entry_present = entry is not None

    return kp, entry_present, parent, entry


def update_entry(data, entry, check_mode_on):
    """
    Checks if there are differences between the
    data dict and the data stored in the entry.

    returns: Boolean describing if changes are present.
    """
    entry_changed = False

    if data["username"] != entry.username:
        entry_changed = True
        if not check_mode_on:
            entry.username = data["username"]

    if data["password"] != entry.password and data["update_password"]:
        entry_changed = True
        if not check_mode_on:
            entry.password = data["password"]

    if data["url"] != entry.url:
        entry_changed = True
        if not check_mode_on:
            entry.url = data["url"]

    if data["notes"] != entry.notes:
        entry_changed = True
        if not check_mode_on:
            entry.notes = data["notes"]

    if data["tags"] != entry.tags:
        entry_changed = True
        if not check_mode_on:
            entry.tags = data["tags"]

    # if data["expiry_time"] != entry.expiry_time:
    #     entry_changed = True
    #     if not check_mode_on:
    #         entry.expiry_time = data["expiry_time"]

    if data["icon"] != entry.icon:
        entry_changed = True
        if not check_mode_on:
            entry.icon = data["icon"]

    return entry_changed


def entry_present(data, check_mode_on):
    """
    Ensures an entry is present.
    """
    entry_name = data["title"]
    filename = data["db_file"]
    password = data["db_password"]
    kp, entry_present, parent, entry = entry_exists(
        data, filename, password, entry_name
    )

    diff = {
        "before_state": "present" if entry_present else "absent",
        "after_state": "present",
        "before_title": entry.title if entry_present else None,
        "after_title": data["title"],
        "before_parent": entry.parentgroup.name if entry_present else None,
        "after_parent": data["parent"],
        "before_username": entry.username if entry_present else None,
        "after_username": data["username"],
        "before_password": entry.password if entry_present else None,
        "after_password": entry.password
        if entry_present and not data["update_password"]
        else data["password"],
        "before_url": entry.url if entry_present else None,
        "after_url": data["url"],
        "before_notes": entry.notes if entry_present else None,
        "after_notes": data["notes"],
        "before_tags": entry.tags if entry_present else None,
        "after_tags": data["tags"],
        "before_expiry_time": entry.expiry_time if entry_present else None,
        "after_expiry_time": data["expiry_time"],
        "before_icon": entry.icon if entry_present else None,
        "after_icon": data["icon"],
    }
    entry_changed = False
    # Überprüfen, ob mindestens ein Wert anders ist, falls
    # es den Entry schon gibt.
    if entry_present:
        entry_changed = update_entry(data, entry, check_mode_on)

        if entry_changed and not check_mode_on:
            kp.save()

    # The entry needs to be created if
    # the entry wasn't present at the beginning.
    if not entry_present and not check_mode_on:
        kp.add_entry(
            destination_group=parent,
            title=entry_name,
            username=data["username"],
            password=data["password"],
            url=data["url"],
            notes=data["notes"],
            tags=data["tags"],
            expiry_time=data["expiry_time"],
            icon=data["icon"],
        )
        kp.save()

    return {
        "changed": entry_changed or not entry_present,
        "diff": diff,
    }


def entry_absent(data, check_mode_on):
    """
    Checks if an entry is absent.
    """
    entry_name = data["title"]
    filename = data["db_file"]
    password = data["db_password"]
    kp, entry_present, _, entry = entry_exists(data, filename, password, entry_name)

    diff = {
        "before_state": "present" if entry_present else "absent",
        "after_state": "absent",
        "before_title": entry.title if entry_present else None,
        "after_title": None,
        "before_parent": entry.parentgroup.name if entry_present else None,
        "after_parent": None,
        "before_username": entry.username if entry_present else None,
        "after_username": None,
        "before_password": entry.password if entry_present else None,
        "after_password": None,
        "before_url": entry.url if entry_present else None,
        "after_url": None,
        "before_notes": entry.notes if entry_present else None,
        "after_notes": None,
        "before_tags": entry.tags if entry_present else None,
        "after_tags": None,
        "before_expiry_time": entry.expiry_time if entry_present else None,
        "after_expiry_time": None,
        "before_icon": entry.icon if entry_present else None,
        "after_icon": None,
    }

    # entry_present ist true, wenn der Eintrag vorhanden ist.
    if entry_present and not check_mode_on:
        kp.delete_entry(entry)
        kp.save()

    # entry_present ist für den state "absent" gleich wie changed.
    return {
        "changed": entry_present,
        "diff": diff,
    }


def main():
    fields = {
        # Shared between db, entry and group
        "db_file": {
            "type": "path",
            "required": True,
        },
        "type": {
            "choices": ["db", "group", "entry"],
            "type": "str",
            "required": True,
        },
        "db_password": {
            "type": "str",
            "required": True,
            "no_log": True,
        },
        "state": {
            "default": "present",
            "choices": ["present", "absent"],
            "type": "str",
        },
        # Shared between entry and group
        "title": {"type": "str", "required": False},
        "parent": {"type": "str", "required": False},
        # Only for entry
        "username": {"type": "str", "required": False},
        "password": {"type": "str", "required": False, "no_log": True},
        "update_password": {"default": True, "type": "bool", "required": False},
        "url": {"type": "str", "required": False},
        "tags": {"type": "str", "required": False},
        "expiry_time": {"type": "str", "required": False},
        # Shared between entry and group
        "notes": {"type": "str", "required": False},
        "icon": {"type": "str", "required": False},
    }

    requirements = [
        ("type", "entry", ["title"]),
        ("type", "entry", ["title", "username", "password"]),
    ]

    choice_map = {
        "db": {
            "present": database_present,
            "absent": database_absent,
        },
        "group": {
            "present": group_present,
            "absent": group_absent,
        },
        "entry": {
            "present": entry_present,
            "absent": entry_absent,
        },
    }

    module = AnsibleModule(
        argument_spec=fields,
        required_if=requirements,
        supports_check_mode=True,
    )

    result = choice_map[module.params["type"]].get(module.params["state"])(
        module.params, module.check_mode
    )

    module.exit_json(changed=result["changed"], diff=result["diff"])


if __name__ == "__main__":
    main()
