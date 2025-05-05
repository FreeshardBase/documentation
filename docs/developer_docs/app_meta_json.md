---
title: The app_meta.json File
---

A shard must know a few things about your app that cannot be configured in the `docker-compose.yml.template` file
because they are specific to how the shard treats your app.
This is what the `app_meta.json` file is for.

---

{!developer_docs/includes/portal_name_info.md!}

## Full Example

This is a complete example of an `app_meta.json` file.
Click on the plus buttons for a description of each field.

```json
{
  "v": "1.2", // (1)!
  "app_version": "0.1.1", // (2)!
  "name": "my-app", // (3)!
  "pretty_name": "My App", // (10)!
  "icon": "icon.png", // (4)!
  "homepage": "https://myapp.com", // (12)!
  "upstream_repo": "https://github.com/namespace/myapp", // (11)!
  "entrypoints": [ // (5)!
    {
      "container_name": "my-app",
      "container_port": 8080,
      "entrypoint_port": "http"
    }
  ],
  "paths": { // (6)!
    "": {
      "access": "private"
    }
  },
  "lifecycle": { // (7)!
    "always_on": false,
    "idle_time_for_shutdown": 3600
  },
  "minimum_portal_size": "s", // (8)!
  "store_info": { // (9)!
    "description_short": "This is a very good app.",
    "description_long": [
      "This app is so good, you won't believe it.",
      "It is the best app ever."
    ],
    "hint": "Although this app is very good, you still have to create an account to use it.",
    "is_featured": true
  }
}
```

1. The version of the `app_meta.json` format. Should be "1.2".
2. The version of your app. This is used to determine if an update is available.
    It is recommended to match with your own versioning scheme.
3. The name of your app as seen in the URL.
    It must be unique across all apps in the app store.
    It can only contain lowercase letters, numbers, and dashes.
4. The name of the icon file that you must provide alongside the `app_meta.json` file.
    It may be a PNG or JPEG or SVG file of any size, but it would be best if it is not huge.
5. This is where you configure the ports that your app exposes to the internet.
    * The `container_name` is the name of the container that you defined in the `docker-compose.yml.template` file.
    * The `container_port` is the port that your app is listening on inside the container.
    * The `entrypoint_port` is the port that you want to expose to the internet.
        It can be `http` (mapped to 443) or `mqtt` (mapped to 8883).
6. Here you can configure the access control for your app.
    It is a mapping of path prefixes to access control settings.
    The empty string `""` is the default and will be used for all paths that are not explicitly configured.
    Read more about access control [here](routing_and_ac.md).
7. Most freeshard apps do not run continuously but are started on demand and stopped after an idle period.
    This is where you can configure this behavior. Read more about it [here](lifecycle.md).
8. This is the minimum size of a managed shard that is required to run your app 
    and should be set according to your app's CPU and memory requirements.
    If you do not specify this, your app will be available on all VM sizes.
9. This is where you can configure the information that is displayed in the app store.
    See [Submitting to the App Store](submitting.md) for more information.
10. The name of your app as seen in the app store and below the icon on the shard home screen.
    It can be different from the `name` field and may include uppercase letters and spaces.
11. (Optional) The URL of the repository where the source code of your app is hosted.
    Right now, this is only used for automatically checking for updates.
    It only works with GitHub repositories which use the "Release" feature.
12. (Optional) The URL of the homepage of your app.
    This is where users can find more information about your app.

## Schema

To help you write your `app_meta.json` file,we publish a JSON schema that describes the format 
[here](https://storageaccountportab0da.blob.core.windows.net/json-schema/0-30-2/schema_app_meta_1.2.json).
Add it to your IDE to get auto-completion and validation.
Here is a guide for [Visual Studio Code](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings){target=blank}
and one for [PyCharm](https://www.jetbrains.com/help/pycharm/json.html#ws_json_schema_add_custom){target=blank}.

## Versioning

Since the format of the `app_meta.json` evolves over time,
it is important to include the version of the format in which it is written.
It is contained in the `v` attribute.
The current version is `1.2`.

When new versions are released, we will attempt to make them backwards compatible.
That means that freeshard still can process the previous version
and translate it to the current one.

### Past Updates

#### Version 1.2

* Added the `homepage` and `upstream_repo` fields.

#### Version 1.1

* Added the `pretty_name` field.
