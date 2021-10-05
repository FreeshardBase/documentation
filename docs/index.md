# Welcome

Portal is a B2C cloud computer. User can run apps on their Portal just as they do on their smartphones.
However, they are able to use these apps from any of their physical devices once they are paired to their Portal.
It is similar to self-hosting but as-a-service and super convenient and user-centric.

You can write your own Portal app and have users install and run it.
Since Portal is based on well-established concepts and technology, this is very easy and straightforward.

A Portal app is published as a Docker image containing a webserver that listens for http and serves the static and dynamic content that makes up your app.
The http endpoint is routed and authenticated by Portal, so there is no need to concern yourself with that.
In its simplest form, your app will be available as a subdomain at `<app-name>.<portal-URI>` and only be accessible from the user's paired devices.

## Your Advantages

You do not have to take care of

* hosting
* account management
* authentication
* access control
* security/certificates