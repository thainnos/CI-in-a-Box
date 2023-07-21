import yaml
import ipaddress
import argparse


def print_group_suffix(ip_address: ipaddress.IPv4Address, inventory_file_contents: str):
    """Prints the group suffix from a inventory file as string.

    Args:
        ip_address (ipaddress.IPv4Address): The ip adress for which the group suffix should be found.
        inventory_file_contents (str): The contents of the inventory file as a string.
    """
    ip_addr_network = ipaddress.ip_network(ip_address.compressed + "/24", False)
    data = yaml.load(inventory_file_contents, Loader=yaml.Loader)
    server_groups: dict = data["all"]["children"]["server"]["children"]

    for group in server_groups.keys():
        # The path when leaving out children to this group is:
        # all > server > * > proxmox > hosts
        group_proxmox_server: dict = server_groups[group]["children"]["proxmox"][
            "hosts"
        ]
        proxmox_ip_addr_with_cidr: str = list(group_proxmox_server.values())[0][
            "ip_addr"
        ]
        proxmox_ip_addr = list(proxmox_ip_addr_with_cidr.split("/"))[0]

        proxmox_ip_addr = ipaddress.ip_address(proxmox_ip_addr)
        if proxmox_ip_addr not in ip_addr_network:
            continue

        suffix = server_groups[group]["vars"]["suffix"]
        print(suffix)
        break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the server-* group of a host by it's ip address and print the group suffix."
    )
    parser.add_argument(
        "ip_address",
        type=str,
        help="the ip address of the host (e.g. '172.16.1.10').",
    )
    args = parser.parse_args()

    ip_addr = ipaddress.ip_address(args.ip_address)

    try:
        with open("../../../inventory.yml") as file:
            text = file.read()
    except FileNotFoundError:
        pass

    print_group_suffix(ip_addr, text)
