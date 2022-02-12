# Persisting Data

If your app needs to persist data between restarts or upgrades, 
it can do so by requesting access to a part of the Portal's file system.
Use this feature for a database or user-data in the shape of files.
Shared directories allow data exchange between apps.

---

## App-specific directories

For each installed app, Portal creates a separate app-directory inside its file system 
and allows the app to mount subdirectories of that directory into itself
by specifying them in the `app.json`.
This feature is based on Docker [bind mounts](https://docs.docker.com/storage/bind-mounts/).

Initially, these directories will be empty and your app can arbitrarily read and write inside them.
If your app is stopped, the mounted directories remain intact and will still be there when your app restarts.
If you release a new version of your app, it is your job to detect 
whether the content of the mounted directories was created by the old version and migrate it if needed.

You might not want to run your application as root inside your container but as some other user.
In this case, it would not have access to the mounted directories, since they are owned by root.
In order to allow access, you can change the mounted directories' owner by defining its user and group id.
Set it to the values of the user that runs the app.

Use these app-specific directories to persist data that is used only by your app.

### Example

```json
...
  "data_dirs": [
    "/user_data",
    {
      "path": "/more_data",
      "uid": 1000,
      "gid": 1000
    }
  ],
...
```

## Shared directories

!!! warning "Upcoming Feature"
    Shared directories are not yet implemented.
    You cannot use them yet and their implementation - when completed - might differ from this description. 

Portal defines a set of shared directories like *own media* or *own documents*.
Your app can request read or read-write access to these similar to app-specific directories.
They are mounted inside your app's file system at a path that is specified in the `app.json`.

Use these directories to access preexisting user data and share data with other apps that have access.

## Built-In Services

Each Portal runs some built-in services that your app may use.
For example, your app can get its own database at the Portal's Postgres instance
and use it to store its data.
Take a look at the [section about Portal's internal services](internal_services.md) for more information.
