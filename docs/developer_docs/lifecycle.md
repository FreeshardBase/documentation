---
title: The App Lifecycle
---

Portal starts and stops installed apps on demand and lets you configure this behaviour.

---

## Installation and Creation

When a user installs your app, the image is pulled and a container is created.
However, the app is not started yet.
Basically, the following command is executed.

```shell
docker-compose up --no-start
```

## Start

The Portal's reverse proxy forwards all http traffic to your app and takes care of authentication and other concerns.
This is described in detail under [Routing and Access Control](routing_and_ac.md).
One of its tasks is to inform the Portal core of incoming traffic to an app
such that the app can be started if it is not running.
Since the container was created during installation, only the `docker start` command is issued.

During the time it takes for the app to start, a splash screen is displayed and regularly refreshed.
This splash screen is provided by the Portal core and as an app developer, you do not have to do anything.

## Stop

After some idle time - i.e. a time period without http traffic to an app - the Portal core stops the app.
The container is only stopped, but not removed. Essentially, the `docker stop` command is issued.

## Configuration

You may configure your apps lifecycle behaviour via the `lifecycle` section inside the `app_meta.json`.
For example:

```json
  "lifecycle": {
    "always_on": false,
    "idle_time_for_shutdown": 60
  },
```

You may set `always_on` to `true` causing your app to never be stopped.
In this case, providing an `idle_time_for_shutdown` is forbidden.

Or you may set and `idle_time_for_shutdown` in seconds.
The default is `60`.
In this case, `always_on` must not be set or set to `false`.
