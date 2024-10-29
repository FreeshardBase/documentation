# Portal

Most technologies have first been a tool for professionals before they became a tool for consumers.
Cloud computers have not yet made this transition:
they are used by professionals all the time, but only indirectly by consumers.
However, a _personal cloud computer_ would have a lot to offer if it can be made simple enough.

With current technology, this can be achieved easily.
Portal is this cloud computer for consumers.

---

The benefits of a personal cloud computer are:

* A **single place** for all your data and applications.
* Accessing data and applications from **any device**.
* An **always-on** and **always-online** personal server.
* The **privacy and security** of dedicated and owned infrastructure.

Current modes of using computers and the internet can be categorized into three general types:

Local applications run on a single device, store their data on that device, and are bound by its capabilities.
They cannot be used for hosting anything with any reliability.
And if you want to use them on another device, you are out of luck.

SaaS applications run on a remote server and are accessed through a web browser or a dedicated app.
That makes them reliably available on any device.
However, their data is stored on the server, which means you have to trust the provider.
And the data is in a silo, which means you cannot open it with other applications, and it is generally hard to move it.

Finally, there are self-hosted applications.
They solve the problems mentioned above, but they are hard to set up and maintain.
You need considerable technical knowledge to set them up and maintain them.


|                  | Portal | SaaS | self-host | local |
|------------------|--------|------|-----------|-------|
| Privacy          | ✅      | ❌    | ✅         | ✅     |
| Simplicity       | ✅      | ✅    | ❌         | ✅     |
| Cross-Device     | ✅      | ✅    | ✅         | ❌     |
| Always available | ✅      | ✅    | ✅         | ❌     |

## How it works

![Portal Architecture](img/arch.png)

## Developing for Portal

When developing a Portal-app you need to think a little differently about it compared to web-apps, desktop applications
or mobile apps.
A Portal-app has a unique combination of features and paradigms.

As it runs on a Portal which is a virtual machine on cloud infrastructure,
it has the benefits of the cloud:

* your app can be always on and always online, which is great for serving content like a blog or continually monitoring
  something like sensor readings,
* your app is present on all the user's devices, so you can create a cross-device experience, making it equally mobile
  for a smartphone and complex for a desktop computer or even combine and sync multiple devices in new and unique
  workflows,
* your app keeps its single source of truth on the Portal.

However, since a Portal is a single user's private space, a Portal-app also has aspects of a local application:

* each running instance serves a single user, there is no user management,
* there is a local file-system on the Portal that belongs to the user and your app can use it to persist data,
* the infrastructure that runs your app is already there, you don't need to think about hosting.

## What Portal does for you

The Portal core software stack that manages the whole Portal including your app
already does a lot of things for you.
Things that usually you would have to do yourself.
For example:

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
and to make your life as a Portal-app developer simpler:
you have to learn only very few new concepts to get started.

A Portal app is published as a Docker image containing a web server that listens for HTTP and serves the static and
dynamic content that makes up your app's GUI.
The HTTP endpoint is routed and authenticated by Portal, so there is no need to concern yourself with that.
When a user installs your app, it will be available at a subdomain of the user's Portal: `<app-name>.<portal-URI>`.
It will only be accessible from the user's paired devices.

Giving your app more capabilities is easy. You
can [request a part of Portal's file-system](../developer_docs/persisting.md)
or [add views that are public or only accessible to peers](../developer_docs/routing_and_ac.md)
or [listen and react to Portal-wide events](../developer_docs/events.md).
