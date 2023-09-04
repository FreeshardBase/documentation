# Portal's Internal Services

The core software stack that manages a Portal offers several services to installed apps.
Use them by making REST requests against their APIs.

---

!!! danger "Unsafe API"
    Right now, the APIs described here are accessible without any checks.
    Your app can view, modify, and delete critical information about the Portal
    and even completely break it.
    This will of course be locked down in the future, but for now: be careful what you do!

## Portal Core

The Portal core software stack is what manages all of a Portal's operations
like its identities, terminals, peers or apps.
It provides a REST API that your app may use.
Its base URL is `http://portal_core`. For example, you can list all apps by calling
`GET http://portal_core/protected/apps`.

Find the full API documentation [here](https://ptl.gitlab.io/portal_core/){target=_blank}.

## Other Apps

Your app can contact other apps that are installed on the same Portal
if they offer an API for this.

!!! warning "Upcoming Feature"
    Inter-App APIs are not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description.
