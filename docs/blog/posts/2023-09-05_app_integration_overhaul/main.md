---
draft: false 
date: 2023-09-05
authors:
  - max
---

# App Integration Overhaul

When developing a piece of software, the best way to make steady and sustainable progress is to work in small and self-contained increments.
Each change should have a clear scope that is easy to reason about, to test, and to roll back if needed.
Side effects should be avoided as much as possible.
With the latest update, I did the opposite of that.

<!-- more -->

# The Inciting Incident

I wanted to include Overleaf in our app store.
Overleaf is a web-based LaTeX editor that is very popular among scientists and students
and would make a great addition.
It is especially useful because writing with LaTeX can be painfully technical and Overleaf just takes care of most of the details for you. 

However, it turns out that Overleaf has a few requirements in the form of other containers that need to be running on the same machine,
namely a Redis server and a MongoDB database.
And that is something that Portal just did not support.
Now, in the past, I sometimes worked around this by building a new image for the app that includes and starts all the required processes.
But that can be tricky and error-prone and goes against the idea of Docker containers doing only one thing at a time.

So it was a good time to tackle a task that has been sitting in the backlog for quite some time:
overhauling the app integration system.

# Taking it all Apart

![Mechanic and disassembled machine](./mechanic.jpg){ width="500" }

Handling apps is one of the primary tasks of Portal and because of that it is deeply integrated into many parts of the Portal core.
Assumptions about how apps work and behave are scattered all over the codebase.
Many of them would no longer be true after the overhaul.
So I had to touch a lot of different modules, pull them apart and put them back together again.

The rest of this post goes over the major changes - planned, and unplanned, and opportunistic ones - that I made along the way.

# What is an App?

## Before

Before the overhaul, an app was essentially three things: 

1. a single Docker image (hosted somewhere) and 
2. the `app.json` file that contained metadata and configuration and
3. an image file that was the app's icon.

During installation, a large `docker-compose.yml` was updated 
that included all the apps that were installed on the Portal and the new app was added to it.
The `app.json` contained the necessary information to do that.

Over time, it turned out that the format of the `app.json` more and more resembled the format of a `docker-compose.yml` file.
Many values that need to be rendered into the `docker-compose.yml` had to be present in the `app.json` file.
I reinvented the wheel but in a more limited way, most importantly with the one-container-per-app limitation.

## After

So it was an obvious choice to just use `docker-compose.yml` files directly.
Each app now has its own `docker-compose.yml` file and Portal just starts it.
Right away, the primary goal was achieved: each app can consist of multiple containers.
As a bonus, lots of configuration can be directly expressed in the `docker-compose.yml` file in a well-known format
and can be thrown out of the `app.json` file.

However, I could not dispose of the `app.json` file completely. 
Some Portal-specific configuration was still needed like access control or lifecycle rules
and these cannot be expressed in a `docker-compose.yml` file.
So I kept it, renamed it to `app_meta.json` (because it is more clear and this was the perfect opportunity)
and cleaned it up.

While I was at it, I also added an option for apps to define the minimum Portal size they need to run.
Overleaf was the first app to use that because on the smallest Portal size, there is not enough memory to run all the required containers.

And as a small bonus, I also now publish a json schema file for the `app_meta.json` schema (see [here](../../../developer_docs/app_meta_json.md#schema){target=_blank}).
This makes it much easier to write that file because the schema can be used by an IDE for validation and auto-completion.

Back to the `docker-compose.yml`, it turned out to be insufficient for apps to provide a static file:
some apps need to be configured during installation.
In particular, many app developers will want to add a Portal's base URL, which is specific to each Portal, to the environment of an app.
So instead of providing the `docker-compose.yml` directly,
the app developer now needs to provide a `docker-compose.yml.template` file, which may contain variables in Jinja2 syntax. 
During installation, the `docker-compose.yml` file is generated from that.

So to sum up, an app now consists of the following four artefacts:

1. all needed Docker images (hosted somewhere) and 
2. the `app_meta.json` containing Portal-specific metadata and configuration and
3. the `docker-compose.yml.template` which is a template for the `docker-compose.yml` file and
4. an image file that is the app's icon.

The docs contain all the details about the new app format [here](../../../developer_docs/overview.md#app-format){target=_blank}.

And by the way, I of course also had to migrate all existing apps to the new format - or at least those that actually were used.

# App Store

## Before

Changing the app format meant that I also had an opportunity to change the app store backend.
Before, the app store was a GitLab repository that contained the `app.json` files and icons of all apps.
Portal would use the GitLab API to query the app store and download the files.
That seemed like a good idea at the time because it was easy to implement.

However, there were a few problems with that approach.
First, the GitLab API is not very fast.
After opening the app store, a Portal would take a few seconds querying.
Second, the GitLab API was never meant for hundreds or thousands of clients querying it all the time
which is after all what we are aiming for.
I was afraid that we would hit some rate limits at some point.

## After

The obvious solution was to move the app store to a CDN.
The app store is just a bunch of static files after all and CDNs are very good at serving those with low latency and high throughput.

So now, there is a CI/CD pipeline that builds a few files from the app store repository and pushes them to a CDN on Azure.
The different branches of the app store repository are placed under different paths on the CDN so that testing changes or additions
can be done by switching branches in the Portal UI.
The pipeline also creates a summary file that contains all the apps that are available in the app store 
with the metadata that is needed for displaying them in the UI.
(You can check it out [here](https://storageaccountportab0da.blob.core.windows.net/app-store/feature-docker-compose/all_apps/store_metadata.json){target=_blank}.)
That way, only a single request is needed to initially load the app store content (excluding the icons of course).

With a growing app store, I would also like to add a search feature for apps by name or description or keyword.
I am not sure yet, if, and how that could work with a backend that is just a bunch of static files.
If you have any ideas, please [let me know](mailto:contact@getportal.org/)!

# App Installation

## Before

I describe above how before the overhaul, installed apps were put into a large `docker-compose.yml` file, containing all apps.
The Portal core rendered this file but since it was itself a docker container, it could not directly start it - or so I thought at the time.
Instead, there was a systemd service running on the host that watched the file for changes and executed `docker-compose up` when it changed.
This kinda worked, but it was strange and surprising and not very robust.
In particular, installing multiple apps in rapid succession often lead to errors.

With the new system, there is now one `docker-compose.yml` file per app,
so I had to redo the starting of apps anyway.

## After

What I did not realize at the time and would have saved a lot of work is that
by mounting the docker socket, the Portal core container can control the docker daemon directly.
No need for systemd to call docker commands.
That way, the Portal core container can now issue docker-compose commands to start and stop apps
and do anything else that is needed.

So now the installation process is as follows:

1. Portal core downloads the app's files from the app store.
2. Portal core updates its internal database with the app's metadata.
3. Portal core renders the `docker-compose.yml` file from the template.
4. Portal core updates the configuration for the Traefik reverse proxy.

And when the app receives a request, Portal core simply starts the app's docker-compose file.

Since the Portal core does everything itself now, there is much more control and visibility of app management,
enabling a few more useful features.

* If the user installs multiple apps in rapid succession, we can queue the installations and execute them sequentially.
* The UI can show a spinner for an app icon as long as the app is still installing.
* The UI can show a running indicator for an app that is currently running.
* When an app fails to install, the UI can show an error message so that the user is at least informed about the problem.

Of course the last three items need some kind of push mechanism to update the UI.
And you probably know where this is going.

# Websockets

This next section is so obvious, the AI-copilot even suggested the correct heading.

## Before

Until now, there was no websocket integration at all.
I just did not see it as a priority and the very few times it was needed, polling was good enough.
Now with the changes to the app installation process, I really wanted to show users what is happening in real time.

## After

Fortunately, FastAPI has built-in support and makes websockets really easy to add.
I also took the additional step and integrated websockets with the [Python blinker library](https://blinker.readthedocs.io/en/stable/#){target=_blank},
which I have been using for internal signals for a while now.
So now there is something of a very lightweight internal event bus using blinker
with a subset of events being additionally published to websockets.

The frontend which is built with Vue.js reacts to websocket events by publishing them to a global event bus
and by updating the VueX store if needed.
This allows me to use the same list of event names and payload schemas across the whole application.

# Misc

These were the large changes, but there were also a few smaller ones that were needed or just made sense to do at the same time.

* I removed the shared Postgres container that was running on every Portal and that apps could use.
    The original plan was to add many more of these shared services but now that each app can spin up its own auxiliary containers,
    there really is no need anymore.
* There is one docker-compose file that configures the mandatory containers that make up a Portal which are
    the Portal core, the Traefik reverse proxy and a container that statically serves the web frontend.
    In this file, the containers were defined with the `:latest` tag which meant that each restart could update them to the latest version.
    This was a bit uncontrollable, so I define the exact version now and push a new `docker-compose.yml` file from the backend onto each Portal when I do an update.
* With the new app format, apps can in principle mount any host directory.
    I prevent this by policy by not adding apps to the store that do this.
    However, it is also an opportunity to give some privileged apps more access to the host.
    Like the filebrowser app that can now see all files of all apps.
* Since the overhaul included so many deep changes, existing Portals could not be updated automatically by existing means.
    So I added a migration tool that can update a Portal to the new format.
    Hopefully, I can use it as a template in case of future deep changes.
* App developers must be informed about the new app system and how to use it.
    So I overhauled all the pages of the documentation that were related to the changes (which were almost all of them).

# Conclusion

The tasks described above were only the ones that warranted a note on the ever-growing and ever-changing section of todos for this feature.
So all in all, this was a large undertaking, one that took me about two months to complete.
The changes were spread out over 48 commits, the first one being on 2023-05-22 and the last one on 2023-07-18
and touching 103 files.

Of course, this is not the best way to do things and I only did it because as a single developer,
there is no coordination overhead.
The benefits of having full control, I guess.

Anyway, I hope you enjoyed this little insight into the development process of Portal
and are eager to try out the new app system.
Feel free to submit your own apps to the app store ([learn how](../../../developer_docs/overview.md){target=_blank})
and let us know what you think!
