# Portal's Internal Services

The core software stack that manages a Portal offers several services to installed apps.
Use them by making REST requests against their APIs.

---

!!! danger "Unsafe API"
    Right now, the APIs described here are accessible without any checks.
    Your app can view, modify, and delete critical information about the Portal
    and even completely break it.
    This will of course be locked down in the future but for now: be careful what you do!

## Identities

Your app may query and modify identities stored on the Portal:
the Portal's own identities, those of paired terminals, and those of known peers.
The service that handles them is called `identity_handler`.
You can reach its API at `http://ih/` and there is a full [OpenAPI Specification](https://ptl.gitlab.io/identity_handler/).

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