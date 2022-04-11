# Portal's Internal Services

The core software stack that manages a Portal offers several services to installed apps.
Use them by making REST requests against their APIs.
Also let your app request access to shared services like a database.

---

!!! danger "Unsafe API"
    Right now, the APIs described here are accessible without any checks.
    Your app can view, modify, and delete critical information about the Portal
    and even completely break it.
    This will of course be locked down in the future, but for now: be careful what you do!

## Portal Core

The Portal core software stack is what manages all of a Portal's operations
like its identities, terminals, peers or apps.
It provides a [REST API](https://ptl.gitlab.io/portal_core/) that your app may use.
Its base URL is `http://portal_core`. For example, you can list all apps by calling
`GET http://portal_core/protected/apps`.

## Postgres

There is a Postgres instance running on every Portal
and your app can request its own database on it.
Enable it in the `app.json` by adding `postgres` under the section `services`.
Then, you can pass the needed connection information as environment variables
by using template strings.

For example, include `"DATABASE_URL": "{{ postgres.connection_string }}"`
in the `env_vars` section, to pass the whole postgres connection string.
All variables related to postgres start with `postgres.`. Here is a full list of variables you may use.

| variable            | example                                           |
|---------------------|---------------------------------------------------|
| `connection_string` | `postgres://myapp:mypassword@postgres:5432/myapp` |
| `userspec`          | `myapp:mypassword`                                |
| `user`              | `myapp`                                           |
| `password`          | `mypassword`                                      |
| `hostspec`          | `postgres:5432`                                   |
| `host`              | `postgres`                                        |
| `port`              | `5432`                                            |

## Docker Socket

Portal makes heavy use of Docker.
The Portal core, the reverse proxy, and every app are all realized as Docker containers.
Apps that need to read the state of the Docker daemon may get read-only access to the Docker socket
by adding `docker_sock_ro` under the section `services`.

This causes the Docker socket to be mounted into the app container.
It is equivalent to the option `-v /var/run/docker.sock:/var/run/docker.sock:ro` of the Docker CLI.

No app can get read-access to the Docker socket, that is the privilege of the Portal core.

## Peer Routing

!!! warning "Upcoming Feature"
    Peering is not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description.

## Other Apps

Your app can contact other apps that are installed on the same Portal
if they offer an API for this.

!!! warning "Upcoming Feature"
    Inter-App APIs are not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description.