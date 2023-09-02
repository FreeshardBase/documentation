# The Docker-Compose Template

When starting an app, Portal simply brings up a docker-compose file just like you would with `docker-compose up`.
This file is generated during installation of the app from a `docker-compose.yml.template` that you have to provide.
This template is a normal docker-compose file with some special variables that Portal will replace with the correct values.

---

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

1. This is the network that Portal uses to connect all apps together and to the reverse proxy and Portal core.
    You need to include this in your template.
2. This is the image that will be used for your app. Please specify a fixed version, not just `my-app:latest`.
   When you update your app, you will also need to release a new version of the metadata including a new template.
3. You must explicitly set the container name, and it must match with the service name.
4. In order to persist data, you need to mount a host directory.
   For data that only concerns your app, you should use the `fs.app_data` variable
   and a subdirectory that matches the directory inside the container.
5. You need to connect your app to the `portal` network specified above.

## Complex Example

Now let's look at a more complex example.
Here we have an app that depends on a redis database and has some environment variables that need to be set.
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

    my-app-redis: # (6)!
        image: redis:6.2
        container_name: my-app-redis
        expose:
        - 6379
        volumes:
        - "{{ fs.app_data }}/redis_data:/redis_data" # (7)!
        networks:
        - portal
```

1. The app container depends on the redis container, so that the redis container will be started first.
2. We mount the shared data directory into the app container in order for the app to be able to exchange data with other apps.
3. The app need to know the hostname of the redis container, so we set it as an environment variable.
4. Some apps need to know their base URL, so we set it as an environment variable.
    Since the Portal's domain name is only known at install time, we need to use the `portal.domain` variable.
    An app's domain name is always `<app-name>.<portal domain>`.
5. We can also use the `portal.short_id` variable to get the Portal's six-digit unique identifier.
    This is useful for example to set the title of the app.
6. This app need a redis database, so we add a redis container to the docker-compose file.
    The naming convention for additional containers is `my-app-<name>`, where `<name>` is the name of the container.
7. We mount a directory for redis to store its data. Note that we use `fs.app_data` just as for the app itself
    so the redis data will be stored in the same directory as the app data.

## Variables

Here is a complete list of all variables that you can use in your template.

### Portal Variables

{!developer_docs/includes/template_vars_portal.md!}

### Filesystem Variables

{!developer_docs/includes/template_vars_fs.md!}

## Limitations

Technically, you can use any docker-compose feature in your template.
However, since this would allow you to write apps that break things or are malicious,
we enforce some limitations on what you can do.
When you submit your app for the app store, we will check that it does not violate these limitations.

### Filesystem access

You may not mount any host directories other than the ones provided in the filesystem variables.
And when mounting `fs.app_data`, you should have a good reason.

### Performance

Memory and CPU capacity on a Portal vary depending on a Portal's size and are never infinite.
So starting a large number of containers or containers that use a lot of resources can slow down the Portal.
Also remember that your app might not be the only one running at any time.
If your app is very resource intensive, you should set the `min_portal_size` option in the `app_meta.json` to a high value.
