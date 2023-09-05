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
Now, in the past, we sometimes worked around this by building a new image that includes and starts all the required processes.
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

Before the overhaul, an app was a single Docker image and the `app.json` file that contained metadata and configuration.
During installation, a large `docker-compose.yml` was updated that included all the apps that were installed on the Portal.
The `app.json` contained the necessary information to do that.
Over time, it turned out that the format of the `app.json` more and more resembled the format of a `docker-compose.yml` file.
We reinvented the wheel but in a more limited way, most importantly with the one-container-per-app limitation.

So it was an obvious choice to just use `docker-compose.yml` files directly.
Each app would have its own `docker-compose.yml` file and Portal would just start it.
Right away, each app could now consist of multiple containers.

However, some Portal-specific configuration was still needed like access control or lifecycle rules.
Since these cannot be expressed in a `docker-compose.yml` file,
we still needed parts of the `app.json` file.
So we kept it, renamed it to `app_meta.json` (because it is more clear and this was the perfect opportunity)
and cleaned it up a bit.
We also added an option for apps to define the minimum Portal size they need to run.
Overleaf was the first app to use that because on the smallest Portal size, there is not enough memory to run all the required containers.
As a small bonus, we also now publish a json schema file for the `app_meta.json` schema.
This makes it easier to write apps because the schema can be used for validation and auto-completion.

In addition, it turned out to be insufficient for apps to provide a static `docker-compose.yml` file:
some apps need to be configured during installation.
In particular, we want to be able to add a Portal's base URL to the environment of an app
because that is something many apps need.
So the `docker-compose.yml` file is now generated at install time from a `docker-compose.yml.template` file
which may contain variables.

So to sum up, an app is now a directory that contains the following files:

* `app_meta.json`: Portal-specific metadata and configuration
* `docker-compose.yml.template`: A template for the `docker-compose.yml` file
* An image file that is the app's icon

And by the way, we of course also had to migrate all existing apps to the new format.

# App Store

Before, Portal queried GitLab API.
Now, app files are pushed to a CDN and Portal queries that.
Much better performance and prepares for the increase in the number of apps.

# App Installation

Installation sequentially to avoid existing bug.
Before there was systemd that detected a change in the `docker-compose.yml` file,
now the Portal core container uses the docker socket directly.
Errors during app installation are more clearly communicated to the user.

# Life UI Updates

Now that app installation can be deferred, UI should update on its own via websockets.
There was no websocket support, so we added it.
We took the opportunity and used it for other things as well like a running indicator.
Also integration with python blinker for state change updates.

# Removals

Common service: Postgres

# Misc

Update of Portal exclusively through push from backend. This makes it more controlled and easier to test. Self-service is planned.

With docker-compose it is possible to let apps access any directories. So filebrowser is now privileged and can see all apps' files.

Migration tool for existing Portals.

Overhaul of documentation.

# Conclusion

These were only the main tasks, there were many more smaller ones.
48 commits, first commit was 2023-05-22, last commit was 2023-07-18.
Changes to 103 files.

