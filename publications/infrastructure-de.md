# CIinaBox Infrastruktur

In diesem Verzeichnis ist die Infrastruktur Automatisierung für CIinaBox. Die Infrastruktur Automatisierung konfiguriert einen OPNsense Router und beliebig viele Proxmox Server für die Verwendung bei CIinaBox.

## Was macht die Automatisierung?

- Sie konfiguriert das LAN Netzwerk des Routers zum 172.16.0.0/12 Netzwerk.
- Sie erstellt einen VPN damit eine Verbindung zum Router LAN Netzwerk aus dem Router WAN Netzwerk möglich ist.
- Sie erstellt eine self-signed Certificate Authority.
- Sie konfiguriert eine beliebige Anzahl an Proxmox Servern so dass automatisch VMs auf den Proxmox Servern erstellt werden können.
- Sie erstellt basierend auf der Konfiguration VMs auf den Proxmox Servern.
- Sie konfiguriert die VMs basierend auf der Konfiguration als Gitlab Server, Jenkins Server, Gitlab Runner oder Jenkins Agent.
- Sie verknüpft die Jenkins Server mit den zugehörigen Jenkins Agents und die Gitlab Server mit den zugehörigen Gitlab Runnern.
- Sie erstellt Benutzer für den VPN.
- Sie erstellt Benutzer für die Gitlab Server Webinterfaces.
- Sie erstellt Benutzer für die Jenkins Server Webinterfaces.
- Sie speichert alle erstellten Benutzer in einer kdbx Passwort Datenbank.
- Sie konfiguriert den DNS des Routers so, dass alle Proxmox, Gitlab und Jenkins Server über eine URL lokal erreichbar sind.
- Sie erstellt mit der self-signed Certificate Authority Zertifikate und fügt diese zu allen Proxmox, Gitlab und Jenkins Servern und dem Router selbst hinzu.

## Bestandteile der Automatisierung

Die Automatisierung ist in zwei Teile zerlegbar. Einerseits die Konfigurationsautomatisierung, welche mithilfe von Ansible durchgeführt wird und andererseits die Provisioning Automatisierung, welche mithilfe von Terraform ausgeführt wird. Konfiguriert werden kann die Automatisierung durch Ansible inventory Dateien.

Die ansible Automatisierung ist im Verzeichnis [ansible](./ansible) und die Terraform Automatisierung im Verzeichnis [terraform](./terraform) auffindbar.

## Verwenden der Automatisierung

Die Datei [Bedienungsanleitung.md](./Bedienungsanleitung.md) enthält eine Bedienungsanleitung. Sie enthält Anleitungen für:
- die Installation der Abhängigkeiten der Automatisierung
- das Aufsetzen von Proxmox
- das Aufsetzen von OPNsense
- die Konfiguration der Automatisierung
- die Ausführung der Automatisierung
