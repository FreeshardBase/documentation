# Integration of Existing Apps

Many apps that are made for self-hosting are also useful to run on Portal.
However, the degree to which an app can be configured for a smooth user experience on Portal varies.

---

We discern four levels of adaptation to Portal that an app can achieve:
0) blocked, 1) usable with caveats, 2) general adaptations, 3) specific adaptations.

Apps that are made for self-hosting mostly are in category zero or one, some are in category two, none is currently in category three.
Our aim is to motivate app developers to work towards bringing their apps into category three
because it yields the best and smoothest experience for the user.

## Level 0: Blocked

Some apps cannot be run on Portal at all.
They might consist of multiple Docker images that work together or rely on external services that Portal does not offer.
As Portal is developed further, some of these apps might move into level 1 on their own.

## Level 1: Usable with Caveats

These are apps that can run on Portal, but they do not offer a smooth user experience.
When using the app, it is clear that it was not made for Portal.
Typical issues that break the user experience are an account creation and login screen - which should almost never be needed on Portal -
or that resources that should be publicly accessible are not.

### App Requirements for Level 1

* The app is contained inside a single docker image and only depends on external services that Portal offers (see [Portal's Internal Services](internal_services.md)).
* No manual setup is needed after the app starts for the first time. E.g. database migration, user creation.
* System requirements in terms of processing and memory are relatively low.

## Level 2: General Adaptations

Apps that can be configured in a way that allows a mostly smooth user experience on Portal fall in this category.
The configuration options are not made specifically for integration with Portal,
instead they are useful for multiple common hosting scenarios.

### App Requirements for Level 2

* The app can be configured for proxy auth, such that it reads the logged-in username from a http header.
* HTTP resource paths cleanly separate public and protected resources such that [Portal path-base AC](routing_and_ac.md#access-control) can be used.

## Level 3: Specific Adaptations

A Portal is a unique environment for an app to run in.
To fully use what the Portal has to offer, adaptations of the app must therefore also be unique tailored to the Portal.
These adaptations are usually not useful in other hosting scenarios,
but they enable an extraordinarily smooth user experience on Portal.

### App Requirements for Level 3

* [Portal's peering feature](peering.md) is used for multi-user apps.
