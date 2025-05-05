---
title: Peering
status: disabled
---

A shard's owner can enter other shards' IDs in order to peer with them.
This allows apps to establish end-to-end encrypted and authenticated communication
between itself and another instance of the same app that is running on a peer.

---

!!! warning "Feature is disabled"
    At the moment, there is no app in the app store that uses this feature.
    For this reason and in order not to confuse users, the feature is deactivated currently.
    If you plan to make use of it, please [contact us](mailto:contact@freeshard.net).

## Overview

### Rationale

Each shard is a single-user platform and so each app that runs there is owned by a single user.
This is in contrast to typical SaaS platforms which often include user management
and serve many users at once.
But of course many applications benefit from or completely rely on multiple users accessing them,
e.g. chat/messaging, collaboration, social, sharing, etc.

In order to allow such use-cases on freeshard while maintaining privacy and sovereignty,
apps must be able to exchange data in a peer-to-peer manner.

### Shards' role

Shards allow apps to send http requests to another instance of the same app that runs on a peer.
It takes care of:

* Managing the list of known peers and their basic information (ID, name).
* Sending signed http requests to peers on behalf of apps.
* Verifying signatures of incoming http requests before forwarding them to apps.

As an app developer, your responsibility is:

* Querying the shard core for known peers and enriching them with app-specific metadata if needed (ACLs, privileges, etc.).
* Implementing the business logic for sending and receiving requests to and from peers.
* Adding the necessary entries in the `app_meta.json` to configure access control and get needed information on each incoming request. (See [Routing and AC](routing_and_ac.md))

In particular, it is important for each app to implement a symmetric endpoint for each call it makes.
If it calls a peer with a POST to `foo/bar`, it must listen to POST requests from other instances at `foo/bar`.

## Shard IDs

Each shard has a unique and random ID.
You can think of it like the shard's phone number (although it is alphanumeric).
You can see the first six digits of your shard's ID on the home screen and as part of its URL.
The real ID is much longer, but you rarely need it.

![Screenshot of a shard's ID](img/screenshot_portal_id.png)

Every shard also maintains a contact list containing the IDs of other shards,
which we call peers.
You can modify this list, e.g. add your friends' shards.

![Screenshot of a shard's peers view](img/peers_view.png)

When a shard communicates with another shard, both shards must have added each other as a peer.
Then, the nature of the IDs makes sure that all communication is authenticated and end-to-end encrypted.

## Access Control

When writing your `app_meta.json` file, you can limit access to certain URL-paths to peers only.
And you can let the shard add http headers to any incoming request that identify requests coming from peers
and include the peer's id and name.
You can also combine these features.
This allows you to open parts of your app for peer-to-peer communication.
For more details see the section about [Routing and AC](routing_and_ac.md).

## Listing Peers

In order to send data to a peer, your app must first request the list of peers that the host-shard knows about.
This is achieved by sending an internal request to the shard core at `http://shard_core/protected/peers`.
See the [API docs](https://ptl.gitlab.io/portal_core/#tag/protected/operation/list_all_peers_protected_peers_get){target=blank} for details.

## Sending a Request to a Peer

Once the desired peer and its ID is known, your app can send http requests to it.
However, it cannot send the requests directly, because then,
the receiver shard cannot authenticate the sender.
Instead, the request must be sent through shard core which adds the necessary authentication header.

Consider the app `my-app` that would like to send a `GET` request to the path `foo/bar`
on a peer shard with the ID `b8rk3f`.
The complete URL is `https://my-app.b8rk3f.<domain>/foo/bar`.
However, to have the shard add authentication, your app must instead send the request to
`http://shard_core/internal/call_peer/b8rk3f/foo/bar`.

### Sending Sequence

When sending a request to a peer, this is the sequence that it follows.

``` mermaid
sequenceDiagram
  participant Aa as myapp on c0p3x5
  participant Ac as Core on c0p3x5
  participant Bp as Proxy on b8rk3f
  participant Bc as Core on b8rk3f
  participant Ba as myapp on b8rk3f

  Aa->>Ac:shard_core/internal/call_peer/b8rk3f/foo/bar
  Ac->>Bp:my-app.b8rk3f.<domain>/foo/bar
  Bp->>Bc:shard_core/internal/auth
  Bc-->>Bp:OK
  Bp->>Ba:my-app/foo/bar
  Ba-->>Bp:OK
  Bp-->>Ac:OK
  Ac-->>Aa:OK
```

* `Core on c0p3x5` adds a signature to the request
* `Proxy on b8rk3f` accepts the request and decides about routing
* `Core on b8rk3f` verifies the signature and decides about access control according to the configuration in `app_meta.json`
