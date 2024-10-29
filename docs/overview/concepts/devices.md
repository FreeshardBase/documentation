# Devices

## Device Pairing

A Portal is a cloud computer and so it is impossible to directly interact with it like with a smartphone or a notebook.
Instead, a Portal's owner uses existing devices to access their Portal remotely.
This, of course, requires some kind of authentication mechanism to ensure that only the owner can access their Portal.

With Portal, this is done by pairing devices with the Portal, which is a one-time process.
Once paired, the device can access the Portal's web interface and all apps with full permissions.
Without pairing, only the Portal's public view can be accessed (where the owner may or may not publish some information about themselves)
as well as any data that is published by apps.

To pair a new device, another, already paired device is needed.
It can generate a one-time code that the new device can use to pair with the Portal.
The first code is generated during sign-up and used right away to pair the first device.
The design goal is to make the pairing process as simple as possible, while still being secure.

??? technical-details "Credentials and encryption"
    After pairing, the device is given a JWT containing a unique device ID and a secret key.
    This JWT is stored as a cookie in the browser.
    (So to be precise, not the device is paired, but the browser on the device.)

    For encryption, Portal relies on standard HTTPS encryption.
    The Portal is authenticated by a certificate and the browser by its JWT.

## Inversion of Control

Today, devices and cloud services usually have a relationship where the device is the main platform
and any cloud services are secondary to it, e.g. by syncing data across devices or installed applications.
With Portal, the goal is to inverse that relationship:
Portal should become the primary platform, devices should become secondary.
In fact, with a feature-complete Portal, devices should become completely interchangeable.

This is a natural evolution of the way consumers use computers.
It started with single desktop PCs, evolved with Notebooks, then Smartphones.
Now, with the need to switch between different devices in different situations,
applications and data are moving to the cloud as everything becomes a SaaS.
The next logical step is to put the whole platform in the cloud, like Portal.
