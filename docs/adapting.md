# Adapting an existing App

A Portal App is essentially a Docker container with a web interface.
This technical simplicity makes it easy to adapt many existing apps to run on Portal and benefit from its features.

---

## Hosting an existing App on Portal

It is a common practice to publish apps for self-hosting as Docker images.
That makes deployment and setup easy and standardized.

If an app has no other dependencies (like a database or cache), it can very easily be hosted on Portal.
You just need to write a minimal `app.json` containing a name, the Docker image reference and the port of the web interface or API ([details here](app_json.md)).
If it needs to persist data, mount a directory by adding a `data_dirs` entry.
After writing the `app.json`, paste it into the *Custom App* field as described [here](testing.md).

The app will now run on your Portal and you can access its web interface from any paired device.
If you want to make parts or all of the app publicly accessible, [read about access control](routing_and_ac.md).

## Basic Adaptations

Usually, apps for self-hosting work on Portal and benefit from hosting and access control.
However, some assumptions of self-hosting are different in the Portal ecosystem
which often leads to awkward user experience.
Luckily, those can be often dealt with rather easily.

### User Management

### Access Control

## Advanced Adaptations

### Peer-2-Peer Communication

### Publishing and Subscribing to Events
