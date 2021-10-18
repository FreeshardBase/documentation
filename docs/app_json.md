# The app.json File

In order for Portal to recognize your app, you have to provide an `app.json` file 
containing some metadata and instruction on how to run your app.

---

## Full Example
```json
{
  "name": "my-app",
  "description": "A Portal app that serves as a simple example",
  "image": "my-app:latest",
  "port": 8080,
  "data_dirs": [
    "/user_data"
  ],
  "env_vars": {
    "DEBUG": "true"
  },
  "authentication": {
    "default_access": "private",
    "public_paths": ["/public/"],
    "peer_paths": ["/peer/"]
  }
}
```

## Description of Fields

| field | description
|---|---|
| name | Your app's name as seen in the app store, on the Portal home screen, and in the URL |
| description | A short text that is displayed in the app store |
| image | The docker image reference of your app; this is what you usually use with `docker run` |
| port | The port at which your app publishes its UI or API; this port will be forwarded to the user's browser |
| data_dirs | A list of directories inside your image; Portal will create matching directories inside its filesystem and mount those into them; see [bind mounts](https://docs.docker.com/storage/bind-mounts/) for details |
| env_vars | A dictionary of environment variables that are set for your app |
| authentication | An object which you can use to define access control rules for your app by matching URL-paths to user groups; for more details see [Routing and Access Control](routing_and_ac.md) |
