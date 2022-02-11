# The app.json File

For Portal to recognize your app, you have to provide an `app.json` file 
containing some metadata and instructions on how to run your app.

---

## Full Example
```json
{
  "name": "myapp",
  "description": "A Portal app that serves as a simple example",
  "image": "myapp:latest",
  "port": 8080,
  "data_dirs": [
    "/user_data",
    {
      "path": "/more_data",
      "uid": 1000,
      "gid": 1000
    }
  ],
  "services": ["postgres"],
  "env_vars": {
    "DATABASE_URL": "{{ apps[\"myapp\"].postgres.connection_string }}",
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

| field                     | description                                                                                                                                                                                                           |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                      | Your app's name as seen in the app store, on the Portal home screen, and in the URL                                                                                                                                   |
| description               | A short text that is displayed in the app store                                                                                                                                                                       |
| image                     | The docker image reference of your app; this is what you usually use with `docker run`                                                                                                                                |
| port                      | The port at which your app publishes its GUI or API; this port will be forwarded to the user's browser                                                                                                                |
| data_dirs (optional)      | A list of directories inside your image; Portal will create matching directories inside its file system and mount those into them; see [Persisting Data](persisting.md) for details                                   |
| services (optional)       | A list of built-in services that your app uses; Portal will prepare them for you and provide access information in the form of template variables; see [Portal's Internal Services](internal_services.md) for details |
| env_vars (optional)       | A dictionary of environment variables that are set for your app                                                                                                                                                       |
| authentication (optional) | An object which you can use to define access control rules for your app by matching URL-paths to user groups; for more details see [Routing and Access Control](routing_and_ac.md)                                    |

## Templating

You can include variables in your `app.json` that are substituted during install time.
They help you include values that are specific to each individual Portal.
Use Jinja-like double curly brackets for this.

### Example

With this snippet, you can tell your app the actual full domain at which it is published.

```json
"env_vars": {
  "url": "https://myapp.{{ portal.domain }}/"
}
```

### Variables

| variable        | description                                   | example                                                                                                   |
|-----------------|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `portal.domain` | The fully qualified domain name of the Portal | `8271dd.p.getportal.org`                                                                                  |
| `portal.id`     | The full-length hash-ID of the Portal         | `8271ddlqxa5fcp7a5l0s61pbqqtglba31d65jg2fqhdwdw2kkr7l94b2q54hfdl2zfn5s5g1nkjy1z1a3f02tl8yln14050l8s598f2` |

More variables are provided by Portal's built-in services if your app defines them as dependencies.
See [Portal's Internal Services](internal_services.md) for details.