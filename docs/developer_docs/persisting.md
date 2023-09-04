---
title: Persisting Data
---

If your app needs to persist data between restarts or upgrades, 
it can do so by mounting a directory of the Portal's file system.
Use this feature for a database or user-data in the shape of files.
Shared directories allow data exchange between apps.

---

## App-specific directories

For each installed app, Portal creates a separate app-directory inside its file system.
You can mount subdirectories of this directory into your app's file system
by using the `fs.app_data` variable in the `docker-compose.yml.template`.

Initially, this directory will be empty and your app can arbitrarily read and write inside it.
If your app is stopped, the mounted directories remain intact and will still be there when your app restarts.
If you release a new version of your app, it is your job to detect 
whether the content of the mounted directories was created by the old version and migrate it if needed.

Use this app-specific directory to persist data that is used only by your app.

### Example

In the `docker-compose.yml.template`:

```yaml
        volumes:
        - "{{ fs.app_data }}/data:/data"
```

## Shared directories

Portal defines a single shared directory.
You can mount it or subdirectories of it into your app's file system,
allowing your app to access preexisting user data and share data with other apps that have access to the same directories.
Use the `fs.shared` variable in the `docker-compose.yml.template`.

Examples of shared directories are:

* `documents`
* `media`
* `music`

### Example

In the `docker-compose.yml.template`:

```yaml
        volumes:
        - "{{ fs.shared }}/documents:/documents"
```
