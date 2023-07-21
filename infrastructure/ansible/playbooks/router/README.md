# Router

This playbook can be used to configure a fresh OPNsense installation for usage in the CIinaBox Automation.

The playbook does the following:
- It configures the domain of the router to "demo".
- It adds a user default to the router.
- It configures the lan router ip address to be 172.16.0.1.
- It configures the lan dhcp range from 172.16.3.1 to 172.16.3.254.
- It creates a CA (certificate authority) for the CIinaBox automation and stores it on the router.
- It updates the router website SSL certificate with a SSL certificate signed by CIinaBox CA.
- It creates a VPN SSL certificate signed by the CIinaBox CA.

To do this the /conf/config.xml file is downloaded from the OPNsense router, updated and reuploaded. To activate the changes the router gets rebooted.

## Requirements

n/a

## Variables

Following are the variables that should be set in the inventory for the group proxmox or a parent group. Optional variables are marked by the text "(optional)." at the beginning of their description.

- db_location:
  The location of a keepassxc database.
- db_password:
  The password of the keepassxc database at db_location.
- ssh_public_key:
  The public ssh key of the user of the automation.

## Dependencies

n/a

## Structure of the playbook

### Directory overview

Following is a short overview over the contents of the playbooks:

```bash
.
├── main.yml
├── README.md
├── script
│   ├── configure_certificates.py
│   ├── configure_general.py
│   ├── configure_lan_interface.py
│   ├── cryptography_helpers.py
│   └── xml_helpers.py

```

### A short introduction to the files

- The main.yml File contains the actual playbook.
- The script configure_general configures users and the domain of the router.
- The script configure_lan_interfaces configures the lan interface (subnet, ip address and dhcp).
- The script configure_certificates configures the certificates and the CIinaBox CA.

## License

n/a