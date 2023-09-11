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
With the latest update, we did the opposite of that.

<!-- more -->

# The Inciting Incident

We wanted to include Overleaf in our app store.
Overleaf is a web-based LaTeX editor that is very popular among scientists and students
and would make a great addition.
It is especially useful because writing with LaTeX can be painfully technical and Overleaf just takes care of most of the details for you. 

However, it turns out that Overleaf has a few requirements in the form of other containers that need to be running on the same machine,
namely a Redis server and a MongoDB database.
And that is something that Portal just did not support.
Now, in the past, we sometimes worked around this by building a new image for the app that includes and starts all the required processes.
But that can be tricky and error-prone and goes against the idea of Docker containers doing only one thing at a time.

So it was a good time to tackle a task that has been sitting in the backlog for quite some time:
overhauling the app integration system.

# Taking it all Apart

![Mechanic and disassembled machine](./mechanic.jpg){ width="500" }

Handling apps is one of the primary tasks of Portal which means that it is deeply integrated into many parts of the Portal core.
Assumptions about how apps work and behave are scattered all over the codebase.
Many of them would no longer be true after the overhaul.
So we had to touch a lot of different modules, pull them apart and put them back together again.

The rest of this post is a list of the changes - planned ones and unplanned ones - that we made along the way.

# What is an App?

## Before

Before the overhaul, an app was a single Docker image and the `app.json` file that contained metadata and configuration.
During installation, a large `docker-compose.yml` was updated 
that included all the apps that were installed on the Portal and the new app was added to it.
The `app.json` contained the necessary information to do that.

Over time, it turned out that the format of the `app.json` more and more resembled the format of a `docker-compose.yml` file.
Many values that need to be rendered into the `docker-compose.yml` had to be present in the `app.json` file.
We reinvented the wheel but in a more limited way, most importantly with the one-container-per-app limitation.

## After

So it was an obvious choice to just use `docker-compose.yml` files directly.
Each app now has its own `docker-compose.yml` file and Portal just starts it.
Right away, the primary goal was achieved: each app can consist of multiple containers.
As a bonuns, lots of configuration can be directly expressed in the `docker-compose.yml` file in a well-known format.

However, some Portal-specific configuration was still needed like access control or lifecycle rules.
Since these cannot be expressed in a `docker-compose.yml` file,
we still needed some parts of the `app.json` file.
So we kept it, renamed it to `app_meta.json` (because it is more clear and this was the perfect opportunity)
and cleaned it up a bit.

While we were at it, we also added an option for apps to define the minimum Portal size they need to run.
Overleaf was the first app to use that because on the smallest Portal size, there is not enough memory to run all the required containers.

And as a small bonus, we also now publish a json schema file for the `app_meta.json` schema.
This makes it much easier to write that file because the schema can be used by an IDE for validation and auto-completion.

Back to the `docker-compose.yml`, it turned out to be insufficient for apps to provide a static file:
some apps need to be configured during installation.
In particular, we want to be able to add a Portal's base URL, which is specific to each Portal, to the environment of an app
because that is something many apps need.
So the app developer needs to provide a `docker-compose.yml.template` file, which may contain variables in Jinja2 syntax, 
and the `docker-compose.yml` file is generated at install time from that.

So to sum up, an app is now a directory that contains the following files:

* `app_meta.json`: Portal-specific metadata and configuration
* `docker-compose.yml.template`: A template for the `docker-compose.yml` file
* An image file that is the app's icon

And by the way, we of course also had to migrate all existing apps to the new format.

# App Store

## Before

Changing the app format meant that we also had an opportunity to change the app store backend.
Before, the app store was a GitLab repository that contained the `app.json` files and icons of all apps.
Portal would use the GitLab API to query the app store and download the files.
That seemed like a good idea at the time because it was easy to implement.

However, there were a few problems with that approach.
First, the GitLab API is not very fast.
After opening the app store, a Portal would take a few seconds querying.
Second, the GitLab API was never meant for hundreds or thousands of clients querying it all the time
which is after all what we are aiming for.
We were afraid that we would hit some rate limits at some point.

## After

The obvious solution was to move the app store to a CDN.
The app store is just a bunch of static files after all and CDNs are very good at serving those with low latency and high throughput.

So now, there is a CI/CD pipeline that builds a few files from the app store repository and pushes them to a CDN on Azure.
We still keep the different branches of the app store repository in sync with the CDN so that we can easily test changes or additions
by switching branches in the Portal UI.
And we create a summary file that contains all the apps that are available in the app store with the metadata that is needed for displaying them in the UI.
(You can check it out [here](https://storageaccountportab0da.blob.core.windows.net/app-store/feature-docker-compose/all_apps/store_metadata.json){target=_blank}.)
That way, only a single request is needed to initially load the app store content (excluding the icons of course).

With a growing app store, we would also like to be able to search for apps by name or description or keyword.
We are not sure yet, if, and how that could work with a backend that is just a bunch of static files.
If you have any ideas, please let us know!

# App Installation

## Before

We describe above how installed apps were put into a large `docker-compose.yml` file, containing all apps.
The Portal core rendered this file but since it was itself a docker container, it could not directly start it - or so we thought at the time.
So instead, there was a systemd service running on the host that watched the file for changes and executed `docker-compose up` when it changed.
This kinda worked, but it was strange and surprising and not very robust.
In particular, installing multiple apps in rapid succession often lead to errors.

With the new system, we have one `docker-compose.yml` file per app,
so we had to redo the starting of apps anyway.

## After

What we did not realize at the time and would have saved us a lot of work is that
by mounting the docker socket, we can control the docker daemon from inside the container.
No need for systemd to call docker commands.
That way, the Portal core container can now directly issue docker-compose commands to start and stop apps
and do anything else that is needed.

So now the installation process is as follows:

1. Portal core downloads the app's files from the app store.
2. Portal core updates its internal database with the app's metadata.
3. Portal core renders the `docker-compose.yml` file from the template.

And when the app gets a request, Portal core simply starts the app's docker-compose file.

Since the Portal does everything itself now, there is much more control and visibility of app management,
enabling a few more useful features.

* If the user installs multiple apps in rapid succession, we can queue the installations and execute them sequentially.
* We can show a spinner for an app icon as long as the app is still installing.
* We can show a running indicator for an app that is currently running.
* When an app fails to install, we can show an error message so that the user is at least informed about the problem.

Of course the last three items need some kind of push mechanism to update the UI.
And you probably know where this is going.

# Websockets

This next section is so obvious, the AI-copilot even suggested the correct heading.

## Before

Until now, we had no websocket integration.
We just did not see it as a priority and the very few times we needed it, we used polling.
Now with the changes to the app installation process, we really wanted to show users what is happening in real time.

## After

Fortunately, FastAPI has built-in support and makes websockets really easy to add.
We also took the additional step and integrated websockets with the [Python blinker library](https://blinker.readthedocs.io/en/stable/#){target=_blank},
which we have been using for internal signals for a while now.
So now we have something of a very lightweight internal event bus using blinker
with some events being additionally published to websockets.

On the frontend where we use Vue.js, we react to websocket events by publishing them to a global event bus
and by updating the VueX store if needed.
This allows us to use the same list of event names and payload schemas across the whole application.

# Misc

These were the large changes, but there were also a few smaller ones that were needed or just made sense to do at the same time.

* We removed the Postgres container that was running on every Portal and that apps could use.
    The original plan was to add many more of these shared services but now that each app can spin up its own auxiliary containers,
    there really is no need anymore.
* There is one docker-compose file that configures the basic containers that make up a Portal:
    the Portal core, the Traefik reverse proxy and a container that statically serves the web frontend.
    In this file, the containers were defined with the `:latest` tag which meant that each restart could update them to the latest version.
    This was a bit uncontrollable, so we define the exact version now and push a new `docker-compose.yml` file from the backend when we want to update.
* With the new app format, apps can in principle mount any host directory.
    We prevent this by policy by not adding apps to the store that do this.
    However, it is also an opportunity to give some privileged apps more access to the host.
    Like the filebrowser app that can now see all files of all apps.
* Existing Portals could of course not be updated automatically by existing means.
    So we added a migration tool that can update a Portal to the new format.
    Hopefully, we can use it as a template in case of future deep changes.
* App developers must be informed about the new app system and how to use it.
    So we overhauled all the pages of the documentation that were related to the changes (which were almost all of them).

# Conclusion

The tasks described above were only the ones that warranted a note on the ever-changing section of todos for this feature.
So all in all, this was a large undertaking, one that took us about two months to complete.
The changes were spread out over 48 commits, the first one being on 2023-05-22 and the last one on 2023-07-18
and touching 103 files.

Of course, this is not the best way to do things and I only did it because as a single developer,
there is no coordination overhead.
The benefits of having lone control, I guess.

Anyway, I hope you enjoyed this little insight into the development process of the Portal
and are eager to try out the new app system.
Feel free to submit your own apps to the app store and let us know what you think!
