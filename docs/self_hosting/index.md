# Self-Hosting

Freeshard's software, Shard Core, can run on a machine of your own instead of a hosted shard.
Its source code is public under the [Functional Source License (FSL-1.1-ALv2)](https://github.com/FreeshardBase/freeshard/blob/main/LICENSE.md), which permits self-hosting.

This page is the complete guide: what you need, how to try it locally, how to run it on a server, and what does not work yet.

!!! warning "Early stage"
    A self-hosted shard runs, but the setup is not polished yet.
    Every known gap is listed under [Known gaps](#known-gaps), with the issue that tracks it.

## Prerequisites

* **A Linux machine with an x86-64 (amd64) CPU.** The Shard Core image is only built for amd64, so ARM boards such as a Raspberry Pi will not work.
* **Docker Engine with the Compose v2 plugin.** All commands below use `docker compose`. The retired v1 tool `docker-compose` is not supported.
* **A host to itself.** Ports 80, 443 and 8883 must be free, and there must be no Docker network called `portal`. Both are fixed in the compose file ([#196](https://github.com/FreeshardBase/freeshard/issues/196)). Shard Core also removes unused Docker images on the host once a day (see `PRUNE_IMAGES` under [Configuration](#configuration)). A dedicated machine or VM is the easiest setup.
* **Root or `sudo`.** The containers write the shard's data as root.
* **Memory and disk.** There is no tested minimum yet. For comparison, the smallest hosted shard has 1 vCPU and 2 GB of RAM. Apps are downloaded when they are first opened, and some are large: the Immich images alone are about 3.5 GB.
* **For a local test: `*.localhost` resolution.** The shard is reached at `http://<shard id>.localhost`. systemd-resolved resolves such names; plain glibc without it and Windows do not.
* **For a server on the internet: a domain with wildcard DNS**, and for now a DNS zone hosted in Azure DNS. See [Certificates](#certificates) before you rent a server for this.

## Get the files

A shard needs two files from the [repository](https://github.com/FreeshardBase/freeshard), in one directory of your choice.
Run every command on this page from that directory.

```shell
mkdir freeshard && cd freeshard
curl -fsSL -o docker-compose.yml https://raw.githubusercontent.com/FreeshardBase/freeshard/main/docker-compose.yml
curl -fsSL -o .env https://raw.githubusercontent.com/FreeshardBase/freeshard/main/.env.template
```

The compose file pins the same versions of Shard Core, Traefik, Postgres and the two web interfaces that hosted shards run.

## Try it locally

1. Edit `.env`:
    * `FREESHARD_DIR`: an absolute path where all shard data will be stored. It is created on first start and owned by root.
    * `DNS_ZONE`: leave it at `localhost`.
    * `EMAIL`: can stay as it is, no certificates are requested.
    * `DISABLE_SSL`: set it to `true`.
2. Start the shard:
    ```shell
    docker compose up -d
    ```
3. Read the welcome message:
    ```shell
    docker compose logs shard_core
    ```
    It shows the Freeshard logo, the shard's address `http://<shard id>.localhost` and, as long as no device is paired, a pairing link that is valid for 10 minutes.
4. Open the pairing link in your browser. If the code is not filled in, type it into the pairing field.

To pair another device later, get a fresh code from inside the shard's network:

```shell
docker run --rm --network portal curlimages/curl -s "http://shard_core/protected/terminals/pairing-code"
```

Then open `http://<shard id>.localhost/#/pair` on the new device and enter the code.

## Run it on a server

1. Use a server that is reachable from the internet, with a domain whose DNS you control.
2. Point the domain and every subdomain at the server. Each app gets its own subdomain under the shard's domain, so you need a wildcard record, for example `*.example.org`. The shard's own address is `<shard id>.example.org`, which the wildcard covers.
3. [Get the files](#get-the-files) onto the server and edit `.env`:
    * `FREESHARD_DIR`: an absolute path for all shard data.
    * `DNS_ZONE`: your domain, for example `example.org`.
    * `EMAIL`: your address, which Let's Encrypt uses for certificate notices.
    * `DISABLE_SSL`: `false`. Never set it to `true` on a server reachable from the internet.
4. Set up certificates as described under [Certificates](#certificates).
5. Start the shard with `docker compose up -d`, then read the welcome message and pair your first device as in the local test. The address now starts with `https://`.

### Certificates

Every app lives on its own subdomain, so the shard needs a wildcard certificate, and Let's Encrypt issues those only through a DNS challenge.
Traefik answers that challenge by creating a DNS record through your DNS provider's API.

Today Shard Core configures Traefik for Azure DNS only, and the provider cannot be changed without rebuilding the image ([#292](https://github.com/FreeshardBase/freeshard/issues/292)).
If your zone is in Azure DNS, uncomment the `AZURE_*` variables and `LEGO_AZURE_BYPASS_DEPRECATION` of the `traefik` service in `docker-compose.yml` and fill them in with a service principal that may edit the zone ([Traefik's provider list](https://doc.traefik.io/traefik/v2.11/https/acme/#providers) names the variables).
With any other DNS provider, Traefik falls back to its own self-signed certificate, which browsers reject.

## Configuration

All settings live in `.env`. The first three are required; the rest are optional and fall back to the defaults shown.

| Variable | Default | Meaning |
|---|---|---|
| `FREESHARD_DIR` | | Absolute path for all shard data |
| `DNS_ZONE` | | Domain the shard lives under; `localhost` for a local test |
| `EMAIL` | | Contact address for Let's Encrypt |
| `DISABLE_SSL` | `false` | `true` only for a local test without certificates |
| `EMAIL_ENABLED` | `false` | Keep `false`, see [The owner's email address](#the-owners-email-address) |
| `PRUNE_IMAGES` | `true` | Once a day at 04:00, removes Docker images that no container uses and that are older than 24 hours. This applies to every image on the host, not only the shard's. Set it to `false` if the host runs other containers |
| `SUNDIAL_ENABLED` | `false` | `true` serves Sundial, the new web interface, at the shard's root instead of the current one |
| `OIDC_ENABLED` | `false` | `true` turns on the shard's built-in login provider for apps |
| `PAUSE_ENABLED` | `false` | `true` pauses idle apps first and stops them only later or when memory gets tight, so they come back faster |

After changing `.env`, run `docker compose up -d` again.

### The owner's email address

On a hosted shard, a new owner address only counts once its owner has opened a confirmation link mailed to it.
A self-hosted shard cannot send mail, so with `EMAIL_ENABLED=false` the address is taken as given, without a confirmation mail.
That is acceptable because you control the machine.
With `true`, setting an address fails with HTTP 502 and the address stays unconfirmed.

The confirmed address is what the built-in login provider passes to apps.
Without one, apps you log into through it create fresh accounts instead of linking to an existing one by address.

## What a self-hosted shard still gets from Freeshard

A self-hosted shard is not self-contained ([#195](https://github.com/FreeshardBase/freeshard/issues/195)). Both halves of the app catalogue come from infrastructure Freeshard operates:

* the catalogue and the app packages come from an Azure storage container (`apps.app_store` in [`config.toml`](https://github.com/FreeshardBase/freeshard/blob/main/config.toml)), and
* the container images of apps that do not use a public upstream image come from Freeshard's registry, `portalapps.azurecr.io`.

Shard Core logs in to that registry with credentials that are committed to `config.toml` on purpose.
They belong to a service principal whose only permission anywhere is reading that one registry: it can pull images and read registry metadata, nothing else.
Every shard needs it to install apps.
If you would rather not depend on Freeshard's infrastructure, these two are what you would have to replace.

The shard also still contacts Freeshard's management service, for example at startup and for the nightly backup.
Those requests fail for a self-hosted shard, which has no account there ([#286](https://github.com/FreeshardBase/freeshard/issues/286)).

## Known gaps

* **Certificates only through Azure DNS** ([#292](https://github.com/FreeshardBase/freeshard/issues/292)), see [Certificates](#certificates).
* **No automatic backup.** The nightly backup depends on Freeshard's management service and fails on a self-hosted shard, although the interface says a backup runs every night ([#286](https://github.com/FreeshardBase/freeshard/issues/286)). See [Backups](#backups).
* **The shard assumes it owns the host:** fixed ports, a fixed network name, and Traefik also picks up other containers on the host ([#196](https://github.com/FreeshardBase/freeshard/issues/196)).
* **Isolation.** Shard Core and Traefik have access to the Docker socket, which amounts to root access on the host. Run a shard on a machine or VM that does nothing else you care about ([#198](https://github.com/FreeshardBase/freeshard/issues/198)).

## Backups

Everything a shard has is in `FREESHARD_DIR`: its identity and private key, the database, the installed apps and all user data.
Back up that directory, ideally with the shard stopped (`docker compose stop`) so the database is consistent.
The repository README describes [how hosted shards back up and restore](https://github.com/FreeshardBase/freeshard#backup-and-restore).

## Updating

Download the current `docker-compose.yml` again (see [Get the files](#get-the-files)), keep your `.env`, and run:

```shell
docker compose up -d
```

Docker pulls the new images and recreates the containers. Database migrations run when Shard Core starts.
If you changed `docker-compose.yml` yourself, for example for certificates, carry those changes over.

## Uninstalling

`docker compose down` stops and removes the containers.
It does not remove any data, not even with `-v`: everything lives in `FREESHARD_DIR`, including the shard's private key.
To remove the shard completely, delete that directory, which needs `sudo` because the files belong to root:

```shell
docker compose down
sudo rm -rf <FREESHARD_DIR>
```

## Questions

If something on this page is wrong or out of date, or you get stuck, open an issue on [GitHub](https://github.com/FreeshardBase/freeshard/issues) or write to [contact@freeshard.net](mailto:contact@freeshard.net).
