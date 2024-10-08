---
hide:
  #- navigation
  - toc
---

# Portal

Most technologies have first been a tool for professionals before they became a tool for consumers.
Cloud computers have not yet made this transition, although _personal cloud computers_ would have a lot to offer. 

But with current technology, the time is right.

Portal is the cloud computer for consumers.

Private like your home.

Simple as your phone.

Always with you on the nearest screen.

---

With Portal, everyone can have their own cloud computer and enjoy the benefits that come with it.

* A **single place** for all your data and applications.
* Accessing data and applications from **any device**.
* An **always-on** and **always-online** personal server.
* The **privacy and security** of dedicated and owned infrastructure.

## How it works

![Portal Architecture](img/arch.png)

## Key Concepts

### Always On, Always Online

### Device Pairing

### Apps

(Start/Stop)

### Portal Pairing

### Web Interface

### How to think about your App

### Subscription and Management

When developing a Portal-app you need to think a little differently about it compared to web-apps, desktop applications or mobile apps.
A Portal-app has a unique combination of features and paradigms.

As it runs on a Portal which is a virtual machine on cloud infrastructure,
it has the benefits of the cloud:

* your app can be always on and always online, which is great for serving content like a blog or continually monitoring something like sensor readings,
* your app is present on all the user's devices, so you can create a cross-device experience, making it equally mobile for a smartphone and complex for a desktop computer or even combine and sync multiple devices in new and unique workflows,
* your app keeps its single source of truth on the Portal.

However, since a Portal is a single user's private space, a Portal-app also has aspects of a local application:

* each running instance serves a single user, there is no user management,
* there is a local file-system on the Portal that belongs to the user and your app can use it to persist data,
* the infrastructure that runs your app is already there, you don't need to think about hosting.

## What the Portal does for you

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

A Portal app is published as a Docker image containing a web server that listens for HTTP and serves the static and dynamic content that makes up your app's GUI.
The HTTP endpoint is routed and authenticated by Portal, so there is no need to concern yourself with that.
When a user installs your app, it will be available at a subdomain of the user's Portal: `<app-name>.<portal-URI>`.
It will only be accessible from the user's paired devices.

Giving your app more capabilities is easy. You can [request a part of Portal's file-system](developer_docs/persisting.md)
or [add views that are public or only accessible to peers](developer_docs/routing_and_ac.md)
or [listen and react to Portal-wide events](developer_docs/events.md).
