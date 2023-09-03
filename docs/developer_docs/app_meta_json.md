# The app_meta.json File

A Portal must know a few things about your app that cannot be configured in the `docker-compose.yml.template` file
because they are specific to how Portal treats your app.
This is what the `app_meta.json` file is for.

---

## Full Example

This is a complete example of an `app_meta.json` file.
Click on the plus buttons for a description of each field.

```json
{
  "v": "1.0", // (1)!
  "app_version": "0.1.1", // (2)!
  "name": "my-app", // (3)!
  "icon": "icon.png", // (4)!
  "entrypoints": [ // (5)!
    {
      "container_name": "actual",
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
    "description_short": "Enjoy managing your finances",
    "description_long": [
      "Enjoy managing your finances",
      "Actual is a super fast privacy-focused app for managing your finances. You own your data, and we will sync it across all devices with optional end-to-end encryption."
    ],
    "hint": "The app prompts you to set a password on first launch. You can choose a simple one, Portal secures the app separately.",
    "is_featured": true
  }
}
```

1. The version of the `app_meta.json` format. Should be "1.0".
2. The version of your app. This is used to determine if an update is available.
    It can but does not have to match with your own versioning scheme.
3. The name of your app as seen in the app store, on the Portal home screen, and in the URL.
    It must also match the name of the container and the service in the `docker-compose.yml.template` file.
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
7. Most Portal apps do not run continuously but are started on demand and stopped after an idle period.
    This is where you can configure this behavior.
8. This is the minimum size of a Portal that is required to run your app 
    and should be set according to your app's CPU and memory requirements.
    If you do not specify this, your app will be available on all Portal sizes.
9. This is where you can configure the information that is displayed in the app store.
    * The `description_short` is a short description that is on the app card.
    * The `description_long` is a longer description that is displayed when the user clicks on the app card.
      It can be a list of strings, each of which will be displayed as a paragraph.
    * The `hint` is a short text that you can use to describe limitations of your app.
    * The `is_featured` flag determines if your app is featured in the app store.
      We will only feature apps that are of high quality and integrate well with Portal.

## Schema

To help you write your `app_meta.json` file,we publish a JSON schema that describes the format 
[here](https://storageaccountportab0da.blob.core.windows.net/json-schema/0-21-0/schema_app_meta_1.0.json).
Add it to your IDE to get auto-completion and validation.
Here is a guide for [Visual Studio Code](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings)
and one for [PyCharm](https://www.jetbrains.com/help/pycharm/json.html#ws_json_schema_add_custom).

## Versioning

Since the format of the `app_meta.json` evolves over time,
it is important to include the version of the format in which it is written.
It is contained in the `v` attribute.
The current version is `1.0`.

When new versions are released, we will attempt to make them backwards compatible.
That means that Portal still can process the previous version
and translate it to the current one.

### Past Updates

This is where we will list and describe all changes to the `app_meta.json` format.
