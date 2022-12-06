# Overview

Your app is made up of two distinct artifacts: the docker image that contains the app 
and the `app.json` file that tells a Portal how to run the image. 

---

## The App Image

Your docker image is run on the user's Portal when they install your app.
It must contain a web-service which means it must serve HTTP (not HTTPS!) on some port.
How exactly you accomplish this is up to you.
You may e.g. use rendered templates for each view of your app.
Or you may build a web application that runs in the browser and queries data using a RESTful interface.
You also may use any language or framework you like best.

However, we ask you to make your UI responsive.
Portal provides an omni-device user experience, so every app should be equally comfortable to use,
whether on a notebook, tablet or smartphone.

By default, only the Portal's owner can access your app's UI, 
which means the terminals they have paired with their Portal.
If you want to make part of your app public or usable by the owner's peers, you can do so.
See [Routing and Access Control](routing_and_ac.md) to learn how.

At the moment we do not provide hosting for any images.
You can use [Docker Hub](https://hub.docker.com/) or any other docker repository for that.
Or, if for any reason you do not want to host your image, contact us and we will work something out.

## The `app.json` File

Every Portal app is accompanied by an `app.json` file.
It is not part of the image but defines the context in which the image must be executed on a user's Portal.

Things you have to configure here are:

* the identifier of your docker image such that the Portal knows which image to load,
* the port at which your app's UI is published,
* directories inside the docker image where paths from the host should be mounted,
* URL-paths that should be public or private or only reachable for peers.

In addition, this file contains metadata like the app's name, its version and a description
that will be shown in the app store and other places.

Read more about configuration options on the [page about `app.json`](app_json.md).
