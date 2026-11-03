---
title: The App Lifecycle
---

A shard starts and stops installed apps on demand and lets you configure this behaviour.

---

## Installation and Creation

When a user installs your app, the image is pulled and the containers are created.
However, the app is not started yet.
Basically, the following command is executed.

```shell
docker-compose up --no-start
```

## Start

The shard's reverse proxy forwards all http traffic to your app and takes care of authentication and other concerns.
This is described in detail under [Routing and Access Control](routing_and_ac.md).
One of its tasks is to inform the shard core of incoming traffic to an app
such that the app can be started if it is not running.

During the time it takes for the app to start, a splash screen is displayed and regularly refreshed.
This splash screen is provided by the shard core and as an app developer,
you do not have to do anything to make it work.

## Pause and Stop

After some idle time - i.e. a time period without http traffic to an app - the shard core pauses the app.
Its containers are frozen and their memory is moved to swap, so a paused app uses almost no memory
but resumes quickly on the next request.

After a longer idle time, a paused app is stopped.
The container is only stopped, but not removed. Essentially, the `docker-compose stop` command is issued.
A stopped app is started again on the next request, as described above.

When the shard runs low on memory, it pauses or stops the least recently used apps before their idle time is reached,
one app at a time until enough memory is free.
When the shard runs low on disk space, it stops all apps.

## Configuration

You may configure your apps lifecycle behaviour via the `lifecycle` section inside the `app_meta.json`.
For example:

```json
  "lifecycle": {
    "idle_for_pause": 300,
    "idle_for_stop": 3600
  },
```

All fields are optional. Times are given in seconds.

| field            | description                                                        | default         |
|------------------|--------------------------------------------------------------------|-----------------|
| `idle_for_pause` | Idle time after which the app is paused                            | `60`            |
| `idle_for_stop`  | Idle time after which the app is stopped                           | `10800` (3 hours) |
| `skip_pause`     | If `true`, the app is never paused, only stopped after `idle_for_stop` | `false`     |
| `always_on`      | If `true`, the app is never paused or stopped                      | `false`         |

Some rules apply to their combination:

- Both idle times must be at least `5`, and `idle_for_pause` must be less than `idle_for_stop`.
- Set `skip_pause` for apps that do not tolerate being frozen.
  Providing an `idle_for_pause` together with it is forbidden.
- If `always_on` is `true`, providing any other lifecycle field is forbidden.
  An always-on app is still stopped when the shard runs low on disk space.

Note that pausing can be switched off on a shard.
In that case, apps are not paused but only stopped after `idle_for_stop`.

In version 1.2 of the `app_meta.json` format and earlier, this section had a single `idle_time_for_shutdown` field.
Freeshard still reads it from files in those versions and treats it as `idle_for_pause`.
