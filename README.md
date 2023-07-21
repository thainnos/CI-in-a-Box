# CI in a Box Master Repo

This is the working repo and drafting repo for the publishing on Github.

Welcome to the CI-in-a-Box project: A platform as a playground for testing CI pipelines with embedded devices.

The idea behind this project is to provide a platform for the development of CI/CD pipelines,
integrate embedded devices into pipelines, and be used for demonstration purposes.
It should enable learning, exploration and flexible development of pipelines without
interfering with existing infrastructures.
Whether new build environments need to be created, Docker environments set up, templates developed,
tested/evaluated remotely, or if you just want to gain experience with pipelines,
this platform can do it all.

The platform comes with Gitlab as the source code management (SCM) tool and Jenkins as the CI/CD tool.
Both instances, as well as VMs prepared for Jenkins agents and Gitlab runners, are virtualized using Proxmox on the physical servers.
Two servers were chosen to allow the instances to be separated on separate nodes. This allows for
communication over a physical network connection.
Edge devices and a selection of embedded devices have been added to learn and test their integration into the pipelines.
A managed Layer 2+ switch is added to enable VLAN testing or specific network ideas.
A router running OPNsense routing software is added to separate and remove the need for a host network.
This helps to manage the platform by adding local domain names for all instances,
correct network segmentation of the different VMs, VPN access from a potential WAN network,
using certificates for secure internal communications and providing proper DHCP support.
The whole platform is built into a Thomann rack, so it is mobile and can be moved.
All of the internal infrastructure is automated and provided as an easy install and setup so you can build this platform,
set up the infrastructure via the script and then use it as you wish.
If something goes wrong, the installation/setup can be repeated to reset the platform to its default state.
(Note: This will also remove any changes made since the initial setup).

A detailed explanation of the individual parts is divided into the individual READMEs in the folders.

## Repository overview
Most of the explanatory documentation is divided into the READMEs of the individual folders depending on the topic.  
Below is an overview of the repository:

```bash
├── README.md
├── documents
├── examples
│   ├── apache-server
│   └── apache-server-secure
├── hardware
├── infrastructure
└── software
```

## Buildup
Please refer to the [Hardware README](hardware/README.md) for information about how to build up the platform.
Also there is more information about the hardware decision and which version of the platform might fit best.

In general the build-up of the platform is fairly easy: just screwing everything together and plugging everything in.

## Setup
Please refer to the [Infrastructure README](infrastructure/README.md) for information on how to setup the platforms infrastructure.
After the infrastructure setup the platform is usable and ready to go.

Additional optional steps are including and importing the [examples](examples/README.md).
Please refer to the [Examples README](examples/README.md) for more information about the examples.

## Usage
Once set up, the platform is ready to use.
From here you have the flexibility to do what you want.
The [examples](examples/README.md) are usually a good place to start and get used to the environment and infrastructure.
(Note: Additional hardware may be required depending on the example).

Since the main intention is to provide a playing field for your own ideas,
I suggest you start by setting up your own repository with the project you need,
and then play around with setting up pipelines.

## ToDo
This platform is currently functional and fully usable.
However, there are some features that could be improved and some features that are missing.
 - Move the infrastructure from Ansible + Terraform to a better automation framework
 - Automate Group setup and adding user to the group
 - Automate the optional importing of the examples
 - Add a second automation example for split server setup
 - Add Edge Nodes to automatically get a static IP and added as agents

## Contribute
Please refer to the [contributing guide](CONTRIBUTING.md) for information on how to contribute to this project.

We accept various types of contributions: examples, infrastructure changes, documentation updates, hardware setups, etc.
We are always interested in including examples of real-world use of the platform.

## About
This project was developed within the [HITSSSE](https://www.hitssse.de/) research project.

### Contributors
| Name             | Contributor |
| ---------------- | ----------- |
| Philipp Schloyer | Maintainer  |
| Fabian Klemm     | Developer   |