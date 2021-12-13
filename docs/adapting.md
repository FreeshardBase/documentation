# Adapting an existing App

A Portal App is essentially a Docker container with a web interface.
This technical simplicity makes it easy to adapt many existing apps to run on Portal.

---

## Hosting an existing App on Portal

It is a common practice to publish apps for self-hosting as Docker images.
That makes deployment and setup easy and standardized.

If an app has no other dependencies (like a database or cache), it can very easily be hosted on Portal.
You just need to write a minimal `app.json` containing a name, the Docker image reference and the port of the web interface or API ([details here](app_json.md)).
If it needs to persist data, mount a directory by adding a `data_dirs` entry.
After writing the `app.json`, paste it into the *Custom App* field as described [here](testing.md).

The app will now run on your Portal and you can access its web interface from any paired device.
If you want to make parts or all of the app publicly accessible, [read about access control](routing_and_ac.md).

## Basic Adaptations

Usually, apps for self-hosting work on Portal and benefit from hosting and access control.
However, some assumptions of self-hosting are different in the Portal ecosystem
which often leads to awkward user experience.
Luckily, those can be often dealt with rather easily.

### User Management

Most existing self-hosting apps feature some kind of user management.
This could be the usual username/password method with functions for registration and signup.
Or it could be using single sign-on.
Whatever the method, for Portal it is usually not needed.

A Portal app has only a single owner who is also the main user.
Having an app ask the user to register is therefore an awkward experience and should be avoided.
It is also unnecessary because there is no need to authenticate incoming requests
since the Portal already does that.

Some apps provide configuration options to disable user management 
or switch to proxy authentication.
This mode is made for situations in which the app is running behind a reverse proxy
which performs authentication and adds a http header containing the logged-in user.
Use these options if available to quickly adapt the app to the Portal ecosystem.
If you are a maintainer, adding an option of this kind should often be a pretty small task.

If you are using proxy authentication, you can use the `X-Ptl-Client-Type` header to source the username.
It always contains one of `terminal`, `peer` or `public` depending on the request's origin.

### Access Control

If your app is only used by the main user - the Portal's owner - 
you do not have to concern yourself with access control.
By default, Portal only allows paired terminals to reach an app.

If, however, your app contains views or API endpoints 
that are meant to be accessed publicly (e.g. blog posts) or by the owner's peers (e.g. a chat API)
you need to implement a kind of access control.
There are generally two approaches.

#### URL-path based AC

Portal allows you to define access based on URL-paths.
Details are described in the [section about routing and access control](routing_and_ac.md).
If your app's path schema naturally distinguishes public and private parts by their path prefixes,
then this may be a suitable approach.
You just have to define the default access and the paths that should be private/public.

However, not all apps consequently reflect access control through paths.

#### App-specific AC

!!! warning "Upcoming Feature"
    The requirements for app-specific AC are not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description. 

With URL-path based AC, your app delegates access control to the Portal on which it runs.
But if your AC needs are more complex, you might want to implement the required logic yourself.

By choosing app-specific AC, you instruct the Portal to let all incoming requests reach your app
but still populate the http headers `X-Ptl-Client-Type` and `X-Ptl-Client-Id`.
This allows you to know for each request from which kind of client it originated
(`terminal`, `peer` or `public`) and if applicable from which specific terminal or peer.
Based on that information, you can make arbitrarily complex access control decisions.

## Advanced Adaptations

Some adaptations to the Portal ecosystem require deeper modification of an app's codebase.
They are often not absolutely required for a good user experience, 
but they really make the difference of a full-fledged Portal app.

### Peer-2-Peer Communication

!!! warning "Upcoming Feature"
    Peering is not yet implemented.
    You cannot use it yet and its implementation - when completed - might differ from this description.

Portal apps usually do not require a dedicated backend server.
Each app runs only on its owner's Portal and app instances talk to each other in a peer-2-peer fashion.

The build-in services that run on every Portal allow you to manage P2P communication.
See the [section about peering](peering.md) for details.
