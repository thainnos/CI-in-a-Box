## 1.3. Jenkins Agents aufsetzen
Folgende Schritte müssen alle zweimal ausgeführt werden: Einmal für die dritte VM, die als Build Node agiert,
und für den Raspberry Pi.
Es empfiehlt sich, die Benennung von den Keys/Nodes/Labels entsprechend anzupassen.

### 1.3.1. SSH Key erstellen
Zunächst muss lokal ein SSH Key erstellt werden (nicht auf dem Agent):
```bash
ssh-keygen -f ~/.ssh/<jenkins_agent_name>_key
```
Danach den Key wie folgt in Jenkins hinzufügen:
1. Jenkins Dashboard in einem Browser öffnen.
2. Auf **Manage Jenkins** in der linken Seitenleiste klicken und danach **Manage Credentials** auswählen.
3. Auf den Dropdown neben **(global)** klicken und dann auf **Add Credentials** gehen.
4. Im Dropdownmenu die Option **SSH Username with private Key** auswählen.
   Einen Namen zur Identifikation im Feld **ID** eingeben.
    **jenkins** als Benutzernamen angeben.
   Auf **Enter directly** unter Private Key klicken.
   Den private SSH Key in der Konsole mit dem Kommando `cat ∼/.ssh/<jenkins_agent_name>_key` ausgeben und
   dann in das Textfeld einfügen.
   Falls ein Passwort gewählt wurde, muss das mit angegeben werden.

### 1.3.2. Agent selbst einreichten
Jetzt muss auf dem zukünftigen Agent ein Benutzer für Jenkins eingerichtet werden.
Dazu muss man sich auf dem Ant einloggen und den folgenden Command eingeben
(Auchtung: gleichen Benutzernamen wie im [letzten Schritt](#131-ssh-key-erstellen) verwenden)
```bash
useradd -m jenkins
```

Jetzt muss der SSH Key aus dem [letzten Schritt](#131-ssh-key-erstellen)
mit folgendem Command auf den Agent kopiert werden:
```bash
ssh-copy-id -i ~/.ssh/<jenkins_agent_name>_key.pub jenkins@<agent_ip_adresse>
```

Abschließend muss noch Java auf dem Agent installiert werden:
```bash
apt update
apt install -y openjdk-17-jre
```

### 1.3.3. Agent in Jenkins registrieren
1. Jenkins Dashboard in einem Browser öffnen.
2. Auf **Manage Jenkins** in der linken Seitenleiste klicken und danach **Manage Nodes and Clouds** auswählen.
3. Im Seitenmenu **New Node** auswählen.
4. Zuerst dem Agent einen Namen geben, anschließend die Option **Permanent Agent** auswählen und **Create** anklicken.
5. Nun die folgenden Felder ausfüllen:
    - Im Feld **Remote root directory** den Wert **/home/jenkins** ein.
    - Im Feld **Labels** Tags/Schlagwörter eingeben. Mithilfe dieser Schlagwörter kann später innerhalb einer Pipeline ausgewählt werden, auf welchem Agent eine Pipeline durchgeführt werden soll.
    - Im Feld **Launch method** muss die Option **Launch agents by SSH** ausgewählt werden. Hier muss die IP Adresse des vorher erstellen Agents eingetragen und anschließend das vorher erstellte Password File ausgewählt werden. Dann im Punkt **Host Key Verification Strategy** die Option **Manually trusted key Verification Strategy** auswählen
6. Nun auf **Save** klicken, um den Agent hinzuzufügen.
7. Falls der Agent nicht von selbst geladen werden sollte, kann der Agent in der automatisch geöffneten Übersicht durch Anklicken ausgewählt werden und danach mit dem Button **Launch agent** gestartet werden.


# 2. Pipeline aufsetzen und konfigurieren
Jetzt setzen wir die Pipeline in Jenkins auf und alles was dazu gehört.
Es wird davon ausgegangen, dass ein Repository `<repo_name>` auf dem GitLab existiert, das gebaut werden soll.

## 2.1. Builder User in GitLab erstellen
Bevor die Pipeline aufgesetzt werden kann, muss ein "Builder User" in GitLab angelegt werden.
Dieser User muss Teil von jedem Repository/jeder Gruppe sein, das gebaut werden soll.  
***Achtung***: Dies muss nur getan werden, wenn das Jenkinsfile/Pipeline Script im SCM liegt und
nicht direkt in der Pipeline selbst.

1. Unter GitLab einen neuen User anlegen.
   Hierbei am besten einen Username `<builderUser>` wählen, der einfach als "Builder User" zu identifizieren ist.
2. Oben rechts auf **Preferences** gehen und anschließend in der linken Seitenleiste auf **SSH Keys**.
3. Jetzt in einem Terminal den Command `ssh-keygen -f ~/.ssh/<builderUser>_key` eingeben.
4. Mit `cat ∼/.ssh/<builderUser>_key.pub` den Public Key ausgeben lassen und den kopieren.
5. In GitLab jetzt im Key Eingabefenster den kopierten Key einfügen, dem Ganzen einen Titel geben und
   abschließend auf **Add key** klicken.
6. Jetzt ins Jenkins Dashboard wechseln und in der linken Seitenleiste auf **Manage Jenkins** gehen.
7. Anschließend **Manage Credentials** auswählen.
8. Auf den Dropdown neben **(global)** klicken und dann auf **Add Credentials** gehen.
9. Jetzt wie [zuvor](#131-ssh-key-erstellen) den SSH Key hinzufügen:
   Im Dropdownmenu die Option **SSH Username with private Key** auswählen.
   Einen Namen zur Identifikation im Feld **ID** eingeben.
    `<builderUser>` als Benutzernamen angeben.
   Auf **Enter directly** unter Private Key klicken.
   Den private SSH Key in der Konsole mit dem Kommando `cat ∼/.ssh/<builderUser>_key` ausgeben und
   dann in das Textfeld einfügen.
   Falls ein Passwort gewählt wurde, muss das mit angegeben werden.


## 2.2. Pipeline einrichten
Nun wird die wirkliche Pipeline eingerichtet und vorkonfiguriert, soweit es geht.

1. Im Jenkins Dashboard in der linken Seitenleiste auf **New Item** klicken.
2. Jetzt der Pipeline einen Namen geben, **Pipeline** auswählen und **Ok** klicken.  
   ***Achtung***: Name darf *keine* Leerzeichen enthalten
3. Unter **Build Triggers** die Option **Build when a change is pushed to GitLab...** setzen
   (Die Webhook URL merken/kopieren, kann aber später jederzeit eingesehen werden).
4. Auf **Advanced** klicken und bei **Secret token** auf **Generate** klicken.
5. Den generierten Token kopieren und für später merken/speichern.
   (Der Token kann später jederzeit eingesehen werden).
4. Im Abschnitt **Pipeline** unter **Definition** im Dropdownmenu **Pipeline script from SCM** auswählen.
   ***Achtung***: Dient nur zu Entwicklungszwecken.
   Sollte normalerweise auf **Pipeline Script** stehen mit direkt eingegebenem Script,
   da dann das Pipeline Script nur in Jenkins von berechtigten Personen geändert werden kann
   und nicht von jedem im SCM.
5. Im Dropdown unter **SCM** jetzt **Git** auswählen.
6. Jetzt muss aus dem Repository die URL zum "Clonen mit SSH" kopiert werden und unter **Repository URL** eingefügt werden.
7. Anschließend unter Credentials die [zuvor](#21-builder-user-in-gitlab-erstellen) erstellen \<builderUser> Credentials auswählen.
8. Unter **Branches to build** sicher stellen, dass `*/main` und nicht `*/master` eingetragen ist.


## 2.3. Webhook im Repository aufsetzen
Damit die Pipeline auch informiert wird, dass ein Push ins Repository gekommen ist, müssen wir die Webhook für das entsprechende Repo aufsetzen.
Hierzu nutzen wir die Webhook URL und den Secret Token von [zuvor](#22-pipeline-einrichten).
Wir benutzen hier ein Webhook, weil die Jenkins Integration einen User mit Passwort fordert.

1. Im entsprechenden Repository `<repo_name>` in der linken Seitenleiste auf **Settings > Webhooks**.
2. Unter **URL** muss die Webhook URL und unter **Secret token** der Secret token von [zuvor](#22-pipeline-einrichten) eingetragen werden.
3. Jetzt auf **Add webhook** klicken.
4. In der angelegten Project Hook im Dropdown **Test** auf **Push events** klicken.
   Wenn alles geklappt hat, sollte oben auf der Seite jetzt `Hook executed successfully: HTTP 200` stehen.


## 2.4. Links
 - [Jenkins Integration in GitLab](https://docs.gitlab.com/ee/integration/jenkins.html)


# 3. Pipeline Script
Jenkins setzt als Modelling Sprache auf eine Pipeline Domain-Specific Language (DSL).
Das Pipeline Script wird als deklarative Pipeline gebaut.
Der Hauptteil der Dokumentation steht als Kommentare in dem Pipeline Script `Jenkinsfile` direkt.
Die Pipeline hat fünf Stages:
- **Prepare Stashes**: Kopieren der letzten erfolgreichen Artifacts
- **Build**: Bauen des Chipwhisperer Firmware Images
- **Capture**: Ausführen des Seitenkanal Angriffes auf den Chipwhisperer
- **Analyze**: Auswertung der Testdaten und generieren des Reports
- **Collect Artifacts**: Sammeln und abspeichern der Artifacts

Es werden hier fünf Stages gebraucht, obwohl nur 3 effektiv was tun.
Die anderen zwei Stages werden gebraucht, um "incremental Pipelines" zu ermöglichen.
Es müssen zunächst die in der **Prepare Stashes** Artifacts kopiert werden und in die einzelnen Stashes gepackt werden.
Dann werden in den drei Main Stages **Build**, **Capture** und **Analyze** die eigentliche Pipeline Aufgaben erledigt.
Am Ende wird in der **Collect Artifacts** Stage die gesamten Artifacts aus den Stashes gesammelt und als Pipeline Artifacts abgespeichert.

Der incremental Charakter der Pipeline druckt sich dadurch aus, dass die Main Stages nur gebaut werden, wenn in dem entsprechenden Ordner sich etwas geändert hat.
Das Triggern der Main Stages sieht wie folgt aus:
- **Build**: Changes im *firmware/* Ordner
- **Capture**: Changes im *firmware/* oder *capture/* Ordner
- **Analyze**: Changes im *firmware/*, *capture/* oder *analyze/* Ordner

Mit **--force** kann man eine vollen Rebuild von allen Stages erzwingen, auch wenn es keine Änderungen gab.
Die beiden anderen Stages laufen immer durch, damit ein sauberer Zustand der der Artifacts garantiert werden kann.
Das vorbereiten der Stashes muss gemacht werden, da nicht garantiert werden kann, dass die vorherige Stage durchläuft, deren Artifacts in der Stage gebraucht werden.
Da Stashes mit gleichem Namen werden überschrieben, was das Problem der Artifactsbeschaffung vereinfacht.
Wenn das **--force** Flag benutzt wird, wird die **Prepare Stashes** Stage nicht ausgeführt, da diese nicht notwendig ist.
***Achtung***: Der allerste Run der Pipeline ***muss*** mit dem **--force** Flag ausgeführt werden.

Folgende Links wurden verwendet, um die Pipeline aufzubauen.
- [Jenkins Pipeline Doc](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax DSL](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins with Pyenv](https://medium.com/@artem.hatchenko/jenkins-python-virtualenv-with-version-selection-8a5db11a3ad2)
- [Python Build Dependencies for Pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
- [Remove sudo from jenkins user](https://stackoverflow.com/a/20241946)
- [Sudoers file](https://embeddedartistry.com/blog/2017/11/16/jenkins-running-steps-as-sudo/)