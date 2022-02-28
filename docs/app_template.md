# The App Template

When building a Portal app from scratch, there is a lot of scaffolding to do
before you can start on the actual business logic.
We prepared a template for Portal apps written in Python that you can use to quickly bootstrap a new app.

---

!!! info ""
    The app template is hosted [here on GitLab](https://gitlab.com/ptl-public/app-template-python).
    To get started, simply fork it and start building. 

## Features

This template provides quite a bit of scaffolding, so you can directly start implementing business logic.
However, what we provide is also very opinionated in order to work right out of the box.
At some point in time, you might want to revisit our assumptions 
and replace the boilerplate with something more suited to your needs. 

### Endpoints

Two endpoints are provided, a private one and a public one.
Their implementation is in `app_template/web/private.py` and `app_template/web/public.py`.

The private endpoint demonstrates how to use the `AuthValues` dependency 
to access the requesting terminal's name and id.
This dependency is defined in `app_template/web/dependencies.py`.

### Config

Use the `config.yml` to maintain configuration that you would rather not hard-code.
Access the values using [gconf](https://gitlab.com/max-tet/gconf/).
The configuration is loaded during startup.

### TinyDB

We added [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) for persistence.
Since Portal apps are often single-user apps, there is rarely need for the usual ACID features.
TinyDB instead offers simplicity and flexibility and lets you start quickly.

It is initialized in `app_template/database.py` and used in `app_template/web/private.py` and `app_template/web/public.py`
to count the number of calls to each endpoint.

The database file is stored in `/user_data` where a persistent host directory is mounted.
See below for the `app.json` where this is specified.
When running the app locally, you can overwrite the location of the database file
with the environment variable `GCONF_DATABASE_FILENAME`.
See the [gconf docs](https://gitlab.com/max-tet/gconf#environment-variables-override) for how that works.

### Logging

Log output is configured with a sensible format to stdout.
Use the usual `log = logging.getLogger(__name__)` at the top of your files to access the logger.
You may also change the log level of individual modules through the `config.yml`.
An example is provided there.

### Icon

At `portal_meta/icon.svg` there is an icon that will be displayed on the Portal home screen.
Replace it with your own.

### GitLab-CI

There is a `.gitlab-ci.yml` already prepared.
It contains stages for unittests, Docker build and a rudimentary integration test.
Tagged commits are assumed to be releases and cause the build of a version-tagged Docker image
and the open API documentation released to GitLab pages.

### Docker

Built Docker images are pushed to the GitLab project's build-in registry
as part of the GitLab-CI pipeline.

### PyTest

Unittests with PyTest are already setup under `tests/` and there are some examples.
They demonstrate how you can perform API calls and test the responses.

The whole test suite is executed as part of the GitLab-CI pipeline.

### Open API docs

When running the app, the open API documentation is hosted at `/openapi`.
Its JSON-format is available at `/openapi.json`.

During the GitLab-CI pipeline, if the commit is tagged,
the documentation is uploaded to the project's GitLab pages space.

## Install the template

This template is a fully functioning Portal app, and it is available in the app store.
It just does not do a lot, and it is up to you to fill it with content.

Use the `app.json` below as a starting point for your own one.
Adapt it to your app by changing at least the name, description and image.

```json
{
  "v": "1.0",
  "name": "app-template-python",
  "description": "A fully functional and minimal Portal app that can be used to quickly bootstrap a new app using Python",
  "image": "registry.gitlab.com/ptl-public/app-template-python:master",
  "port": 80,
  "data_dirs": [
    "/user_data"
  ],
  "paths": {
    "": {
      "access": "private",
      "headers": {
        "X-Ptl-Client-Id": "{{ client_id }}",
        "X-Ptl-Client-Name": "{{ client_name }}",
        "X-Ptl-Client-Type": "terminal",
        "X-Ptl-Foo": "bar"
      }
    },
    "/public/": {
      "access": "public",
      "headers": {
        "X-Ptl-Client-Type": "public",
        "X-Ptl-Foo": "bar"
      }
    }
  }
}
```

## Submit your app to the app store

When you feel that your app is ready to be released, you can submit it to the app store.
See [here](submitting.md) for details.