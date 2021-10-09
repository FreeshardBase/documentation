# The app.json File

In order for Portal to recognize your app, you have to provide an `app.json` file 
containing some metadata and instruction on how to run your app.

Example:
```json
{
  "name": "ghost",
  "description": "A free and open source blogging platform, designed to simplify the process of online publishing for individual bloggers as well as online publications",
  "image": "ghost:alpine",
  "port": 2368,
  "data_dirs": [
    "/var/lib/ghost/content"
  ],
  "env_vars": {
    "url": "https://ghost.{{ portal.domain }}/"
  },
  "authentication": {
    "default_access": "public",
    "private_paths": ["/ghost/"]
  }
}
```