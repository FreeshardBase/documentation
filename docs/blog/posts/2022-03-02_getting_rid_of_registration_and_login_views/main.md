---
draft: false 
date: 2022-03-02
authors:
  - max
---

# Getting rid of Registration and Login Views

We are continuously working on bringing more apps into our app store. But since we are using apps that were originally made for self-hosting, we often need to make some tweaks. In particular, we want the user to be able to open an app after installation without the need to go through a registration or login form. Each Portal is mainly a single-user platform so that would be quite confusing.

<!-- more -->

Some apps can be configured with a proxy auth feature out of the box. It can often be enabled from an environment variable and causes the app to read the logged-in user from a http header. This works great if it is deployed behind a reverse proxy that handles authentication and sets the header - exactly the situation that we have on the Portal, so that is our favourite way of getting rid of confusing login screens.

For the sake of simplicity, we want to be able to apply the needed configuration purely through settings in the app.json file, if possible. Setting environment variables has been possible for a long time. But configuring http headers that are added to all requests that are forwarded to the app was not possible. That has now changed and you now can specify these http headers in app.json. See [the updated documentation](https://docs.getportal.org/developer_docs/routing_and_ac/){target=_blank} for more information.

In fact, we had to add another feature as a dependency: [app.json format versions](https://docs.getportal.org/developer_docs/app_json/#versioning){target=_blank}. Up until now, there was only one valid format for the app.json document at a time. But with the http header feature, we wanted to fundamentally change the way URL paths are configured. For that to go smoothly, we introduced version 1.0 of the app.json format. Portal still understands version 0.0 though and transparently converts those older documents to 1.0.

We believe that this change will make it easier to adapt apps to the Portal app store and in particular to make the user experience smoother by getting rid of registration and login views.
