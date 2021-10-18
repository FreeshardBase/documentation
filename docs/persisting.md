# Persisting Data

If your app needs to persist data between restarts or upgrades, 
it can do so by requesting access to a part of the Portal's filesystem.
Use this feature for a database or user-data in the shape of files.
Shared directories allow data exchange between apps.

---

## App-specific directories

For each installed app, Portal creates a separate app-directory inside its filesystem 
and allows the app to mount subdirectories of that directory into itself
by specifying them in the `app.json`.
This feature is based on Docker [bind mounts](https://docs.docker.com/storage/bind-mounts/).

Initially, these directories will be empty and your app can arbitrarily read and write inside them.
If your app is stopped, the mounted directories remain intact and will still be there when your app restarts.
If you release a new version of your app, it is your job to detect 
whether the content of the mounted directories was created by the old version and migrate it if needed.

Use these directories to persist data that is used only by your app.

## Shared directories

!!! warning "Upcoming Feature"
    This feature is not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description. 

Portal defines a set of shared directories like *own media* or *own documents*.
Your app can request read or read-write access to these similar to app-specific directories.
They are mounted inside your app's filesystem at a path that is specified in the `app.json`.

Use these directories to access preexisting user data and share data with other apps that have access.
