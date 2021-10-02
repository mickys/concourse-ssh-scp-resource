# ssh-scp-resource
A Concourse resource to run commands on hosts or copy files to them using SSH or SCP.

## Resource Configuration
All items are required, and go under the `source` key:

* `user`: SSH username
* `host`: Host to log into
* `private_key`:  Private key for `user`

## Behavior

* `check`: Not implemented
* `get`: Not implemented
* `put`: Run a command or copy a file to the configured `user@host`

To copy files, add the`files` key to `params`, and under it, give the source as a key and destination as value for each file or directory. It is recommended to quote both the source and destination to avoid any YAML parsing surprises. The source directory should be an `output` name from a previous build step.

```yaml
 params:
   files:
     "outfiles/index.html": "/var/www/public_html/index.html"
     "outfiles/page.html": "/var/www/public_html/page.html"
 ```
 
To run commands, add the `commands` key to `params`, and under that, give the commands to run as list items (prefixed with a `-`). Again, quotes are recommended to avoid YAML surprises.

```yaml
params:
  commands:
    - 'ls /var/www/public_html`
    - `free -m`
```

You may copy files and run commands as part of the same step. Note that file copies will always be run first.
```yaml
params:
  files:
     "outfiles/index.html": "/var/www/public_html/index.html"
     "outfiles/page.html": "/var/www/public_html/page.html"
  commands:
    - 'ls /var/www/public_html`
    - `md5sum /var/www/public_html/*`
```

## Installation
Add a new resource type to your pipeline:
```yaml
resource_types:
#
- name: ssh-scp
  type: registry-image
  source: { repository: karunamon/concourse-ssh-scp-resource }
```

Then, define a resource targeting the system you want to run commands on or copy files to:
```yaml
resources:
- name: website-html-scp
  type: ssh-scp
  icon: web
  source:
    user: someuser
    host: mywebserver.com
    private_key: |
      -----BEGIN OPENSSH PRIVATE KEY-----
      # redacted
      -----END OPENSSH PRIVATE KEY-----
```
