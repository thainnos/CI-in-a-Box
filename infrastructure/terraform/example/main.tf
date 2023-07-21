#
# Gitlab VMs
#

module "gitlab-top" {
  source = "../modules/gitlab"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  ipaddr = "172.16.1.10/12"
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
      "0" = "172.16.1.30/12"
    }
}

#
# Jenkins VMs
#
module "jenkins-top" {
  source = "../modules/jenkins"
  ssh_key = var.ssh_key
  hostname_suffix = var.suffix
  ipaddr = "172.16.1.20/12"
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
      "0" = "172.16.1.40/12"
    }
}
