# Overview

Your app is made up of two distinct artifacts: the docker image that contains the app 
and the `app.json` file that tells a Portal how to run the image. 

---

## The App Image

Your docker image is run on the user's Portal when they install your app.
It must contain a web-service which means it must serve http on some port.
How exactly you accomplish this is up to you.
You many e.g. use rendered templates for each view of your app.
Or you may build a web application that runs in the browser and queries data using a RESTful interface.
That means you also may use any language or framework you like best.

However, we ask you to make your UI responsive.
Portal provides an omni-device user experience, so every app should be equally comfortable to use
weather a notebook, tablet or smartphone is used to access it.

## The `app.json` File

When your docker images is executed on the user's Portal, 
the `app.json` file allows you to provide some option that control its execution.
E.g. you have to configure the port which should be forwarded or file paths that should be mounted
and of course the identifier of your docker image such that the Portal knows which image to load.

In addition, this file contains metadata like the app's name, its version and a short and a long description
that will be shown in the app store and other places.

Read more about configuration options at the [page about `app.json`](app_json.md).
