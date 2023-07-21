# local.jenkins-slave-setup

This role sets up a user for later ssh connections made by the jenkins controller and installs Java.

## Requirements

n/a

## Role Variables

```yaml
# The java package to install.
java_package: openjdk-11-jre
```

## Dependencies

n/a

## Example Playbook

Default usage

```yaml
- name: Add all agents to all jenkins controllers.
  hosts: jenkins
  become: yes

  roles:
    - local.jenkins-slave-setup
```

## License

BSD

## Author Information

Author: Fabian Antonio Klemm
Company: Hsa_innos
