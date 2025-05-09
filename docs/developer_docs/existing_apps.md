---
title: Integration of Existing Apps
---

Many apps that are made for self-hosting are also useful to run on a shard.
And thanks to freeshard's technical simplicity, this is often easy to do.
However, the degree to which an app can be configured for a smooth user experience on freeshard varies.

---

## Levels of Integration

We roughly discern four levels of adaptation to freeshard that an app can achieve:

1. blocked, 
1. usable with caveats, 
1. generally adapted, 
1. specifically adapted.

Apps that are made for self-hosting mostly are in category one or two, some are in category three, none is currently in category four.
Our aim is to motivate app developers to work towards bringing their apps into category four
because it yields the best and smoothest experience for the user.

### Level 1: Blocked

Some apps cannot be run on freeshard at all.
They might not offer a Docker image at all or rely on external services or specific hardware that freeshard does not offer.
As freeshard is developed further, some of these apps might move into level 2 on their own
but most will require some effort by the developer to bring them to level 2.

### Level 2: Usable with Caveats

These are apps that can run on freeshard, but do not offer a smooth user experience.
When using the app, it is clear that it was not made for freeshard.
Typical issues that break the user experience are an account creation and login screen - which should almost never be needed on freeshard -
or resources that should be publicly accessible but are not.

#### App Requirements for Level 2

* The whole app (backend and web-UI) is contained in a collection of docker images.
* The app only depends on services that freeshard offers (see [Freeshard's Internal Services](internal_services.md)).
* No manual setup is needed after the app starts for the first time. E.g. database migration, user creation.
* System requirements in terms of processing and memory are relatively modest.

### Level 3: Generally Adapted

Apps that can be configured in a way that allows a mostly smooth user experience on freeshard fall in this category.
The configuration options are not made specifically for integration with freeshard,
instead they are useful for multiple common hosting scenarios.

#### App Requirements for Level 3

* The app can be configured to allow for a smooth single-user experience. E.g. no account creation or login screen.
    This is usually done by disabling user management or switching to proxy authentication.
* HTTP resource paths cleanly separate public and protected resources such that [path-based AC](routing_and_ac.md#access-control) can be used.

### Level 4: Specifically Adapted

A shard is a unique environment for an app to run in.
To fully use what the shard has to offer, adaptations of the app must therefore also be uniquely tailored to the shard.
These adaptations are usually not useful in other hosting scenarios,
but they enable an extraordinarily smooth user experience on freeshard.

#### App Requirements for Level 4

* [Freeshard's peering feature](peering.md) is used for multi-user apps.

## Tasks for integration of an existing App

If all goes well, bringing an existing app into the freeshard app store can be quick and easy.
Sometimes a little more work has to be done, depending on the requirements that the app already meets.
Here is a checklist to work through.

### Make sure, the app meets at least level 2 requirements

Many self-hosting apps already meet the requirements for level 2 integration [listed above](#app-requirements-for-level-2) but some do not.
If your app does not meet the requirements, it is for you to decide if the needed modifications are quick and easy or too much effort.

For example your app might rely on a manual user-creation step after first start.
Performing this step automatically configured by environment variables might be an easy modification.
On the other hand, if your app needs specific hardware and cannot work without it,
you are out of luck - it might just not be a good match for freeshard.

### Write or adapt a `docker-compose.yml.template` file

The `docker-compose.yml.template` file tells the shard how to run the containers of your app.
See here for [details about Docker Compose](https://docs.docker.com/compose/compose-file/){target=blank}.

Often, you can take an existing `docker-compose.yml` file as a starting point and
modify some configuration values as needed.
In particular, you want to take a look at volume mounts and environment variables.
See [here](docker_compose_template.md) for more details.

### Write an `app_meta.json` file

The `app_meta.json` file tells the shard how to treat the containers started by the `docker-compose.yml.template` file.
You will have to write one for your app.
The easiest way is to copy the example from [here](app_meta_json.md#full-example) and modify it.
To aid you in this task, we provide a [schema](app_meta_json.md#schema) for the file.

### Test your app on your shard

You need your own shard for this step.
If you do not have one, you can get a free trial [here](https://trial.getportal.org/){target=blank}.
Then, you can package your app as a freeshard app and install it as described [here](custom_apps.md).

### Make further adaptations

Many apps can easily be configured such that the user experience is smoother.
For example, you can provide environment variables
or add http headers to calls to certain paths.
These are the most common configurations that help smooth out the user experience.

#### Proxy Authentication

Most existing self-hosting apps feature some kind of user management and corresponding login flow.
This could be the usual username/password method with functions for registration and signup.
Or it could be using single sign-on.
Whatever the method, for freeshard it either must be modified slightly or is not needed at all.

In contrast to a self-hosting environment, each shard is owned and primarily used by only a single person.
Therefore, having an app ask the user to register makes not much sense.
It is also unnecessary because there is no need to authenticate incoming requests.
The shard already does that for you.

Some apps provide configuration options to disable user management 
or switch to proxy authentication.
This mode is made for situations in which the app is deployed behind a reverse proxy
which performs authentication and adds a http header containing the name of the logged-in user.
Use these options if available to avoid a puzzling registration form.
If you are a maintainer, adding an option of this kind should often be a pretty small task.

If you are using proxy authentication, you can configure your app such that the shard adds
the necessary headers to all requests. See the [section about access control](routing_and_ac.md#access-control) for details.

#### Access Control

If your app is only used by the main user - the shard's owner - 
you do not have to concern yourself with access control at all.
By default, the shard only allows paired devices to reach an app.

If, however, your app contains views or API endpoints 
that are meant to be accessed publicly (e.g. blog posts) or by the owner's peers (e.g. a chat API)
you need to implement a kind of access control.

There are generally two approaches: path-based AC and app-specific AC.
Depending on the existing structure of your app and your willingness to make adaptations,
one or the other might be suitable.
Read more about them in the [section about routing and access control](routing_and_ac.md).


