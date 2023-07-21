# local.jenkins-controller

This role installs Jenkins (with it's dependencies), configures it's server settings, installs the suggested plugins and adds an SSH key for connections with ssh agents.

## Requirements

n/a

## Role Variables

**jar configuration**

```yaml
# The file jenkins uses at it's initial start.
jenkins_init_file: /etc/default/jenkins

# The changed to be made to jenkins_init_file.
jenkins_init_changes:
  - option: "JENKINS_ARGS"
    value: "--prefix={{ jenkins_url_prefix }}"
  - option: "{{ jenkins_java_options_env_var }}"
    value: "{{ jenkins_java_options }}"

# The environment variables when starting jenkins.
jenkins_java_options_env_var: JAVA_ARGS

# The options set while starting jenkins.
jenkins_java_options: "-Djenkins.install.runSetupWizard=false"

# The port parameter.
jenkins_http_port_param: HTTP_PORT
```

**system user configuration**

```yaml
# The jenkins process user
jenkins_process_user: jenkins

# The jenkins process group
jenkins_process_group: "{{ jenkins_process_user }}"

# The directory where the files of the jenkins server will be stored.
jenkins_home: /var/lib/jenkins
```

**jenkins-cli configuration**

```yaml
# Where to download/find the jenkins-cli
jenkins_jar_location: /opt/jenkins-cli.jar

# Duration to wait before a retry
jenkins_connection_delay: 5

# The amount of retries
jenkins_connection_retries: 60
```

**Java configuration**

```yaml
# The java version to install
java_package: openjdk-11-jre
```

**admin user configuration**

```yaml
# The username of the first administrator in the web interface
jenkins_admin_username: admin

# The password of the first administrator in the web interface
jenkins_admin_password: admin

# An alternative to the password
jenkins_admin_password_file: ""
```

**Jenkins URL configuration**

```yaml
# The hostname
jenkins_hostname: localhost

# The url prefix, e.g. /jenkins
jenkins_url_prefix: ""

# The port the server should accept requests on
jenkins_http_port: 8080
```

**Jenkins Proxy configuration**

```yaml
# The URL/ip address of the Proxy server.
jenkins_proxy_host: ""

# The port of the proxy server
jenkins_proxy_port: ""
```

**Jenkins SSH config**

```yaml
# The ssh credential name
ssh_credential_name: jenkins_agents
```

**Jenkins Plugin configuration**

```yaml
# The URL where jenkins gets it's updates
jenkins_updates_url: "https://updates.jenkins.io"

# The list of plugins to install
jenkins_plugins:
  - name: ace-editor
  - name: ant
  - name: antisamy-markup-formatter
  - name: branch-api
  - name: cloudbees-folder
  - name: credentials
  - name: cvs
  - name: docker-plugin
  - name: durable-task
  - name: external-monitor-job
  - name: git-client
  - name: git-server
  - name: git
  - name: github-api
  - name: github-branch-source
  - name: github
  - name: javadoc
  - name: jquery-detached
  - name: junit
  - name: ldap
  - name: mailer
  - name: matrix-auth
  - name: matrix-project
  - name: maven-plugin
  - name: metrics
  - name: pam-auth
  - name: plain-credentials
  - name: scm-api
  - name: script-security
  - name: ssh-credentials
  - name: ssh-slaves
  - name: subversion
  - name: translation
  - name: variant
  - name: windows-slaves
  - name: workflow-aggregator
  - name: workflow-api
  - name: workflow-basic-steps
  - name: workflow-cps
  - name: workflow-durable-task-step
  - name: workflow-job
  - name: workflow-multibranch
  - name: workflow-scm-step
  - name: workflow-step-api
  - name: workflow-support
  - name: favorite
  - name: token-macro
  - name: pipeline-stage-step
  - name: blueocean
  - name: blueocean-autofavorite
  - name: gitlab-plugin

# The state of the plugins in the list jenkins_plugins
jenkins_plugins_state: present

# Whether to install the dependencies needed by the plugins
jenkins_plugins_install_dependencies: true

# The timeout while checking for plugins
jenkins_plugin_timeout: 30

# The timeframe until jenkins checks for new updates.
jenkins_plugin_updates_expiration: 86400
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
    - local.jenkins-controller
```

## License

BSD

## Author Information

Author: Fabian Antonio Klemm
Company: Hsa_innos
