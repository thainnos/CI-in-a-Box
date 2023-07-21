<!-- omit in toc -->
# User Guide

<!-- omit in toc -->
## Table of contents
- [Structure of the Manual](#structure-of-the-manual)
- [Install dependencies](#install-dependencies)
  - [Pip](#pip)
  - [Ansible](#ansible)
  - [Terraform](#terraform)
  - [Python libraries](#python-libraries)
- [Configuration of the automation](#configuration-of-the-automation)
  - [General settings](#general-settings)
- [Router](#router)
  - [Setting up an OPNsense router](#setting-up-an-opnsense-router)
  - [Configure router automation](#configure-router-automation)
  - [Run Router Automation](#run-router-automation)
- [Proxmox Server](#proxmox-server)
  - [Setting up a Proxmox server](#setting-up-a-proxmox-server)
  - [Configuring Proxmox Server Automation](#configuring-proxmox-server-automation)
  - [Execute Proxmox Server Automation](#execute-proxmox-server-automation)
- [Set up Self-signed CA (optional)](#set-up-self-signed-ca-optional)
  - [Add to Firefox](#add-to-firefox)
  - [Add to Chrome](#add-to-chrome)
  - [Add to system certificates](#add-to-system-certificates)
  - [Remove from Firefox](#remove-from-firefox)
  - [Remove from Chrome](#remove-from-chrome)
  - [Remove from system certificates](#remove-from-system-certificates)
- [Troubleshooting](#troubleshooting)
  - [REMOTE HOST IDENTIFICATION HAS CHANGED](#remote-host-identification-has-changed)

## Structure of the Manual

The guide consists of the following four parts:
- The installation of the dependencies for the automation
- The general configuration of the automation 
- The setup and (automatic) configuration of the router
- The setup and (automatic) configuration of the Proxmox servers

No knowledge of configuration automation using Ansible and infrastructure automation using Terraform is required to follow the guide.

## Install dependencies

To use the infrastructure automation, the following programs and libraries need to be added to the system:

- pip
- ansible
- terraform
- The libraries in requirements.txt

The following are the installation instructions for the programs and libraries.

### Pip

To install Pip, you can follow the [installation instructions](https://pip.pypa.io/en/stable/installation/) on the Python Packaging Authority website.

### Ansible

To install Ansible, follow the [installation instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) on Ansible's website.

### Terraform

To install Terraform, you can follow the [installation instructions](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) on hashicorp's website.

### Python libraries

The following command must be executed in the top-level directory of the CIinaBox infrastructure automation and will install the Python libraries needed for the program execution.

```bash
pip install -r requirements.txt
```

## Configuration of the automation

The infrastructure created by the automation can be configured using the inventory.yml file. An example of an inventory.yml file is in the example_inventory.yml file. On the Ansible website there is a good [quick guide](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) to inventories in ansible. 

The most important things are summarised briefly:
- Ansible inventories consist of groups.
- Each group has children (subgroups), vars (variables) and hosts (IP addresses or URLs of servers), all of which must have no entries.
- The variable precedence is host variables before group variables before parent group variables.

To use the CIinaBox infrastructure automation, either copy the example_inventory.yml file and modify the copy below, or modify the example_inventory.yml file directly.

### General settings

The following variables in the all group control basic aspects and should be configured before running the automation for the first time:
- db_location: 
    The path to the KeepassXC database from the ./ansible/playbooks/ directory.
- db_password:
    The password for the KeepassXC database.
- ssh_public_key:
    The ssh public key of the user.
- user_list:
    A list with the names of all users for which:
    - a VPN configuration is to be created
    - a Gitlab user is to be created
    - a Jenkins user should be created

## Router

### Setting up an OPNsense router

To set up an OPNsense router, the following steps must be performed:

- Download an [OPNsense iso](https://opnsense.org/download/) with architecture amd64 and type dvd.
- Create a bootable USB stick using balenaEtcher according to the following [installation instructions](https://linuxhint.com/create_bootable_linux_usb_flash_drive/).
- Connect the LAN cable to the internal network of the router to the router.
- Connect the LAN cable to the external network of the router to the router.
- Connect the USB stick to the router.
- Start the router.
- Wait until a login prompt is displayed.
- Check whether the line beginning with "WAN" shows "0.0.0.0/0" at the end of the line. If this is the case, the LAN cables for the network must be connected the other way round. After changing the connection order of the LAN cables, press the Enter key once.
- At the prompt, enter the user name "installer" and the password "opnsense".
- Select the correct keyboard layout.
- Select the installation option **Install (UFS)**.
- Select the correct hard disk.
- Select the **Root Password** option and set a password. The same password must be selected later for all Proxmox servers.	
- Select the option **Complete Install**.
- As soon as the router reboots, remove the installation medium.

The following steps must now be carried out so that the router can be configured automatically via ssh:

- The web interface of the router must be opened in a browser. To do this, enter the LAN IP address of the router in a browser. It is possible that a warning will be displayed after loading the web page. If a warning is displayed, click on the *Advanced* button and then click on *Continue to* for Chrome, or *Accept risk and continue* for Firefox.
- In the web interface, the user name root and the previously selected password must now be entered.
- Wait until the installation wizard starts. As soon as the wizard has loaded, click on the OPNsense logo in the upper left corner. It is not necessary to run the wizard as the automation will take care of the configuration later.
- In the search bar, the term "Administration" must be entered and the option *System / Settings / Administration* displayed below it must be selected.
- Now scroll down to the item *Secure Shell*. Check the boxes to the right of the entries *Secure Shell Server*, *Root Login* and *Authentication Method*.
- Scroll down to the bottom of the page and click on *Save* to save the changes.

This completes the setup and preparation of the OPNsense router for automation.

### Configure router automation

In order for the router to be configured by the automation, its current IP address must be added as a hosts entry to the router group in the selected inventory file. The original hosts entry for router can be kept or deleted.

If the current IP address of the router is 192.168.1.1, the first 6 lines of the inventory file should look like this:

```yaml
all:
  children:
    router:
      hosts:
        192.168.1.1:
    server:
```

### Run Router Automation

To start router automation, run the following command from the ansible directory, replacing {inventory_file} with the filename of the inventory you are creating:

```bash
ansible-playbook -i ../{inventory_file} -k router.yml
```

After confirming the command, a prompt appears in which the password for the root user of the OPNsense router must be entered.

**Caution**

When the router automation has run for the first time, the IP address of the router has been changed. Therefore, the following things must be done **after** the automation:
- The router's host entry in the inventory file must be set to the IP address 172.16.0.1.
- A new IP address must be requested from the router for the user's computer. This is done by executing the following commands:
  ```bash
  sudo dhclient -r
  sudo dhclient
  ```

## Proxmox Server

### Setting up a Proxmox server

To set up a Proxmox server, the following steps must be performed:

- Downloading a Proxmox VE ISO from the [Proxmox Download Page](https://www.proxmox.com/de/downloads/category/iso-images-pve).
- Create a bootable USB stick using balenaEtcher according to the following [installation instructions](https://linuxhint.com/create_bootable_linux_usb_flash_drive/).
- Connect the Proxmox server to the internal network (LAN) of the router.
- Plug the USB stick into the server.
- Start the server.
- Select the option **Install Proxmox VE**.
- Accept the EULA.
- Select the correct hard disk for the installation.
- Set the correct time zone.
- Enter the same password for each Proxmox server and set a valid email address.
- Confirm the automatic IP address configuration.
- Confirm the installation.	
- When the server reboots, remove the installation media.

**Caution**

Any number of Proxmox servers can be set up for use in the CIinaBox. If several servers are to be used, however, the same password should be used for the root user of all servers when setting up the servers.

### Configuring Proxmox Server Automation

For each Proxmox server to be used, a yaml block must be added to the children of server as in the following example.

```yaml
        server-top:
          children:
            proxmox:
              hosts:
                172.16.1.2: # Future IP address
                172.16.3.7: # Current IP address
                  ip_addr: "172.16.1.2/12"
            vms:
              children:
                gitlab:
                  hosts:
                    172.16.1.10:
                jenkins:
                  hosts:
                    172.16.1.20:
                runner:
                  hosts:
                    172.16.1.30:
                  vars:
                    # The ip/hostname of the runners gitlab server.
                    gitlab_instance: 172.16.1.10
                agent:
                  hosts:
                    172.16.1.40:
                  vars:
                    # The ip/hostname of the agents jenkins server.
                    jenkins_instance: 172.16.1.20
              vars:
                ansible_user: ansible
          vars:
            subnet: "172.16.0.0"
            suffix: "top"
```

After that, the following steps have to be performed for each Proxmox server:

1. set the *suffix*. The *suffix* after a hyphen is appended to the hostname of the Proxmox server and each of its VMs. For example, the hostname of the Proxmox instance in the yaml above would be proxmox-top and the hostname of the Jenkins instance would be jenkins-top. If no suffix is set, the hostname of the Proxmox instance is proxmox and the hostname of the Jenkins instance is jenkins. The line with the suffix variable must be removed to not set the suffix.
2. set the group name. The group name results from *server*, a *hyphen* and *suffix*. If no suffix is set, the group name is server.
Set the current Proxmox IP address. A host entry with the current IP address of the Proxmox server must be added to the Proxmox group of the server.
4. set the future Proxmox IP address. The future IP address of the Proxmox server must be within the 172.16.0.0/12 network. A host entry with the future IP address of the Proxmox server must be added to the Proxmox group of the server. 5. 
5. in addition, the **group variable** ip_addr of the Proxmox group must be set to the future IP address of the Proxmox server followed by */12*, i.e. for example: "172.16.1.2/12".
6. Set the VM IP addresses. For each subgroup of the vms group, 0 to any number of host IP addresses can be added within the 172.16.0.0/12 network. 7.
If hosts are added to the runner group, the variable gitlab_instance must be set for the group. Its content must be the IP address of a Gitlab instance in the network of the CIinaBox router. The variable gitlab_instance can be set on a group basis as well as individually for hosts. 8.
If hosts are added to the agent group, the variable jenkins_instance must be set for the group. Its content must be the IP address of a Jenkins instance in the network of the CIinaBox router. The variable jenkins_instance can be set on a group basis as well as individually for hosts.

### Execute Proxmox Server Automation

To start the router automation the following command must be executed in the ansible directory, replacing {inventory_file} with the filename of the created inventory:

```bash
ansible-playbook -i ../{inventory_file} -k ciinabox.yml
```

After confirming the command, a prompt appears in which the password for the root user of the Proxmox server must be entered.

## Set up Self-signed CA (optional)

During the execution of the automation a (self-signed) root certificate was created, which issues SSL certificates for all web servers. 
To prevent warnings about invalid certificates, this root certificate should be installed in the browser of every user of the CIinaBox demonstrator. In order for curl to work for local https URLs (which are used for git commands, for example), the root certificate must also be installed locally.

Adding the root certificate to the system certificates and to the browser certificates is optional. In the following, adding to a browser is described first and then adding to the system certificates.

### Add to Firefox 

The Firefox browser must be opened. 2.
In the address bar of the browser, enter "about:preferences" and confirm by pressing the Enter key. 3.
In the search bar, enter the word "certificates" (and possibly confirm by pressing the Enter key). 4.
The button "Show certificates" must be clicked. 5.
The tab "Certification authorities" must be selected by clicking on it. 6.
Click on the "Import" button below the table. 7.
In the newly opened window, navigate to the top directory of the infrastructure automation. 8.
If the file "ciinabox-ca.crt" is not displayed, the (drop-down) button at the bottom right must be clicked and then the option "All files" selected. 9.
The file "ciinabox-ca.crt" must now be selected and then the "Open" button at the top right must be clicked. 10.
In the newly opened window, check the option "Trust this CA to identify websites" and then click on "OK".

### Add to Chrome

The Chrome browser must be opened. 2.
2. in the address bar of the browser, "chrome://settings/certificates" must be entered. 3.
The tab "Certificate Authorities" must be clicked. 4.
Click on the button "Import". 5.
In the newly opened dialogue, change to the top directory of the infrastructure automation. 6.
If the file "ciinabox-ca.crt" is not displayed, all files must be selected from the (drop-down) button at the bottom right. 7.
The file "ciinabox-ca.crt" must be selected by clicking on it. 8.
Click on the "Open" button at the top right to add the certificate to the browser. 9.
In the new dialogue that appears, a tick must be placed in the option "Trust this certificate to identify websites". 10.
Click on the "Ok" button to add the certificate to the Chrome browser.

### Add to system certificates

1. install the package "ca-certificates" with the command  
    ```
    sudo apt install ca-certificates -y
    ```
2. open a terminal in the top-level directory of the infrastructure automation and execute the following command
    ```
    sudo cp ./ciinabox-ca.crt /usr/local/share/ca-certificates
    ```
Update the system certificates with the following command.
    ```
    sudo update-ca-certificates
    ```
### Remove from Firefox 

The Firefox browser must be opened. 2.
In the address bar of the browser, enter "about:preferences" and confirm by pressing the Enter key. 3.
In the search bar, enter the word "certificates" (and possibly confirm by pressing the Enter key). 4.
The button "Show certificates" must be clicked. 5.
The tab "Certification Authorities" must be selected by clicking on it. 6.
Find the entry "HSA_innos" in the field "Certificate name". 7.
Click on the entry "ciinabox-ca" below HSA_innos (if this is not visible, click on the arrow to the left of HSA_Innos). 8.
The button "Delete or withdraw trust..." must be clicked. 9.
Confirm the newly opened dialogue by clicking on "OK".

### Remove from Chrome 

The Chrome browser must be opened. 2.
In the address bar of the browser, enter "chrome://settings/certificates". 3.
The tab "Certificate Authorities" must be clicked. 4.
4. find the entry "org-HSA_innos" in the list and click on the arrow at the end of the entry line. 5. click on the three dots at the end of the entry line.
Click on the three dots at the end of the (now open) sub-entry "ciinabox-ca". 6.
Click on the "Delete" option in the drop-down menu. 7.
7. confirm the deletion by clicking on "Ok".

### Remove from system certificates

1. remove the certificate from the system ssl certificates with the command 
  ```bash
  sudo rm /etc/ssl/certs/ciinabox-ca.pem
  ```
  
2. remove the certificate from the local ca certificates with the command 
  ```
  sudo rm /usr/local/share/ca-certificates/ciinabox-ca.crt
  ```


## Troubleshooting

### REMOTE HOST IDENTIFICATION HAS CHANGED

**Reason for error**

The computer has stored an old SSH connection to a computer with an IP address used in the automation and recognizes that another computer has this IP address. For security reasons, the SSH connection is blocked.

**Troubleshooting**

- Find out the IP address that is causing the error. The IP address can be found in the error message.
- Execute the following command, replacing {{ username }} with the username of the user of the manual and {{ ip_address }} with the IP address found in the last step:
  ```bash
  ssh-keygen -f /home/{{ username }}/.ssh/known_hosts -R "{{ ip_address }}"
  ```
