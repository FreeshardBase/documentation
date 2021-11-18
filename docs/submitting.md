# Submitting to the App Store

When your app is ready and tested, you can submit it to be listed in the Portal app store.
This allows all other Portal users to find and install it with a single click.

---

The backend of Portal's app store is [this repository on GitLab](https://gitlab.com/ptl-public/app-repository).
There is a folder for each app containing the `app.json` and the app's icon.
To submit your app, request contributor access to the repository
and create a merge request in which you add the folder for your app.
Obviously, you may not modify any other apps except your own.

When committing your changes, please name your branch `app/<your-app>`.

If you make changes to your app that warrant a modification of the `app.json`,
you may do so by committing to the same branch name 
and submitting another merge request
