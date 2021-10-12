# Welcome

Portal is a private cloud computer that is marketed directly to consumers.
It is meant to replace both locally installed applications and web-services with Portal-apps.

---

A Portal-app runs on a user's personal Portal and is accessed via any device
that the user has paired with their Portal, we call them terminals.

You can write your own Portal app and have users install and run it.
Since Portal is based on well-established concepts and technology, this is very easy and straightforward.

## How to think about your App

Developing a Portal-app is most likely quite different from what you are used to 
whether you have been building web-apps, desktop applications or mobile apps.
A Portal-app has a unique combination of features and paradigms.

As it runs on a Portal which is a virtual machine on cloud infrastructure,
it shares benefits of the cloud:

* your app can be always on and always online which is great for serving content like a blog or continually monitoring something like sensor readings,
* your app is present on all the user's terminals, so you can create an omni-device experience, making it equally mobile for a smartphone and complex for a desktop computer or even combine multiple terminals in new and unique workflows,
* your app keeps its single source of truth on the Portal.

However, since a Portal is a single user's private space, a Portal-app also has aspects of a local application:

* each running instance serves a single user, there is no user management,
* there is a local file-system on the Portal to which your app can request permission,
* the infrastructure that runs your app is already there, no need to think about hosting.

## What the Portal does for you

The Portal core software stack that manages the whole Portal including your app
already does a lot of things for you.
Things that usually you would have to do yourself.
Among other things, these are:

* Encryption and certificates
* User management and authentication
* Contact lists/friend lists
* Hosting
* Backups
* Compensation/Payment

## Technology

A Portal is not rocket science.
We use lots of established technology, not only to make our own lives easier and development quicker
but also to make Portal more reliable and secure
and to make your life as a Portal-app developer easier: 
you have to learn only very few new concepts to get started.

A Portal app is published as a Docker image containing a webserver that listens for http and serves the static and dynamic content that makes up your app.
The http endpoint is routed and authenticated by Portal, so there is no need to concern yourself with that.
In its simplest form, your app will be available as a subdomain at `<app-name>.<portal-URI>` and only be accessible from the user's paired devices.

Giving your app more capabilities is easy, you can [request a part of Portal's file-system](persisting.md)
or [add view that are public or only accessable to peers](routing_and_ac.md)
or [listen and react to Portal-wide events](events.md).
