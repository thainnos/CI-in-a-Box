#!/bin/bash

#
# libguestfs-tools needs to be installed for
# configuring the image
#

# download cloud image
wget http://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img

# customize image
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --update
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --install qemu-guest-agent
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --run-command 'useradd --shell /bin/bash ansible'
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --run-command 'mkdir -p /home/ansible/.ssh'
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --ssh-inject ansible:string:"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDL5QUAy1zP0jja1C+QTCoEri7Hn8RD2z174Uaek9GHPbHYpZJHltG+BZ+M5zfsipkl7AKjuNSsIM2mJ4vorRcz6HHnkyg3PPHx4XtKwe3a41iPQon2xQtRAMhm50n2Joq4AFqDymAP+TqiAOcBiadesnR9nzEy4gh9tPs+aLPqv0/+Yq/Ucw5ooJ2i9MMwYvWhKVeb+dW/XrkozEafQdRTqzJvBsHePRSBxfE4ZKf4y08j3MsS7ynfvFcGboQ+8PZWhrwK44tsk6IRQNI6E1mCJVjQV1/BhITMbSeELrV0JorWk180kZy7GkXv5oa8hiY9HD3UdRTBO0kMccF+tuKhWH/t2fU9+XfON+b4NiCmzMIqfjQciFQmth00kN0pmEKSr2HtC9+gZh6CmMy6xpTXFWyqM5rJ4PHhXAyD0qQX6BhItqSkx5O8F3T7MkwO82FixKNXUNtuNAkIeACn6xcUQcg6Qt9GPug7JrXV+HSANZO4e3TgE6FLU31lWCoZtU= antonio@xlab"
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --run-command 'chown -R ansible:ansible /home/ansible'
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --touch /etc/sudoers.d/ansible
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --write /etc/sudoers.d/ansible:"ansible ALL=(ALL) NOPASSWD: ALL"
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --run-command 'chmod 0440 /etc/sudoers.d/ansible'
virt-customize -a ubuntu-20.04-server-cloudimg-amd64.img --run-command 'chown root:root /etc/sudoers.d/ansible'
  
# create vm
qm create 9000 \
  --name "ubuntu-cloudinit-template" --ostype l26 \
  --cpu cputype=host --cores 2 --sockets 1 \
  --memory 4096 \
  --net0 virtio,bridge=vmbr0

qm importdisk 9000 \
  ubuntu-20.04-server-cloudimg-amd64.img local-lvm

qm set 9000 \
  --scsihw virtio-scsi-pci \
  --scsi0 local-lvm:vm-9000-disk-0

qm set 9000 --boot c --bootdisk scsi0
qm set 9000 --ide2 local-lvm:cloudinit

qm set 9000 --serial0 socket --vga serial0
qm set 9000 --agent enabled=1

# create template
qm template 9000

# remove image
rm ubuntu-20.04-server-cloudimg-amd64.img
