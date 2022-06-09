# The app.json File

For Portal to recognize your app, you have to provide an `app.json` file containing some metadata and instructions on
how to run your app.

---

The `app.json` contains all metadata about your app.
It tells the Portal what to run by defining a docker image and how to run it.
And it contains information that is important to display in the app store,
like the official name and a description.

## Full Example

```json
{
  "v": "3.1",
  "name": "myapp",
  "image": "myapp:1.2.3",
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
    "DATABASE_URL": "{{ postgres.connection_string }}",
    "DEBUG": "true"
  },
  "paths": {
    "": {
      "access": "private",
      "headers": {
        "X-Ptl-Client-Id": "{{ client_id }}",
        "X-Ptl-Client-Name": "{{ client_name }}",
        "X-Ptl-Client-Type": "{{ client_type }}",
        "X-Ptl-Foo": "bar"
      }
    },
    "/public/": {
      "access": "public",
      "headers": {
        "X-Ptl-Client-Type": "{{ client_type }}",
        "X-Ptl-Foo": "baz"
      }
    }
  },
  "lifecycle": {
    "always_on": false,
    "idle_time_for_shutdown": 60
  },
  "store_info": {
    "description_short": "A great app",
    "description_long": [
      "A really great app that serves as an example.",
      "It also has a description that is two paragraphs long."
    ],
    "hint": [
      "This app is not really part of the app store",
      "In fact, this app does not really exist"
    ],
    "is_featured": true
  }
}
```

## Description of Fields

| field                 | description                                                                                                                                                                                                           |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| v                     | The version of the app.json format. Should be "3.1".                                                                                                                                                                  |
| name                  | Your app's name as seen in the app store, on the Portal home screen, and in the URL                                                                                                                                   |
| image                 | The docker image reference of your app; this is what you usually use with `docker run`                                                                                                                                |
| port                  | The port at which your app publishes its GUI or API; this port will be forwarded to the user's browser                                                                                                                |
| data_dirs (optional)  | A list of directories inside your image; Portal will create matching directories inside its file system and mount those into them; see [Persisting Data](persisting.md) for details                                   |
| services (optional)   | A list of built-in services that your app uses; Portal will prepare them for you and provide access information in the form of template variables; see [Portal's Internal Services](internal_services.md) for details |
| env_vars (optional)   | A dictionary of environment variables that are set for your app                                                                                                                                                       |
| paths                 | An object which you can use to define access control rules for your app by defining how each URL path should be handled; for more details see [Routing and Access Control](routing_and_ac.md)                         |
| lifecycle             | An object which defines if and when your app is automatically shut down in order to conserve resources.                                                                                                               |
| store_info (optional) | Information that is read by the app store and displayed there.                                                                                                                                                        |

## Templating for environment variables

You can include variables in the values of the `env_vars` section that are substituted during install time.
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

{!includes/template_vars_portal.md!}

More variables are provided by Portal's built-in services if your app defines them as dependencies.
See [Portal's Internal Services](internal_services.md) for details.

## Versioning

Since the format of the `app.json` evolves over time,
it is important to include the version of the format in which it is written.
It is contained in the `v` attribute.
The current version is `3.1`.

When new versions are released, we will attempt to make them backwards compatible.
That means that Portal still can process the previous version
and translate it to the current one.

### Past Updates

#### version `3.0` to version `3.1`

* Added the `lifecycle` section.

#### version `2.0` to version `3.0`

* Changed the way, variables of internal services are addressed by `env_vars` templates. Example before: `{{ apps[\"myapp\"].postgres.connection_string }}` vs. example after: `{{ postgres.connection_string }}`.

#### version `1.0` to version `2.0`

* Removed the `description` field and instead added the `store_info` section.

#### version `0.0` to version `1.0`

* Removed the `authentication` section and instead added the `paths` section.
* Added the `v` attribute to indication the schema version - an `app.json` without `v` is assumed to be version `0.0`.
