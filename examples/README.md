# Examples

This section provides an overview of the examples provided by the project.

## Overview

 - `apache-server`: a default configured apache server that gets tested from the Jenkins pipeline with a port scan and ssl version test and compiled into a small report
 - `apache-server-secure`: a more secure version of the `apache-server` example
 - `chipwhisperer`: a sidechannel DPA attack for an AES implementation with a Chipwhisperer lite based on the official chipwhisperer example

## Importing an Example to Gitlab
How to import an example Gitlab:

1. If not done yet, generate an SSH key for the Gitlab user and add it to the users SSH keys.
2. Create a new blank project with the name of the examples folder on the Gitlab instance (either under the group or the user).
   Be sure to deselect any initialization with READMEs or similar.
3. Follow the instructions shown on the project page to push an existing folder:
   ```bash
   cd existing_folder
   git init --initial-branch=main
   git remote add origin ssh://git@{{ Gitlab Instance IP/Domain }}/{{ user/group }}/{{ example }}.git
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```
   The {{Gitlab Instance IP/Domain}} is either shown in the displayed instructions or can be found in the automation settings or the OPNsense interface.
   The {{ user/group }} is either the user or the group under which this repository was created.
   {{ example }} is the desired example to import.