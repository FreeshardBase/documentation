# Persisting Data

If your app needs to persist data between restarts or upgrades, 
it can do so by requesting access to a part of the Portal's filesystem.
Use this feature for a database or user-data in the shape of files.

---

For each installed app, Portal creates a separate app-directory inside its filesystem 
and allows the app to mount subdirectories of that directory into itself.
This feature is based on Docker's [bind mount](https://docs.docker.com/storage/bind-mounts/) feature.
The content of these mounted directories can be arbitrarily modified by your app.

If your app is stopped, the mounted directories remain intact and will still be there when your app restarts.
If you release a new version of your app, it is your job to detect whether the content of the mounted directories
was created by the old version and migrate it if needed.