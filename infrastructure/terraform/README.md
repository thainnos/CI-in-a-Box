# Terraform

Dieses Verzeichnis enthält die Bestandteile der Terraform Automatisierung. Das Verzeichnis ist untergliederbar in die folgenden Teile:

- [module](./module): Abstraktionen für die Erstellung von Gitlab, Jenkins, Agent und Runner VMs, welche innerhalb von der Terraform Automatisierung verwendet werden können.
- proxmox-*: Die Terraform Automatisierung für die einzelnen Proxmox Server. Bei der Konfigurationsautomatisierung von Proxmox Servern (die Konfigurationsautomatisierung hierfür befindet sich im playbook [proxmox](../ansible/playbooks/proxmox)) wird für jeden Proxmox Server hier ein Verzeichnis erstellt. Innerhalb dieses Verzeichnisses wird die Konfiguration für die jeweilige Terraform Automatisierung getemplated.
- [example](./example): Ein Beispiel wie eine Terraform Automatisierung für einen Proxmox Server aussieht.