# Self-Hosting

Freeshard's software, Shard Core, can run on a machine of your own instead of a hosted shard.
Its source code is public under the [Functional Source License (FSL-1.1-ALv2)](https://github.com/FreeshardBase/freeshard/blob/main/LICENSE.md), which permits self-hosting.

The step-by-step instructions live in the repository README, for both a [local test and a full server deployment](https://github.com/FreeshardBase/freeshard#hosting).
This page covers what you need before you start and what does not work yet, so you can decide before you spend time on it.

!!! warning "Early stage"
    A self-hosted shard runs, but the setup is not polished yet.
    Every known gap is listed below with the issue that tracks it.

## Prerequisites

* **A Linux machine with an x86-64 (amd64) CPU.** The Shard Core image is only built for amd64, so ARM boards such as a Raspberry Pi will not work.
* **Docker Engine with the Compose v2 plugin.** The command is `docker compose`; the README still says `docker-compose`, which is the retired v1 tool ([#134](https://github.com/FreeshardBase/freeshard/issues/134)).
* **A host to itself.** Ports 80, 443 and 8883 must be free, and there must be no Docker network called `portal`. Both are fixed in the compose file ([#196](https://github.com/FreeshardBase/freeshard/issues/196)). A dedicated machine or VM is the easiest setup.
* **Root or `sudo`.** The containers write the shard's data as root.
* **Memory and disk.** There is no tested minimum yet. For comparison, the smallest hosted shard has 1 vCPU and 2 GB of RAM. Apps are downloaded when they are first opened, and some are large: the Immich images alone are about 3.5 GB.
* **For a server on the internet: a domain with wildcard DNS.** Every app gets its own subdomain, so `*.<your domain>` must point at the server, and the certificate has to be a wildcard certificate obtained through a DNS challenge. See [Certificates](#certificates) below before you rent a server for this.
* **For a local test: `*.localhost` resolution.** The shard is reached at `http://<shard id>.localhost`. systemd-resolved resolves such names; plain glibc without it and Windows do not.

All files (`docker-compose.yml`, `.env`) go into one directory, and the commands are run from there.
Both files are in the root of the [repository](https://github.com/FreeshardBase/freeshard); the env file is shipped as `.env.template`.
Set `FREESHARD_DIR` to an absolute path of your choice; the template's `/home/user/.freeshard` is only an example.

## What a self-hosted shard still gets from Freeshard

A self-hosted shard is not self-contained.
The app catalogue, the app packages and some app container images are served by infrastructure Freeshard operates.
The README explains [where the apps come from](https://github.com/FreeshardBase/freeshard#where-the-apps-come-from) and what you would have to replace to avoid that dependency ([#195](https://github.com/FreeshardBase/freeshard/issues/195)).

The shard also still contacts Freeshard's management service, for example at startup and for the nightly backup. Those requests fail for a self-hosted shard, which has no account there ([#286](https://github.com/FreeshardBase/freeshard/issues/286)).

## Known gaps

### Certificates

Today the shipped setup can only obtain a Let's Encrypt certificate through Azure DNS.
With any other DNS provider, Traefik serves its own self-signed certificate ([#292](https://github.com/FreeshardBase/freeshard/issues/292)).
A local test with `DISABLE_SSL=true` is not affected.

### Email

A self-hosted shard cannot send mail, so mail confirmation has to be switched off, or setting the owner's email address fails with HTTP 502.
The README says to do this in `local_config.toml`, but the container never reads that file ([#300](https://github.com/FreeshardBase/freeshard/issues/300)).
Until that is fixed, add this line to the `environment` list of the `shard_core` service in `docker-compose.yml`:

```yaml
      - FREESHARD_EMAIL__ENABLED=false
```

### Backups

The nightly backup depends on Freeshard's management service and fails on a self-hosted shard, although the interface says a backup runs every night ([#286](https://github.com/FreeshardBase/freeshard/issues/286)).
Back up `FREESHARD_DIR` yourself.
The README section [Backup and Restore](https://github.com/FreeshardBase/freeshard#backup-and-restore) describes what it contains.

### Isolation

Shard Core and Traefik have access to the Docker socket, which amounts to root access on the host.
Run a shard on a machine or VM that does nothing else you care about ([#198](https://github.com/FreeshardBase/freeshard/issues/198)).

## Uninstalling

`docker compose down` stops and removes the containers.
It does not remove any data, not even with `-v`: everything lives in `FREESHARD_DIR`, including the shard's private key, the database and all user data.
To remove the shard completely, delete that directory, which needs `sudo` because the files belong to root.

## Questions

If something on this page is wrong or out of date, or you get stuck, open an issue on [GitHub](https://github.com/FreeshardBase/freeshard/issues) or write to [contact@freeshard.net](mailto:contact@freeshard.net).
