---
title: Overview
---

Your app is made up of two distinct artifacts: a collection of docker images that contain the runtime logic of the app
and a collection of files that describe the app's configuration and metadata.
Three files make up the metadata: The `docker-compose.yml.template` works like a normal `docker-compose.yml` file,
but with optional template variables that are replaced by the shard when the app is installed.
The `app_meta.json` file contains additional metadata about the app.
Finally, there is the app's icon.

---

## The App Images

Your app's docker images are run as containers on the user's shard when they install your app.
One of them must contain a web-service which means it must serve HTTP (not HTTPS!) on some port.
Others are typically used by this container to store data or to run background tasks.
These might be databases, message queues, or other services.

How exactly you write your app is up to you.
You may e.g. use rendered templates for each view of your app.
Or you may build a web application that runs in the browser and queries data using a RESTful interface.
You also may use any language or framework you like best.

However, we ask you to make your UI responsive.
Freeshard provides a cross-device user experience, so every app should be equally comfortable to use,
whether on a notebook, tablet or smartphone.

Which additional containers you need is also up to you and depends on your app.
If you have a `docker-compose.yml` file that starts your app, you are already half way there,
because usually this file must only be modified slightly to derive the `docker-compose.yml.template` file.

For many apps, it is sufficient if only the shard's owner can access the app's UI
using the devices they have paired with their shard.
If you want to make part of your app public or usable by the owner's peers,
you can do so by adding appropriate entries in the `app_meta.json`.
See [Routing and Access Control](routing_and_ac.md) to learn how.

At the moment we do not provide hosting for any images.
You can use [Docker Hub](https://hub.docker.com/){target=_blank} or any other docker repository for that.
Or, if for any reason you do not want to host your image, contact us, and we will work something out.

## The App's metadata

While an app's images are hosted on a docker repository, the app's metadata is hosted on the freeshard app store.
Each app has a directory there that contains:

* the `docker-compose.yml.template` file,
* the `app_meta.json` file,
* and the app's icon (optional).

### The `docker-compose.yml.template` File

This file is a template for the `docker-compose.yml` file that is used to start your app's containers.
It is a normal `docker-compose.yml` file with the exception that it may contain template variables
that are replaced by the shard when the app is installed.
This allows you to configure your app's containers for each user individually.
See [the page about `docker-compose.yml.template`](docker_compose_template.md) for details.

### The `app_meta.json` File

Every freeshard app is accompanied by an `app_meta.json` file.
It contains some instructions for the shard about how to run your app.
Examples are the container and port at which your app's UI is published,
or how to manage the app's lifecycle.

In addition, this file contains metadata like the app's name, its version and a description
that will be shown in the app store and other places.

Read more about configuration options on the [page about `app_meta.json`](app_meta_json.md).
