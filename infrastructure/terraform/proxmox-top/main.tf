#
# Gitlab VMs
#

module "gitlab-top" {
  source = "../modules/gitlab"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  ipaddr = "192.168.0.111"
  gateway = var.gateway
  node = var.node
}

#
# Runner VMs
#
module "runner-top" {
  source = "../modules/runner"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  gateway = var.gateway
  node = var.node
  runner_ips = {
      "1" = "192.168.0.113"
    }
}

#
# Jenkins VMs
#
module "jenkins-top" {
  source = "../modules/jenkins"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  ipaddr = "192.168.0.111"
  gateway = var.gateway
  node = var.node
}

#
# Agent VMs
#
module "agent-top" {
  source = "../modules/agent"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  gateway = var.gateway
  node = var.node
  agent_ips = {
      "1" = "192.168.0.114"
    }
}
