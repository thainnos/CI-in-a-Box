# Jenkins

This playbook consists of three plays. The first play installs and configures the jenkins web application, the second play configures a system for use as a jenkins agent/slave and the third play adds all jenkins agents/slaves to the jenkins server.

## Requirements

This playbook depends on the roles local.jenkins-add-slave, local.jenkins-controller and local.jenkins-slave-setup.

## Variables

In the following section the changeable variables will be listed with a short description and their default value. You can change all these values in the vars.yml file in this playbook.

**System configuration**

```yaml
# The jenkins process user
jenkins_process_user: jenkins

# The jenkins process group
jenkins_process_group: "{{ jenkins_process_user }}"

# The directory where the files of the jenkins server will be stored.
jenkins_home: "/var/lib/jenkins"
```

**SSH Credential configuration**

```yaml
# The ssh credential name
ssh_credential_name: jenkins_agents

# The label of the jenkins agent
agent_labels: jenkins
```

**Jenkins jar configuration**

```yaml
# The location of the file used at the initialisation of jenkins.
jenkins_init_file: /etc/default/jenkins

# The changes to the init file.
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

**jenkins-cli**

```yaml
# Where to download/find the jenkins-cli
jenkins_jar_location: /opt/jenkins-cli.jar

# Duration to wait before a retry
jenkins_connection_delay: 5

# The amount of retries
jenkins_connection_retries: 60
```

**Jenkins user configuration**

```yaml
# The username of the first administrator in the web interface
jenkins_admin_username: admin

# The password of the first administrator in the web interface
jenkins_admin_password: admin

# An alternative to the password
jenkins_admin_password_file: ""
```

**Java configuration**

```yaml
# The java version to install
java_package: openjdk-11-jre
```

**URL configuration**

```yaml
# The hostname
jenkins_hostname: localhost

# The url prefix, e.g. /jenkins
jenkins_url_prefix: ""

# The port the server should accept requests on
jenkins_http_port: 8080

# The complete URL (internal variable built from the previous three variables)
__jenkins_complete_base_url: "http://{{ jenkins_hostname }}:{{ jenkins_http_port }}{{ jenkins_url_prefix }}"
```

**Proxy configuration**

```yaml
# The URL/ip address of the Proxy server.
jenkins_proxy_host: ""

# The port of the proxy server
jenkins_proxy_port: ""
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

## Example configurations

In the following sections different use cases for the three roles will be specified. The playbook main.yml will be the same in every case, the only difference will be in the vars.yml file.

**Default setup**

The current playbook creates a jenkins server at every host specified in the hosts group jenkins with the default
values, configures every host in the host group jenkinsagent as a jenkins slave/agent and adds every jenkins slave/agent to every jenkins server.

**Custom URL configuration**

Make jenkins reachable at the URL http://example.com:80/jenkins.

```yaml
jenkins_hostname: "example.com"
jenkins_url_prefix: "/jenkins"
jenkins_http_port: 80
```

**Custom Proxy configuration**

Make jenkins use a proxy at example.com:8080.

```yaml
jenkins_proxy_host: "example.com"
jenkins_proxy_port: "8080"
```

**Custom Plugin configuration**

A possible minimal installation of Jenkins which will be configured to work with Gitlab repositories.

```yaml
jenkins_plugins:
  - name: antisamy-markup-formatter
  - name: credentials
  - name: git-client
  - name: git-server
  - name: git
  - name: plain-credentials
  - name: ssh-credentials
  - name: ssh-slaves
  - name: blueocean
  - name: blueocean-autofavorite
  - name: gitlab-plugin
```

## License

BSD

## Author Information

Author: Fabian Antonio Klemm p.p. HSAinnos
