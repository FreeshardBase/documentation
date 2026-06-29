# Freeshard Developer Docs — Digest

> AI-optimized digest of the Freeshard developer documentation. Intended for
> coding agents (e.g. the app-repository `add-app` skill) that build and submit
> Freeshard apps. Authoritative copy of `docs.freeshard.net/developer_docs`.
>
> Generated: 2026-06-29
> Source: github.com/FreeshardBase/documentation
> Regenerate with the repo-local `generate-digest` skill (`.claude/skills/generate-digest/`).

> Naming note: the project used to be called *Portal*. Some variables and API
> paths still use the old name (`portal.*`, `shard_core` was `portal_core`) for
> backwards compatibility. Treat "portal" and "shard" as the same thing.

## What Freeshard is

A personal cloud computer for consumers. Each owner gets their own isolated
virtual machine + disk, called a **shard** (single-user, not multi-tenant).
Apps are installed from an app store and run on the shard; the owner reaches them
remotely from paired devices.

Key consequences for app developers:

- **Single user, no login.** Each app instance serves exactly one owner. Don't
  build user management / registration; the shard authenticates requests for you.
  Disable an existing app's account system or switch it to proxy authentication.
- **Always-on cloud host** with a local filesystem the app can persist to.
- **Cross-device**: make the UI responsive (notebook, tablet, smartphone).
- Freeshard already provides: TLS/certificates, user auth, contact/peer lists,
  hosting, backups, and developer compensation (revenue share).

## App anatomy

An app is two artifacts:

1. **Docker images** — the runtime. At least one container must serve **HTTP
   (not HTTPS) on a port**. Other containers (DBs, queues, workers) are optional.
   Images are hosted by you on Docker Hub or any registry (Freeshard does not
   host images).
2. **Metadata** in the app store: `docker-compose.yml.template`, `app_meta.json`,
   and an optional icon file.

Routing: each shard has a six-digit ID and URL `xyz123.<domain>`. Each app is
served at `<app-name>.xyz123.<domain>`. HTTP requests to that subdomain are
forwarded to the container/port named in `app_meta.json` `entrypoints`.

## `docker-compose.yml.template`

A normal docker-compose file plus Jinja-style `{{ ... }}` template variables that
the shard substitutes at install time. The shard runs it like `docker-compose up`.

Minimal example:

```yaml
version: '3.5'

networks:
    portal:          # shard network connecting apps, reverse proxy, core — required
        external: true

services:
    my-app:
        image: my-app:v4          # use a fixed version, never :latest
        container_name: my-app     # must match the service name
        volumes:
        - "{{ fs.app_data }}/data:/data"   # persist data, see Persisting
        networks:
        - portal                   # must join the portal network
```

Complex example (dependency container + env vars + shared dir):

```yaml
version: '3.5'

networks:
    portal:
        external: true

services:
    my-app:
        image: my-app:v4
        container_name: my-app
        depends_on:
        - my-app-redis
        volumes:
        - "{{ fs.app_data }}/data:/data"
        - "{{ fs.shared }}/shared_data:/shared_data"
        networks:
        - portal
        environment:
        - REDIS_HOST=my-app-redis
        - BASE_URL=https://my-app.{{ portal.domain }}   # app domain = <app-name>.<shard domain>
        - TITLE=My app on {{ portal.short_id }}

    my-app-redis:                  # extra containers named my-app-<name>
        image: redis:6.2
        container_name: my-app-redis
        volumes:
        - "{{ fs.app_data }}/redis_data:/redis_data"   # use fs.app_data, same dir tree as the app
        networks:
        - portal
```

### Template variables

Portal (shard) variables:

| variable                | description                                  | example                       |
|-------------------------|----------------------------------------------|-------------------------------|
| `portal.domain`         | Fully qualified domain name of the shard     | `8271dd.<domain>`             |
| `portal.id`             | Full-length hash-ID of the shard             | `8271ddlqxa…8s598f2`          |
| `portal.short_id`       | First six digits of the shard's hash-ID      | `8271dd`                      |
| `portal.public_key_pem` | Shard's public key in PEM format             | `-----BEGIN PUBLIC KEY-----…` |

Filesystem variables:

| variable              | description                                       | example                                            |
|-----------------------|---------------------------------------------------|----------------------------------------------------|
| `fs.app_data`         | Absolute path to your app's data directory        | `/home/user/.freeshard/user_data/app_data/my-app`  |
| `fs.all_app_data`     | Absolute path to the app-data parent directory    | `/home/user/.freeshard/user_data/app_data`         |
| `fs.shared`           | Absolute path to the shared data directory        | `/home/user/.freeshard/user_data/shared`           |
| `fs.installation_dir` | Absolute path to your installation files          | `/home/user/.freeshard/core/installed_apps/my-app` |

### Limitations (enforced on app-store submission)

- **Filesystem**: mount only the directories exposed via `fs.*` variables. Have a
  good reason before mounting `fs.all_app_data`.
- **Docker socket**: may be mounted read-only only:
  `- "/var/run/docker.sock:/var/run/docker.sock:ro"`.
- **Performance**: shard CPU/memory is finite and shared with other apps. If your
  app is resource-heavy, set a high `minimum_portal_size` in `app_meta.json`.

## `app_meta.json`

Tells the shard how to run and present the app. Current format version `v` =
`"1.2"`. Full example:

```json
{
  "v": "1.2",
  "app_version": "0.1.1",
  "name": "my-app",
  "pretty_name": "My App",
  "icon": "icon.png",
  "homepage": "https://myapp.com",
  "upstream_repo": "https://github.com/namespace/myapp",
  "entrypoints": [
    {
      "container_name": "my-app",
      "container_port": 8080,
      "entrypoint_port": "http"
    }
  ],
  "paths": {
    "": {
      "access": "private"
    }
  },
  "lifecycle": {
    "always_on": false,
    "idle_time_for_shutdown": 3600
  },
  "minimum_portal_size": "s",
  "store_info": {
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

Field reference:

- `v` — `app_meta.json` format version, should be `"1.2"`.
- `app_version` — your app's version; used for update detection. Match your own scheme.
- `name` — URL name, **unique across the app store**, lowercase letters/numbers/dashes only.
- `pretty_name` — display name (app store + home screen); may have uppercase/spaces.
- `icon` — icon filename you ship alongside (PNG/JPEG/SVG, keep it small).
- `homepage` — *(optional)* app homepage URL.
- `upstream_repo` — *(optional)* source repo URL; only used for update checks, GitHub Releases only.
- `entrypoints[]` — ports exposed to the internet:
  - `container_name` — container from the compose template.
  - `container_port` — port the app listens on inside the container.
  - `entrypoint_port` — `http` (→443) or `mqtt` (→8883).
- `paths` — access control by path prefix (see below). Must include `""` default.
- `lifecycle` — start/stop behavior (see Lifecycle).
- `minimum_portal_size` — min shard size required (e.g. `"s"`); omit = all sizes.
- `store_info` — app-store display metadata (see Submitting).

JSON schema (add to IDE for autocompletion/validation):
`https://storageaccountportab0da.blob.core.windows.net/json-schema/0-30-2/schema_app_meta_1.2.json`

Version history: **1.2** added `homepage` + `upstream_repo`; **1.1** added
`pretty_name`. New versions aim to be backwards compatible (older files are
translated to current).

## Routing and access control

Requests to `<app-name>.<shard-id>.<domain>` are routed and authenticated by the
shard core per `app_meta.json`. You don't handle TLS — each shard manages a
certificate covering all its subdomains; your app just serves HTTP.

MQTT entrypoints can be forwarded too, but are **public by default** and are NOT
protected by shard access control — add your own.

### `paths` access control (HTTP only)

`paths` maps path prefixes to access settings. Matching is **longest prefix
first**; you **must** include `""` as the final default. Access types:

- `public` — anyone.
- `private` — only paired devices (the owner's). Default behavior.
- `peer` — shards added as peers.

After auth, the shard injects headers you define for the matched path. Header
values may use `{{ ... }}` variables:

| variable           | description                                 | example                             |
|--------------------|---------------------------------------------|-------------------------------------|
| `auth.client_type` | Type of client that sent the request        | `terminal` / `peer` / `anonymous`   |
| `auth.client_id`   | Cryptographic ID of the Terminal or Peer    | `eie767`                            |
| `auth.client_name` | User-assigned name of the Terminal or Peer  | `my notebook`                       |

(plus all `portal.*` variables above.)

Two patterns:

- **Path-based AC** — let the shard enforce access by prefix. Example: default
  `private`, expose `/public/` as `public`:

  ```json
  "paths": {
    "": {
      "access": "private",
      "headers": {
        "X-Ptl-Client-Id": "{{ auth.client_id }}",
        "X-Ptl-Client-Name": "{{ auth.client_name }}",
        "X-Ptl-Client-Type": "{{ auth.client_type }}"
      }
    },
    "/public/": { "access": "public" }
  }
  ```

- **App-specific AC** — set everything `public` so all requests reach the app, but
  still receive identity headers and enforce access yourself in app code.

If the app is only for the owner, you need no AC config — `private` default
already restricts it to paired devices.

## Persisting data

Mount shard filesystem directories into the app to persist across restarts/upgrades.

- **App-specific**: each app gets its own directory via `fs.app_data`. Starts
  empty; persists across stop/restart. On a new app version, you are responsible
  for detecting and migrating old data. Use for app-private data (DBs, files).
  `- "{{ fs.app_data }}/data:/data"`
- **Shared**: one shared directory per shard via `fs.shared`, for exchanging data
  with other apps and accessing preexisting user data. Subdirs e.g. `documents`,
  `media`, `music`.
  `- "{{ fs.shared }}/documents:/documents"`

## App lifecycle

The shard starts/stops apps on demand to conserve resources.

- **Install**: images pulled, containers created but not started
  (`docker-compose up --no-start`).
- **Start**: triggered by incoming HTTP traffic; the shard core starts the app and
  shows a self-refreshing splash screen meanwhile (provided by the shard, no work
  for you).
- **Stop**: after idle time with no HTTP traffic, `docker-compose stop` (containers
  stopped, not removed).

Configure via `lifecycle` in `app_meta.json`:

```json
"lifecycle": {
  "always_on": false,
  "idle_time_for_shutdown": 60
}
```

- `always_on: true` → never stopped; then `idle_time_for_shutdown` is **forbidden**.
- `idle_time_for_shutdown` (seconds, default `60`) → requires `always_on` unset/false.

## Shard internal services

Core services reachable from apps via REST.

> **Unsafe API warning**: these APIs currently have no access checks — an app can
> view/modify/delete critical shard state. To be locked down later; be careful.

- **Shard core** at base URL `http://shard_core`. Manages identities, terminals,
  peers, apps. Example: `GET http://shard_core/protected/apps` lists apps.
  Full API docs: `https://ptl.gitlab.io/portal_core/`.
- **Other apps** (inter-app APIs): *upcoming / not yet implemented.*

## Peering (status: disabled)

> Currently disabled — no app-store app uses it; contact contact@freeshard.net if
> you need it.

Lets app instances on peered shards communicate end-to-end encrypted. Both shards
must add each other as peers (by six-digit ID). The shard handles peer list,
request signing, and signature verification; the app implements the business logic.

- **List peers**: `GET http://shard_core/protected/peers`.
- **Call a peer**: don't call the peer directly — route through core so it adds
  auth. To `GET foo/bar` on peer `b8rk3f`, send to
  `http://shard_core/internal/call_peer/b8rk3f/foo/bar` (target app URL is
  `https://my-app.b8rk3f.<domain>/foo/bar`).
- Implement a **symmetric endpoint** for every call you make (POST to `foo/bar`
  ⇒ also listen for POST at `foo/bar`).
- Use `paths` AC (`peer` access + identity headers) to authorize incoming peer
  requests.

## Events (status: upcoming)

> Not yet implemented; may change.

A built-in shard event broker. Apps will subscribe to any topic and publish under
an app-specific namespace for system-wide events.

## Installing a custom app (without the app store)

For private apps or testing before submission. Zip the metadata files
(`app_meta.json`, `docker-compose.yml.template`, optional icon) — the zip name
must exactly match the app `name`. On the shard: Apps page → *Tools for app
developers* → *Install Custom App* → upload. The zip is small (no images) and can
be shared with others to install the same way.

## Submitting to the app store

Backend repo: `https://github.com/FreeshardBase/app-repository`. One folder per
app containing `app_meta.json`, `docker-compose.yml.template`, and the icon. To
submit, open a PR adding your folder (don't touch other apps); name the branch
`app/<your-app>`. Updates = another PR updating your files.

`store_info` fields (in `app_meta.json`):

```json
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
```

- `description_short` — required; 1–2 sentences, fits the list card.
- `description_long` — optional; string or list of strings (list = paragraphs).
- `hint` — optional; string or list of strings (list = bullet points).
- `is_featured` — leave unset; Freeshard sets this.

## Integrating existing self-hosted apps

Four integration levels:

1. **Blocked** — can't run (no Docker image, needs external services / specific hardware).
2. **Usable with caveats** — runs but rough UX (login screens, non-public resources).
   Requires: whole app (backend + web UI) in Docker images; depends only on
   services Freeshard offers; no manual post-start setup (migrations, user
   creation); modest CPU/memory.
3. **Generally adapted** — configurable for smooth single-user UX (disable user
   management or use proxy auth); HTTP paths cleanly separate public vs protected
   for path-based AC.
4. **Specifically adapted** — uses Freeshard peering for multi-user features;
   tailored to the shard.

Integration checklist: meet ≥ level 2 → write/adapt `docker-compose.yml.template`
(watch volumes + env vars) → write `app_meta.json` (copy the full example, use the
schema) → test on your own shard (free trial: `https://trial.getportal.org/`,
install as a custom app) → smooth UX adaptations:

- **Proxy authentication**: most self-hosted apps have login flows that are
  unnecessary on a single-user shard. Disable user management or switch to proxy
  auth; have the shard inject identity headers (see Routing/AC) so the app trusts
  the proxied user.
- **Access control**: if only the owner uses it, do nothing (default `private`).
  For public (e.g. blog) or peer (e.g. chat API) endpoints, use path-based or
  app-specific AC.

## Revenue share

Developers earn monthly, scaling with how many instances run the app and for how
long; owners pay no per-app cost. Each month: part of the owner's subscription is
a fixed app flatrate → the shard monitors install time per app → computes a weight
proportional to installed time → owner may boost favorites (manual adjustment is
*upcoming*) → the flat fee is split by weight → per-app shares summed across shards
and paid out. Incentives: build broadly useful apps and keep maintaining them
(paid while installed).
