# SupraShare

A platform for sharing interactive versions of trained machine learning models for
chemistry.

## Overview

This repo acts as a template for creating an interactive webapp for one trained model.
The [SupraShare homepage](https://suprashare.rcs.ic.ac.uk/) hosts several webapps
created using this template, all of which require completely different Python environments.
We use [Docker](https://www.docker.com/) to keep these environments separated and [Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
as a webserver with a reverse proxy to make each webapp accessible.

While the app in this template will start if run locally as is, it does not contain any
working ML models. The reason for this is so we could include more features that you may
wish to use in your app, not all of which are compatible with the cage prediction
model.

For a working example that closely resembles the model in this template see the
[cage prediction webapp repo](https://github.com/ImperialCollegeLondon/cage-prediction-webapp).

## Using this template

### Creating a repository

GitHub makes it easy to [create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).
We recommend naming the repository `<model-name>-webapp` and including only the default
branch (`develop`). A new `main` branch can be created afterwards for deployment purposes
(see [below](#tests-ci--cd)).

### Template structure

#### Website

The code in the `website` directory uses [Plotly Dash](https://plotly.com/dash/) and is
separated into several submodules. The terminology is well-explained in the [Dash documentation](https://dash.plotly.com/introduction).
It also uses [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/) for styling,
layout and interactive components.

Of the below files, **Layout**, **Model** and **Callbacks** are designed to be adapted to suit
the needs of the webapp. The others - **App**, **Components** and **Drawer** - are intended to
mostly be imported as-is (just like any other Python package). 

- **Components:** Each component used on the webpage and imported in **Layout** is defined here. Generally these are functions that return a dash core or dash bootstrap component. These components are designed to be flexible and reusable and contain detail on how to use them in docstrings.
- **Drawer:** The components that are unique to the JSME Drawer - also imported in **Layout**. This is in a separate module due to dependency restrictions with older versions of scikit-learn.
- **Layout:** The content for the webpage is defined here, based on imported components.
- **Model:** Functions that load, prepare and run the actual ML model(s).
- **Callbacks:** Functions that are automatically called whenever an input component's property changes. These functions make the app interactive and are how users can interact with the underlying model.
- **App:** The main python file to run the webapp. Brings together the **Layout** and **Callback** components and sets various important variables such as APP_NAME and URL_PATH.

Note: some callbacks are defined in **Callbacks** and others in **Components** and **Drawer**.
Those in **Callbacks** are app-specific and where we recommend adding your own callbacks, the
others are there to make the custom components interactive.

```mermaid
  graph TD;
      Components-->Layout;
      Model-->Callbacks;
      Callbacks-->App;
      Layout-->App;
 ```

#### Models

The trained ML models themselves should be put here, usually in a pickled format or
similar.

#### Tests

Unit tests that check your model(s) give expected outputs for given inputs go here.
You could also include more advanced tests to ensure the webapp behaves as expected.

#### Config files

As well as the usual files such as `LICENCE`, `.gitignore` etc., we have:

- `.github/workflows/ci.yml`, `.flake8` and `.pre-commit-config.yaml` used for [continuous integration](#ci--cd).
- `Dockerfile` and `docker-compose.yml` contain settings used by [Docker](#build-and-run-with-docker).

### Build and run with Docker

#### Dockerfile

[Docker](https://www.docker.com/) is used to set up a container within which the webapp
runs. The `Dockerfile` is used by Docker to build the image that defines the
container automatically. In our case, the steps are to pull a miniconda3 parent image
then set up a conda environment.

When a container based on the image starts running the webapp server is started and the
correct port is exposed. More information on the `Dockerfile` can be found [here](https://docs.docker.com/engine/reference/builder/).

*Note:* The continuumio/miniconda3 parent image is quite large (although smaller than an anaconda equivalent) and still uses anaconda so can be slow to build complex environments.
You may consider using [micromamba](https://github.com/mamba-org/micromamba-docker) to
speed things up a bit.

#### docker-compose.yml

The [`docker-compose` command](https://docs.docker.com/compose/) is used to orchestrate
multi-container Docker applications and the YAML file configures this. For development,
the YAML file in this repository is very simple as there is only one container (for the
webapp) which is named `web` in the YAML file.

The command `docker-compose up --build` is used to build the image(s) then start the
containers.

`docker-compose` is more useful (and the config more complicated) in the [deployment](#deployment)
environemnt where multiple webapps containing different models are being run.

### CI & CD

[Github Actions](https://github.com/features/actions) are used to run code quality checks
on push and pull events. The [pre-commit](https://pre-commit.com/) configuration is used
for this. As the name suggests, these hook scripts can be used to identify problems before
committing code. To set this up on your local machine run:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files # optionally to run once on everything
```

For easy deployment, a [Docker image](https://github.com/ImperialCollegeLondon/SupraShare/pkgs/container/suprashare)
is automatically generated [according to the ci.yml config](https://github.com/ImperialCollegeLondon/SupraShare/blob/develop/.github/workflows/ci.yml) when changes are merged into the main branch.

## Deployment on the webserver

### Webserver overview

The webserver setup consists of only a few configuration files:

- **docker-compose.yml** configures the multi-container docker setup as described above and
- **docker-compose.override.yml** handles the automatic pulling of new images using [watchtower](https://github.com/containrrr/watchtower).
- **Caddyfile** configures the [Caddy](https://caddyserver.com/docs/caddyfile) webserver, mainly handling the reverse proxy that directs client requests to the correct webapp.
- **app_list.yml** is used internally by each app to provide links to other apps in the navbar.
- **index.html** is used by Caddy as the homepage, with links to each webapp.

All of these files need updating (apart from `docker-compose.override.yml`) when a new
webapp is added.

### Adding a new model

The webserver at is configured to periodically check the package repositories specified
in `docker-compose.yml` for new images. Assuming this is called `new-webapp` (and the repository
address is `imperialcollegelondon/new-webapp) a new service needs to be specified in
`docker-compose.yml`, e.g.:

```diff
services:
  cage-prediction-webapp:
    image: ghcr.io/imperialcollegelondon/cage-prediction-webapp:main
    environment:
      - APP_NAME=Is My Cage Porous?
      - URL_PREFIX=/is-my-cage-porous
    restart: unless-stopped
    volumes:
      - ./app_list.yaml:/usr/src/app/app_list.yaml
+ new-webapp:
+   image: ghcr.io/imperialcollegelondon/new-webapp:main
+   environment:
+     - APP_NAME=New App Name
+     - URL_PREFIX=/new-webapp
+   restart: unless-stopped
+   volumes:
+     - ./app_list.yaml:/usr/src/app/app_list.yaml
```

The `Caddyfile` must be updated to direct requests to the new app:

```diff
https://suprashare.rcs.ic.ac.uk {
  tls /srv/cert /srv/key
  reverse_proxy /is-my-cage-porous/* cage-prediction-webapp:8050
+ reverse_proxy /new-webapp/* new-webapp:8050
  file_server {
    root /srv/www/root/
  }
```

The `app-list.yaml` should include a new mapping of the APP_NAME to the URL path:

```diff
  Home: /
  Is My Cage Porous?: /is-my-cage-porous/
+ New App Name: /new-webapp/
```

Finally, a link should be added in `index.html` to the new App. In it's current, very
basic form this might look like:

```diff
<!doctype html>
<html>
  <head>
  <title>SupraShare Landing Page</title>
  </head>
  <body>
    <p><a href="/is-my-cage-porous/">Is My Cage Porous?</a></p>
+   <p><a href="/new-webapp/">New App Title</a></p>
  </body>
</html>
```

## Ongoing development

SupraShare is jointly developed by the [Jelfs Research Group](http://www.jelfs-group.org/) and the Imperial College [Research Software Engineering Team](https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/research-software-engineering/).

Please use the GitHub [Issue Tracker](https://github.com/ImperialCollegeLondon/SupraShare/issues)
to ask questions, report bugs and request features.

## Reproducibility of results

Each newly created app based on this template should include in the README:

- Details of any pulication and archived data relating to the model, including DOIs
- Instructions on how to use the app (allowed input format(s) and expected output(s))
- Instructions for running unit tests
