# Software & Infrastructure

In this directory is the software selection and infrastructure automation for project.
The setup should be done after the assembly of the [hardware](../hardware/README.md) and
before importing the [examples](../examples/README.md).

The order of the instruction files is as follows:
- [0-software-selection](0-software-selection.md)
- [1-user-guide](1-user-guide.md)
- [2-additional-info](2-additional-info.md)

## Software Selection
The [software selection](0-software-selection.md) shows which software is used for the infrastructure and what alternatives are available.

## What does the automation do?
The automation configures an OPNsense router and any number of Proxmox servers for use with the platform.

- Configures the router's LAN network to the 172.16.0.0/12 network.
- Creates a VPN to allow connection to the router LAN network from the router WAN network.
- Creates a self-signed Certificate Authority.
- Configures an arbitrary number of Proxmox Servers so that VMs can be created automatically on the Proxmox Servers.
- Creates VMs on the Proxmox servers based on the configuration.
- Configures the VMs as Gitlab Server, Jenkins Server, Gitlab Runner or Jenkins Agent based on the configuration.
- Associates the Jenkins Servers with the corresponding Jenkins Agents and the Gitlab Servers with the corresponding Gitlab Runners.
- Creates users for the VPN.
- Creates users for the Gitlab Server web interfaces.
- Creates users for the Jenkins Server web interfaces.
- Stores all created users in a kdbx password database.
- Configures the DNS of the router so that all Proxmox, Gitlab and Jenkins servers are locally accessible via one URL.
- Creates certificates with the self-signed Certificate Authority and adds them to all Proxmox, Gitlab and Jenkins servers and the router itself.

## Components of the automation

The automation can be divided into two parts.
One is the configuration automation, which is done using Ansible, and the other is the deployment automation,
which is done using Terraform. The automation can be configured using Ansible inventory files.

The Ansible automation can be found in the [ansible](./ansible) directory and the Terraform automation in the [terraform](./terraform) directory.

## Using the automation

The [user guide](./1-user-guide.md) contains a user guide. It contains instructions for:
- Installing the dependencies of the automation
- Setting up Proxmox
- Setting up OPNsense
- Configuring the automation
- The execution of the automation

## What's next?
Once the infrastructure has been set up, a good idea for the next step is to import the [examples](../examples/README.md).