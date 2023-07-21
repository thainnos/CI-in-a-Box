# CIinaBox Infrastruktur Bedienungsanleitung

## Inhaltsverzeíchnis
- [CIinaBox Infrastruktur Bedienungsanleitung](#ciinabox-infrastruktur-bedienungsanleitung)
  - [Inhaltsverzeíchnis](#inhaltsverzeíchnis)
  - [Aufbau der Anleitung](#aufbau-der-anleitung)
  - [Abhängigkeiten installieren](#abhängigkeiten-installieren)
    - [Pip](#pip)
    - [Ansible](#ansible)
    - [Terraform](#terraform)
    - [Python Bibliotheken](#python-bibliotheken)
  - [Konfiguration der Automatisierung](#konfiguration-der-automatisierung)
    - [Generelle Einstellungen](#generelle-einstellungen)
  - [Router](#router)
    - [OPNsense Router aufsetzen](#opnsense-router-aufsetzen)
    - [Router Automatisierung konfigurieren](#router-automatisierung-konfigurieren)
    - [Router Automatisierung ausführen](#router-automatisierung-ausführen)
  - [Proxmox Server](#proxmox-server)
    - [Proxmox Server aufsetzen](#proxmox-server-aufsetzen)
    - [Proxmox Server Automatisierung konfigurieren](#proxmox-server-automatisierung-konfigurieren)
    - [Proxmox Server Automatisierung ausführen](#proxmox-server-automatisierung-ausführen)
  - [Self-signed CA einrichten (optional)](#self-signed-ca-einrichten-optional)
    - [Zu Firefox hinzufügen](#zu-firefox-hinzufügen)
    - [ZU Chrome hinzufügen](#zu-chrome-hinzufügen)
    - [Zu den Systemzertifikaten hinzufügen](#zu-den-systemzertifikaten-hinzufügen)
    - [Von Firefox entfernen](#von-firefox-entfernen)
    - [Von Chrome entfernen](#von-chrome-entfernen)
    - [Von den Systemzertifikaten entfernen](#von-den-systemzertifikaten-entfernen)
  - [Fehlerbehebung](#fehlerbehebung)
    - [REMOTE HOST IDENTIFICATION HAS CHANGED](#remote-host-identification-has-changed)

## Aufbau der Anleitung

Die Anleitung besteht aus den folgenden vier Teilen:
- Die Installation der Abhängigkeiten für die Automatisierung
- Die generelle Konfiguration der Automatisierung 
- Das Aufsetzen und die (automatische) Konfiguration des Routers
- Das Aufsetzen und die (automatische) Konfiguration der Proxmox Server

Zum Folgen der Anleitung ist kein Wissen zur Konfigurationsautomatisierung mithilfe von Ansible und zur Infrastrukturautomatisierung mithilfe von Terraform benötigt.

## Abhängigkeiten installieren

Zur Verwendung der CIinaBox Infrastruktur Automatisierung müssen die folgenden Programme und Bibliotheken zum System hinzugefügt werden:

- pip
- ansible
- terraform
- Die Bibliotheken in requirements.txt

Folgend sind die Installationsanleitungen für die Programme und Bibliotheken.

### Pip

Zur Installation von Pip kann der [Installationsanleitung](https://pip.pypa.io/en/stable/installation/) auf der Webseite der Python Packaging Authority gefolgt werden.

### Ansible

Zur Installation von Ansible kann der [Installationsanleitung](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) auf ansibles Webseite gefolgt werden.

### Terraform

Zur Installation von Terraform kann der [Installationsanleitung](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) auf hashicorps Webseite gefolgt werden.

### Python Bibliotheken

Das folgende Kommando muss im obersten Verzeichnis der CIinaBox Infrastruktur Automatisierung ausgeführt werden und installiert die für die Programmausführung benötigten Python Bibliotheken.

```bash
pip install -r requirements.txt
```

## Konfiguration der Automatisierung

Die Infrastruktur welche durch die Automatisierung erzeugt wird, kann mithilfe der Datei inventory.yml konfiguriert werden. Ein Beispiel für eine inventory.yml Datei ist in der Datei example_inventory.yml. Auf der Ansible Webseite gibt es eine gute [Kurzanleitung](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) zu Inventories in ansible. 

Das Wichtigste kurz zusammengefasst:
- Ansible Inventories bestehen aus Gruppen.
- Jede Gruppe hat children (Untergruppen), vars (Variablen) und hosts (IP Adressen oder URLs von Servern), welche alle keine Einträge haben müssen.
- Die Variablen Präzedenz ist Host Variablen vor Gruppen Variablen vor Elterngruppen Variablen.

Um die CIinaBox Infrastruktur Automatisierung zu verwenden kann entweder die example_inventory.yml Datei kopiert werden und die Kopie im Folgenden angepasst werden oder die example_inventory.yml Datei direkt angepasst werden.

### Generelle Einstellungen

Die folgenden Variablen der Gruppe all steuern grundlegende Aspekte und sollten vor der ersten Ausführung der Automatisierung konfiguriert werden:
- db_location: 
    Der Pfad zur KeepassXC Datenbank vom Verzeichnis ./ansible/playbooks/ aus.
- db_password:
    Das Passwort für die KeepassXC Datenbank.
- ssh_public_key:
    Der ssh public key des Anwenders.
- user_list:
    Eine Liste mit den Namen aller Benutzer, für welche:
    - eine VPN Konfiguration erstellt werden soll
    - ein Gitlab Benutzer erstellt werden soll
    - ein Jenkins Benutzer erstellt werden soll

## Router

### OPNsense Router aufsetzen

Zum Aufsetzen eines OPNsense Routers müssen die folgenden Schritte durchgeführt werden:

- Herunterladen einer [OPNsense iso](https://opnsense.org/download/) mit der Architektur amd64 und dem Typ dvd.
- Erstellen eines bootbaren USB-Sticks mithilfe von balenaEtcher nach folgender [Installationsanleitung](https://linuxhint.com/create_bootable_linux_usb_flash_drive/)
- Das LAN Kabel zum internen Netzwerk des Routers am Router anstecken.
- Das LAN Kable zum externen Netzwerk des Routers am Router anstecken.
- Den USB-Stick am Router anstecken.
- Den Router starten.
- Warten bis ein Login Prompt angezeigt wird.
- Überprüfen, ob bei der Zeile, die mit "WAN" beginnt am Ende der Zeile "0.0.0.0/0" angezeigt wird. Falls dies der Fall ist, müssen die LAN Kabel für das Netzwerk genau anders herum verbunden werden. Nachdem die Anschlussreihenfolge der LAN Kabel geändert wurde muss einmal die Enter Taste gedrückt werden.
- Beim Prompt den Benutzernamen "installer" und das Passwort "opnsense" eingeben.
- Das korrekte Tastaturlayout auswählen.
- Die Installationsoption **Install (UFS)** auswählen.
- Die korrekte Festplatte auswählen.
- Die Option **Root Password** auswählen und ein Passwort setzen. Das gleiche Passwort muss später für alle Proxmox Server gewählt werden.	
- Die Option **Complete Install** auswählen.
- Sobald der Router neu bootet das Installationsmedium abziehen.

Damit der Router automatisch über ssh konfiguriert werden kann, müssen nun die folgenden Schritte ausgeführt werden:

- Das Webinterface des Rooters muss in einem Browser geöffnet werden. Hierzu muss in einen Browser die LAN IP Adresse des Routers eingebeben werden. Es kann sein, dass eine Warnung nach dem Laden der Webseite angezeigt wird. Falls eine Warnung angezeigt wird, muss auf den Button *Erweitert* geklickt werden und danach auf *Weiter zu* bei Chrome, bzw. *Risiko akzeptieren und fortfahren* bei Firefox geklickt werden.
- Im Webinterface muss nun der Benutzernahme root und das vorher gewählte Passwort eingegeben werden.
- Es muss gewartet werden, bis der Installations-Wizard anfängt. Sobald der Wizard geladen ist, kann auf das OPNsense Logo im linken oberen Eck geklickt werden. Eine Durchführung des Wizards ist nicht notwendig, da sich die Automatisierung später um die Konfiguration kümmert.
- In der Suchleiste muss der Begriff "Administration" eingegeben werden und die darunter angezeigte Option *System / Settings / Administration* ausgewählt werden.
- Es muss nun bis zum Überpunkt *Secure Shell* heruntergescrollt werden. Rechts von den Einträgen *Secure Shell Server*, *Root Login* und *Authentication Method* muss jeweilt ein Haken gesetzt werden.
- Es muss nun zum Ende der Seite heruntergescrollt werden, wo die Änderungen durch einen Klick auf *Save* gespeichert werden.

Damit ist das Aufsetzen und Vorbereiten des OPNsense Routers für die Automatisierung abgeschlossen.

### Router Automatisierung konfigurieren

Damit der Router von der Automatisierung konfiguriert werden kann, muss dessen aktuelle IP Adresse als hosts Eintrag zur Gruppe router in der gewählten Inventory Datei hinzugefügt werden. Der ursprüngliche Host Eintrag bei router kann beibehalten oder gelöscht werden.

Falls die aktuelle IP Adresse des Routers 192.168.1.1 ist, sollten die ersten 6 Zeilen der inventory Datei also so aussehen:

```yaml
all:
  children:
    router:
      hosts:
        192.168.1.1:
    server:
```

### Router Automatisierung ausführen

Um die Router Automatisierung zu starten muss im Verzeichnis ansible das folgende Kommando ausgeführt werden, wobei {inventory_file} durch den Dateinamen des erstellen Inventories ersetzt werden muss:

```bash
ansible-playbook -i ../{inventory_file} -k router.yml
```

Nach der Bestätigung des Kommandos erscheint ein Prompt in welchem das Password für den root Benutzer des OPNsense Routers eingegeben werden muss.

**Achtung**

Wenn die Router Automatisierung das erste Mal durchgelaufen ist, wurde die IP Adresse des Routers geändert. Deswegen müssen die folgenden Dinge **nach** der Automatisierung gemacht werden:
- Der Host Eintrag des Routers in der Inventory Datei muss auf die IP Adresse 172.16.0.1 gesetzt werden.
- Für den Computer des Benutzers der Bedienungsanleitung muss eine neue IP Adresse vom Router angefordert werden. Dies geschieht durch die Ausführung der folgenden Kommandos:
  ```bash
  sudo dhclient -r
  sudo dhclient
  ```

## Proxmox Server

### Proxmox Server aufsetzen

Zum Aufsetzen eines Proxmox Servers müssen die folgenden Schritte durchgeführt werden:

- Herunterladen einer Proxmox VE ISO von der [Proxmox Download Seite](https://www.proxmox.com/de/downloads/category/iso-images-pve).
- Erstellen eines bootbaren USB-Sticks mithilfe von balenaEtcher nach folgender [Installationsanleitung](https://linuxhint.com/create_bootable_linux_usb_flash_drive/)
- Den Proxmox Server am internen Netzwerk (LAN) des Routers anschließen.
- Des USB-Stick am Server anstecken.
- Den Server starten.
- Die Option **Install Proxmox VE** auswählen.
- Die EULA annehmen.
- Die richtige Festplatte für die Installation auswählen.
- Die richtige Zeitzone einstellen.
- Für jeden Proxmox Server muss das gleiche Passwort eingeben werden und eine valide Email Adresse gesetzt werden.
- Die automatische IP Adressen Konfiguration bestätigen.
- Die Installation bestätigen.	
- Sobald der Server neu bootet das Installationsmedium abziehen.

**Achtung**

Es können beliebig viele Proxmox Server für die Verwendung in der CIinaBox aufgesetzt werden. Falls mehrere Server verwendet werden sollen, sollte allerdings für den root Benutzer aller Server beim Aufsetzen der Server das gleiche Passwort verwendet werden.

### Proxmox Server Automatisierung konfigurieren

Für jeden zu verwendenden Proxmox Server muss ein yaml Block wie im folgenden Beispiel zu den children von server hinzugefügt werden.

```yaml
        server-top:
          children:
            proxmox:
              hosts:
                172.16.1.2: # Zukünftige IP Adresse
                172.16.3.7: # Aktuelle IP Adresse
                  ip_addr: "172.16.1.2/12"
            vms:
              children:
                gitlab:
                  hosts:
                    172.16.1.10:
                jenkins:
                  hosts:
                    172.16.1.20:
                runner:
                  hosts:
                    172.16.1.30:
                  vars:
                    # The ip/hostname of the runners gitlab server.
                    gitlab_instance: 172.16.1.10
                agent:
                  hosts:
                    172.16.1.40:
                  vars:
                    # The ip/hostname of the agents jenkins server.
                    jenkins_instance: 172.16.1.20
              vars:
                ansible_user: ansible
          vars:
            subnet: "172.16.0.0"
            suffix: "top"
```

Danach müssen die folgenden Schritte für jeden Proxmox Server ausgeführt werden:

1. Setzen des *suffix*. Das *suffix* nach einem Bindestrich wird dem Hostnamen des Proxmox Servers und jeder seiner VMs angehängt. Der Hostname der Proxmox Instanz im obrigen yaml wäre z.B. proxmox-top und der Hostname der Jenkins Instanz jenkins-top. Falls kein suffix gesetzt wird, ist der Hostname der Proxmox Instanz proxmox und der Hostname der Jenkins Instanz jenkins. Die Zeile mit der Variable suffix muss entfernt werden, um das suffix nicht zu setzen.
2. Setzen des Gruppennamen. Der Gruppenname ergibt sich aus *server*, einem *Bindestrich* und *suffix*. Falls kein suffix gesetzt ist, ist der Gruppenname server.
3. Setzen der aktuellen Proxmox IP Adresse. Der Proxmox Gruppe des Servers muss ein Host Eintrag mit der aktuellen IP Adresse des Proxmox Servers hinzugefügt werden.
4. Setzen der zukünftigen Proxmox IP Adresse. Die zukünftige IP Adresse des Proxmox Servers muss innerhalb des 172.16.0.0/12 Netzwerkes sein. Der Proxmox Gruppe des Servers muss ein Host Eintrag mit der zukünftigen IP Adresse des Proxmox Servers hinzugefügt werden. 
5. Außerdem muss die **Gruppenvariable** ip_addr der Gruppe Proxmox zu der zukünftigen IP Adresse des Proxmox Servers gefolgt von */12* gesetzt werden, also z.B.: "172.16.1.2/12".
6. Setzen der VM IP Adressen. Für jede Untergruppe der Gruppe vms können 0 bis beliebig viele Host IP Adressen innerhalb des 172.16.0.0/12 Netzwerkes hinzugefügt werden.
7. Falls Hosts zur Runner Gruppe hinzugefügt wurden, muss die Variable gitlab_instance für die Gruppe gesetzt werden. Ihr Inhalt muss die IP Adresse einer Gitlab Instanz im Netzwerk des CIinaBox Routers sein. Die Variable gitlab_instance kann sowohl auf Gruppenbasis als auch für Hosts individuell gesetzt werden.
8. Falls Hosts zur Agent Gruppe hinzugefügt wurden, muss die Variable jenkins_instance für die Gruppe gesetzt werden. Ihr Inhalt muss die IP Adresse einer Jenkins Instanz im Netzwerk des CIinaBox Routers sein. Die Variable jenkins_instance kann sowohl auf Gruppenbasis als auch für Hosts individuell gesetzt werden.

### Proxmox Server Automatisierung ausführen

Um die Router Automatisierung zu starten muss im Verzeichnis ansible das folgende Kommando ausgeführt werden, wobei {inventory_file} durch den Dateinamen des erstellen Inventories ersetzt werden muss:

```bash
ansible-playbook -i ../{inventory_file} -k ciinabox.yml
```

Nach der Bestätigung des Kommandos erscheint ein Prompt in welchem das Password für die root Benutzer der Proxmox Server eingegeben werden muss.

## Self-signed CA einrichten (optional)

Bei der Ausführung der Automatisierung wurde ein (self-signed) root-Zertifikat erstellt, welches für alle Webserver SSL Zertifikate ausstellt. 
Um Warnungen vor ungültigen Zertifikaten zu verhindern, sollte dieses root-Zertifikat im Browser jedes Benutzers des CIinaBox Demonstrators installiert werden. Damit auch curl für lokale https URLs (welche zum Beispiel bei git Befehlen verwendet werden) funktioniert, muss das root-Zertifikat zusätzlich lokal installiert werden.

Das Hinzufügen des root-Zertifikates zu den Systemzertifikaten und zu den Browser-Zertifikaten ist optional. Im Folgenden wird zuerst das Hinzufügen zu einem Browser und danach das Hinzufügen zu den Systemzertifikaten beschrieben.

### Zu Firefox hinzufügen 

1. Der Firefox Browser muss geöffnet werden.
2. In der Adresszeile des Browsers muss "about:preferences" eingegeben werden und danach durch das Drücken der Enter Taste bestätigt werden.
3. In der Suchleiste muss das Wort "Zertifikate" eingegeben werden (und möglicherweise durch das Drücken der Enter Taste bestätigt werden).
4. Der Button "Zertifikate anzeigen" muss angeklickt werden.
5. Der Reiter "Zertifizierungsstellen" muss durch Anklicken ausgewählt werden.
6. Der Button "Importieren" unterhalb der Tabelle muss angeklickt werden.
7. In dem neu geöffneten Fenster muss zum obersten Verzeichnis der Infrastruktur Automatisierung navigiert werden.
8. Falls die Datei "ciinabox-ca.crt" nicht angezeigt wird, muss der (Dropdown-)Button rechts unten angeklickt werden und danach die Option "Alle Dateien" ausgewählt werden.
9. Die Datei "ciinabox-ca.crt" muss nun ausgewählt werden und danach muss der "Öffnen" Button rechts oben angeklickt werden.
10. Im neu geöffneten Fenster muss ein Haken bei der Option "Dieser CA vertrauen, um Websites zu identifizieren" gesetzt werden und danach auf "OK" geklickt werden.

### ZU Chrome hinzufügen

1. Der Chrome Browser muss geöffnet werden.
2. In der Adresszeile des Browsers muss "chrome://settings/certificates" eingegeben werden.
3. Der Reiter "Zertifizierungsstellen" muss angeklickt werden.
4. Der Button "Importieren" muss angeklickt werden.
5. Im neu geöffneten Dialog muss zum obersten Verzeichnis der Infrastruktur Automatisierung gewechselt werden.
6. Falls die Datei "ciinabox-ca.crt" nicht angezeigt wird, muss beim (Dropdown-)Button rechts unten alle Dateien ausgewählt werden.
7. Die Datei "ciinabox-ca.crt" muss durch anklicken ausgewählt werden.
8. Durch das Klicken auf den "Öffnen" Button rechts oben wird das Zertifikat zum Browser hinzugefügt.
9. Im jetzt neu angezeigten Dialog muss ein Haken bei der Option "Diesem Zertifikat zum Identifizieren von Websites vertrauen" gesetzt werden.
10. Mit einem Klick auf den "Ok" Button wird das Zertifikat zum Chrome Browser hinzugefügt.

### Zu den Systemzertifikaten hinzufügen

1. Das Paket "ca-certificates" installieren mit dem Kommando  
    ```
    sudo apt install ca-certificates -y
    ```
2. Ein Terminal im obersten Verzeichnis der Infrastruktur Automatisierung öffnen und das folgende Kommando ausführen
    ```
    sudo cp ./ciinabox-ca.crt /usr/local/share/ca-certificates
    ```
3. Die Systemzertifikate mit dem folgenden Kommando aktualisieren.
    ```
    sudo update-ca-certificates
    ```

### Von Firefox entfernen 

1. Der Firefox Browser muss geöffnet werden.
2. In der Adresszeile des Browsers muss "about:preferences" eingegeben werden und danach durch das Drücken der Enter Taste bestätigt werden.
3. In der Suchleiste muss das Wort "Zertifikate" eingegeben werden (und möglicherweise durch das Drücken der Enter Taste bestätigt werden).
4. Der Button "Zertifikate anzeigen" muss angeklickt werden.
5. Der Reiter "Zertifizierungsstellen" muss durch Anklicken ausgewählt werden.
6. Den Eintrag "HSA_innos" in dem Feld "Zertifikatsname" finden.
7. Den Eintrag "ciinabox-ca" unterhalb von HSA_innos angeklicken (Falls dieser nicht sichtbar ist, muss auf den Pfeil links neben HSA_Innos geklickt werden).
8. Der Button "Löschen oder Vertrauen entziehen..." muss angeklickt werden.
9. Den neu geöffneten Dialog durch das Klicken auf "OK" bestätigen.

### Von Chrome entfernen 

1. Der Chrome Browser muss geöffnet werden.
2. In der Adresszeile des Browsers muss "chrome://settings/certificates" eingegeben werden.
3. Der Reiter "Zertifizierungsstellen" muss angeklickt werden.
4. In der Liste den Eintrag "org-HSA_innos" finden und auf den Pfeil am Ende der Eintragszeile klicken.
5. Auf die drei Punkte am Ende des (nun geöffneten) Untereintrags "ciinabox-ca" klicken.
6. In dem Dropdown dir Option "Löschen" anklicken.
7. Mit dem Klicken auf "Ok" das Löschen bestätigen.

### Von den Systemzertifikaten entfernen

1. Das Zertifikat aus den system ssl Zertifikaten entfernen mit dem Kommando 
  ```bash
  sudo rm /etc/ssl/certs/ciinabox-ca.pem
  ```
  
2. Das Zertifikat aus den lokalen ca Zertifikaten entfernen mit dem Kommando 
  ```
  sudo rm /usr/local/share/ca-certificates/ciinabox-ca.crt
  ```


## Fehlerbehebung

### REMOTE HOST IDENTIFICATION HAS CHANGED

**Fehlergrund**

Der Computer hat eine alte SSH Verbindung zu einem Computer mit einer in der Automatisierung verwendeten IP Adresse eingespeichert und erkennt, dass ein anderer Computer diese IP Adresse hat. Aus Sicherheitsgründen wird deswegen die SSH Verbindung blockiert.

**Fehlerbehebung**

- Die IP Adresse herausfinden, welche den Fehler auslöst. Die IP Adresse befindet sich in der Fehlermeldung.
- Das nachfolgende Kommando ausführen, wobei {{ benutzername }} mit dem Benutzernamen des Benutzers der Anleitung und {{ ip_adresse }} mit der im letzten Schritt gefundenen IP Adresse ersetzt werden muss:
  ```bash
  ssh-keygen -f /home/{{ benutzername }}/.ssh/known_hosts -R "{{ ip_adresse }}"
  ```
