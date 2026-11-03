---
title: The Docker-Compose Template
---

When starting an app, the shard simply brings up a docker-compose file just like you would with `docker-compose up`.
This file is generated during installation of the app from a `docker-compose.yml.template` that you have to provide.
The template is a normal docker-compose file with some special variables that the shard will replace with the correct values,
and a `secret()` helper that fills in generated passwords.

---

{!developer_docs/includes/portal_name_info.md!}

## Minimal Example

Let's first look at a minimal example.
This is the most basic template for an app made up of a single container and no dependencies and no special configuration.
Click on the plus buttons for a description of each field.

```yaml
version: '3.5'

networks: # (1)!
    portal:
        external: true

services:
    my-app:
        image: my-app:v4 # (2)!
        container_name: my-app # (3)!
        volumes:
        - "{{ fs.app_data }}/data:/data" # (4)!
        networks:
        - portal # (5)!
```

1. This is the network that the shard uses to connect all apps together and to the reverse proxy and the shard core.
    You need to include this in your template.
2. This is the image that will be used for your app. Please specify a fixed version, not just `my-app:latest`.
   When you update your app, you will also need to release a new version of the metadata including a new template.
3. You must explicitly set the container name, and it must match with the service name.
4. In order to persist data, you need to mount a host directory.
   For data that only concerns your app, you should use the `fs.app_data` variable
   and a subdirectory that matches the directory inside the container.
   Read more in the section on [persisting data](persisting.md).
5. You need to connect your app to the `portal` network specified above.

## Complex Example

Now let's look at a more complex example.
Here we have an app that depends on a password-protected redis database and has some environment variables that need to be set.
We also want to access the shared part of the filesystem where apps can store data that is shared between them.

```yaml
version: '3.5'

networks:
    portal:
        external: true

services:
    my-app:
        image: my-app:v4
        container_name: my-app
        depends_on:
        - my-app-redis # (1)!
        volumes:
        - "{{ fs.app_data }}/data:/data"
        - "{{ fs.shared }}/shared_data:/shared_data" # (2)!
        networks:
        - portal
        environment:
        - REDIS_HOST=my-app-redis # (3)!
        - BASE_URL=https://my-app.{{ portal.domain }} # (4)!
        - TITLE=My app on {{ portal.short_id }} # (5)!
        - REDIS_PASSWORD={{ secret('redis_password') }} # (6)!

    my-app-redis: # (7)!
        image: redis:6.2
        container_name: my-app-redis
        command: redis-server --requirepass {{ secret('redis_password') }} # (8)!
        volumes:
        - "{{ fs.app_data }}/redis_data:/redis_data" # (9)!
        networks:
        - portal
```

1. The app container depends on the redis container, so that the redis container will be started first.
2. We mount the shared data directory into the app container in order for the app to be able to exchange data with other apps.
3. The app need to know the hostname of the redis container, so we set it as an environment variable.
4. Some apps need to know their base URL, so we set it as an environment variable.
    Since the shard's domain name is only known at install time, we need to use the `portal.domain` variable.
    An app's domain name is always `<app-name>.<shard domain>`.
5. We can also use the `portal.short_id` variable to get the shard's six-digit unique identifier.
    This is useful for example to set the title of the app.
6. The app needs the redis password. `secret('redis_password')` generates a random password
    the first time the template is rendered and returns the same value on every later render.
    Read more in the section on [secrets](#secrets).
7. This app need a redis database, so we add a redis container to the docker-compose file.
    The naming convention for additional containers is `my-app-<name>`, where `<name>` is the name of the container.
8. Redis is started with the same secret as its password.
    Because both containers reference the name `redis_password`, they get the same value.
9. We mount a directory for redis to store its data. Note that we use `fs.app_data` just as for the app itself
    so the redis data will be stored in the same directory as the app data.

## Variables

Here is a complete list of all variables that you can use in your template.

### Portal Variables

{!developer_docs/includes/template_vars_portal.md!}

### Filesystem Variables

{!developer_docs/includes/template_vars_fs.md!}

### Secrets

Some values must not be static or predictable, for example the password of a database that only your app talks to.
For these, call the `secret()` helper with a name of your choice:

```yaml
environment:
- POSTGRES_PASSWORD={{ secret('db_password') }}
```

There is nothing to declare beforehand: the name exists as soon as the template references it.
The shard handles it like this:

- The first time a template that references a name is rendered, the shard generates a random value
  of 32 letters and digits (`[A-Za-z0-9]`) and stores it.
- From then on, `secret()` returns that same value for that name.
  It stays the same across app updates, restarts and reinstalls, and it is never rotated.
- Every reference to the same name returns the same value, within one template and across containers.
  Different names get different values.
- Secrets are scoped to your app.
  Another app that uses the same name gets its own, different value.
- Secrets are kept when the app is uninstalled, just like its data,
  so reinstalling the app reuses them.
  They are also part of the shard's backup.

Because the value only contains letters and digits, it can go anywhere in the template without quoting or escaping,
for example inside a connection URL like `postgres://my-app:{{ secret('db_password') }}@my-app-postgres/my-app`.

Note that a secret is tied to its name.
If a later version of your app references `secret('db_pass')` where it used to say `secret('db_password')`,
it gets a new value, and a database that was set up with the old one will no longer accept it.

Secrets are stored unencrypted on the shard.
Scoping keeps apps from colliding on names, it is not a security boundary between apps:
a malicious app template could read other apps' secrets.

The `secret()` helper is available from freeshard version 0.41.2.

## Limitations

Technically, you can use any docker-compose feature in your template.
However, since this would allow you to write apps that break things or are malicious,
we enforce some limitations on what you can do.
When you submit your app for the app store, we will check that it does not violate these limitations.

### Filesystem access

You may not mount any host directories other than the ones provided in the filesystem variables.
And when mounting `fs.all_app_data`, you should have a good reason.

### Docker Socket

You may mount the docker socket into your container, as long as you mount it with the read-only flag.
This is useful for apps that monitor the docker daemon, for example to show the status of other apps.
The mount entry should look like this:

```yaml
volumes:
- "/var/run/docker.sock:/var/run/docker.sock:ro"
```

### Performance

Memory and CPU capacity on a shard vary depending on a shard's size and are never infinite.
So starting a large number of containers or containers that use a lot of resources can slow down the shard.
Also remember that your app might not be the only one running at any time.
If your app is very resource intensive, you should set the `minimum_portal_size` option in the `app_meta.json` to a high value.
