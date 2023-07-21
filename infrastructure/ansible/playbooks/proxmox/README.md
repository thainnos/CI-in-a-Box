# Proxmox

This playbook can be used to configure a fresh Proxmox VE 7.2 installation for usage in the CIinaBox Automation.

The playbook does the following:
- It configures the ip address and hostname of the server.
- It configures sshd to only allow public/private key access.
- It configures (and stores) the root password.
- It configures apt to use the no-subscription repository.
- It creates a cloud-init template for VMs.
- It creates (and stores) an api user.
- It creates, initializes and runs a terraform automation for creating VMs.

## Requirements

n/a

## Variables

Following are the variables that should be set in the inventory for the group proxmox or a parent group. Optional variables are marked by the text "(optional)." at the beginning of their description.

- db_location
    The location of a keepassxc database.
- db_password
    The password of the keepassxc database at db_location.
- ssh_public_key
    The public ssh key of the user of the automation.
- gateway
    The gateway of the proxmox server (the ip address of the router the proxmox server is connected to).
- subnet
    The subnet of the proxmox server.
- ip_addr
    The ip address of the proxmox server.
- hostname
    The to be set hostname of the proxmox server.
- server_postfix
    (optional). The postfix of the proxmox server hostname, e.g. for the hostname "proxmox" and the server_postfix "top" the hostname will be "proxmox-top".

## Dependencies

n/a

## Structure of the playbook

### Directory overview

Following is a short overview over the contents of the playbooks:

```bash
.
├── main.yml
├── README.md
├── scripts
│   └── generate-cloud-init-img.sh
├── tasks
│   ├── configure_api_user.yml
│   ├── configure_network.yml
│   ├── configure_repo.yml
│   ├── configure_root_user.yml
│   ├── configure_ssh.yml
│   ├── configure_vm_template.yml
│   ├── fail_conditions.yml
│   ├── save_user.yml
│   └── terraform.yml
└── templates
    ├── hostname.j2
    ├── main.tf.j2
    ├── providers.tf.j2
    ├── secrets.tfvars.j2
    └── vars.tf.j2
```

### A short introduction to the files

- The main.yml File contains the actual playbook. 
- The generate-cloud-init-img.sh creates a proxmox VM template based on a ubuntu 20.04 image and preconfigures a ansible user.
- The files in ./tasks are included by the main.yml. They are in their own files to guarantee a clear overview when opening the main.yml.
- The files in ./templates are templates that ansible can fill with the values of variables.

## License

n/a