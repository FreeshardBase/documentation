# Apps

The iPhone would not be feasible without its app store.
It turns this hardware platform with its sensors, touchscreen, outputs and connectivity into a million different devices for all kinds of use-cases.
Although the concept of applications is as old as the first computers, 
only smartphones turned them in those easily digestible packages with colorful icons and a simple way to install and launch them.
So it makes only sense to replicate that on a platform like freeshard.

## What is an App

Apps on freeshard work very similar to apps on a smartphone.
They are programs that run on the shard and provide some kind of functionality.
An app is started when it is used and stopped after a while of inactivity.
Freeshard features an app store where the owner can browse, install, and remove apps.

The current selection of apps consists mainly of popular self-hosted applications.
They are preconfigured to work on freeshard and in order to keep freeshard simple, the configuration is not exposed to the owner.

## Technical Background

Apps on freeshard are Docker containers, or more precisely, collection of Docker containers.
Each app is a separate Docker Compose project, with a `docker-compose.yml` file defining the services that make up the app.
Some variables in this file are placeholders that are filled in by freeshard when the app is installed.

The app's GUI is served by a web server and piped through the shard's reverse proxy.
Here, access control is enforced, so that only the owner and paired devices can access the app.
However, it is possible to make certain parts of the app public, so that they can be accessed by anyone.
This is used for sharing data or functionality with others.

Since freeshard does access control itself, additional access control mechanisms in the app are not needed and only would get in the way of a smooth user experience.
So whenever possible, apps are configured for a single user without login.

Freeshard implements a basic lifecycle management for apps.
When a http request is made to the app, it is started if it is not running.
In the meantime, a simple self-refreshing splash screen is shown.
After a while of inactivity, the app is stopped.
This conserves a shard's resources and allows owners to install as many apps as they like, 
just like they are used to from their smartphone,
since they are never all running at the same time.
