# Proxmox Variables
variable "ssh_key" {
  default = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDL5QUAy1zP0jja1C+QTCoEri7Hn8RD2z174Uaek9GHPbHYpZJHltG+BZ+M5zfsipkl7AKjuNSsIM2mJ4vorRcz6HHnkyg3PPHx4XtKwe3a41iPQon2xQtRAMhm50n2Joq4AFqDymAP+TqiAOcBiadesnR9nzEy4gh9tPs+aLPqv0/+Yq/Ucw5ooJ2i9MMwYvWhKVeb+dW/XrkozEafQdRTqzJvBsHePRSBxfE4ZKf4y08j3MsS7ynfvFcGboQ+8PZWhrwK44tsk6IRQNI6E1mCJVjQV1/BhITMbSeELrV0JorWk180kZy7GkXv5oa8hiY9HD3UdRTBO0kMccF+tuKhWH/t2fU9+XfON+b4NiCmzMIqfjQciFQmth00kN0pmEKSr2HtC9+gZh6CmMy6xpTXFWyqM5rJ4PHhXAyD0qQX6BhItqSkx5O8F3T7MkwO82FixKNXUNtuNAkIeACn6xcUQcg6Qt9GPug7JrXV+HSANZO4e3TgE6FLU31lWCoZtU= antonio@xlab"
}

variable "suffix" {
  default = "-top"
}

variable "proxmox_host" {
  default = "192.168.0.17"
}

variable "gateway" {
  default = "192.168.0.1"
}

variable "node" {
  default = "proxmox-top"
}

variable "proxmox_user" {
  # Set here or e.g. in secrets.tfvars and include the file with
  # -var-file=secrets.tfvars
  default = {
    token_id = ""
    token_secret = ""
  }
}

