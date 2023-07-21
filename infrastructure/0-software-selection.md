# Software Selection

This section shows the software used on the platform and lists some alternatives that could be used as well (though they have not been tested).

Following list of types of software is needed:
- Router Software
- Virtualizing Environment
- Source Code Management Tool (SCM)
- CICD / Pipeline Tool
- Operating System

## Router Software
For the routing software the open-source tool called [OPNSense](https://opnsense.org/) is used.
It is free to use and a widely used free routing and firewall software.

Other options are be pfSense and OpenWrt but OPNsense is preferred because of the more frequent security updates and
the better compatibility with x86 architecture platforms.

## Virtualizing Environment
As the virtualizing environment we use the [Proxmox VE](https://www.proxmox.com).
The minimum requirement per virtual machine (VM) depends on the software/tool that runs on the respective VM.
As a rule of thumb with the [V1](../hardware/README.md#version-1), one VM is assigned 3 Cores, 8 GB RAM and 40GB of disk space.

## Host OS
For the host OS on the virtual machines (VMs) [Ubuntu Server 22.04 LTS](https://releases.ubuntu.com/22.04/) is used.

## Source Code Management (SCM) Tool
As the SCM Tool we will use the [Gitlab CE](https://docs.gitlab.com/omnibus/installation/) Edition.
It is installed natively since we use VMs for virtualization and encapsulation.

There are other options like [Github](https://github.com/), [Bitbucket](https://bitbucket.org/),
[Apache Subversion](https://subversion.apache.org/), etc., but Gitlab is open-source and very easy to self-host

## CICD / Pipeline Tool
For the CI/CD Pipeline tool the commonly used [Jenkins](https://www.jenkins.io/doc/book/installing/linux/) is used.
It is also installed natively since we use VMs for virtualization and encapsulation.

There are other options like [Travis CI](https://www.travis-ci.com/), [Bamboo](https://www.atlassian.com/software/bamboo),
[CircleCI](https://circleci.com/), etc., but Jenkins is open-source and very easy to self-host as well,
so we go with that as the main tool.

As a second option a VM with [Gitlab CI](https://docs.gitlab.com/runner/install/docker.html) is set up as well.
This integrates nicely with Gitlab and is also easy to self-host, but doesn't have the flexibility like Jenkins.