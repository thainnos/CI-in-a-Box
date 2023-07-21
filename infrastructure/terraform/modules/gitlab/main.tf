resource "proxmox_vm_qemu" "gitlab" {
    name = "gitlab${var.hostname_suffix}"
    target_node = var.node
    clone = "ubuntu-cloudinit-template"
    agent = 1
    os_type = "cloud-init"
    cores = 4
    sockets = 1
    cpu = "host"
    memory = "8192"
    scsihw = "virtio-scsi-pci"
    bootdisk = "scsi0"
    disk {
        slot = 0
        size = "50G"
        type = "scsi"
        storage = "local-lvm"
        iothread = 1
    }
    
    network {
        model = "virtio"
        bridge = "vmbr0"
    }

    # Not sure exactly what this is for. something about 
    # ignoring network changes during the life of the VM.
    lifecycle {
        ignore_changes = [
        network,
        ]
    }

    # Cloud-init config
    ipconfig0 = "ip=${var.ipaddr},gw=${var.gateway}"
    sshkeys = var.ssh_key

    # Run the bootstrapping automation
    provisioner "local-exec" {
      command = "ansible-playbook -i '${self.default_ipv4_address},' playbooks/fresh_vm/main.yml"
      working_dir = "../../ansible"
    }

    # Remove SSH Fingerprint
    provisioner "local-exec" {
      command = "ssh-keygen -f '/home/antonio/.ssh/known_hosts' -R '${self.default_ipv4_address}'"
      when = destroy
    }
}