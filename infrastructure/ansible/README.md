# Ansible

Dieses Verzeichnis enthält die Bestandteile der Ansible Konfigurationsautomatisierung.
Das Verzeichnis ist untergliederbar in die folgenden Teile:

- [playbooks](./playbooks): Skripte, die von ansible ausgeführt werden können.
- [roles](./roles): Wiederholbare Blöcke, welche in Playbooks verwendet werden können.
- [library](./library): Eigens entwickelte Module, welche in ansible verwendet werden können.

Mithilfe der Datei [ansible.cfg](./ansible.cfg) können ansible Konfigurationsparameter wie z.B. der Pfad zu eigenen Modulen gesetzt werden.

Die Dateien [ciinabox.yml](./ciinabox.yml), [ciinabox_without_router.yml](./ciinabox_without_router.yml), [ciinabox_without_proxmox.yml](./ciinabox_without_proxmox.yml) dienen dazu Playbooks nacheinander auszuführen.
