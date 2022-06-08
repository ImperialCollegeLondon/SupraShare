# SupraShare

A platform for sharing interactive versions of trained machine learning models for
chemistry.

## Overview

This repo acts as a template for creating an interactive webapp for one trained model.
The [SupraShare homepage](https://suprashare.rcs.ic.ac.uk/) hosts several webapps
created using this template.

For a working example that closely resembles the model in this template see the
[cage prediction webapp repo](https://github.com/ImperialCollegeLondon/cage-prediction-webapp).

While the app in this template will start if run locally as is, it does not contain any
working ML model. The reason for this is so we could include more features that you may
wish to include in your app, not all of which are compatible with the cage prediction
model.

## Using this template

GitHub makes it easy to [create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).
We recommend: Naming the repository `<model-name>-webapp` and including only the default
branch (`develop`). A new `main` branch can be created afterwards for CI/CD purposes
(see [below](#tests-ci--cd)).

### Template structure

The code in this template is separated into several submodules depending on its function.

TODO: 1 sentence/bullet point per file describing its purpose.

```mermaid
  graph TD;
      Components-->Layout;
      Model-->Callbacks;
      Callbacks-->App;
      Layout-->App;
 ```

### Running locally with Docker

### Tests, CI & CD

A [Docker image of the containerised app](https://github.com/ImperialCollegeLondon/SupraShare/pkgs/container/suprashare%2Fsuprashare) is automatically generated [using GitHub actions](https://github.com/ImperialCollegeLondon/SupraShare/blob/develop/.github/workflows/ci.yml) when changes are merged into the main branch.

The image is added to the webserver at [suprashare.rcs.ic.ac.uk](https://suprashare.rcs.ic.ac.uk) by manually updating (i) the [docker-compose.yml file](https://docs.docker.com/compose/compose-file/) (ii) the [reverse proxy config](https://caddyserver.com/docs/caddyfile) and (iii) the static index page (front page of the web site), all within the virtual machine running the webserver.

### Best practice checklist

Each newly created app based on this template should include:

- Details of any pulication and archived data relating to the model, including DOIs
- A detailed specification of the programming environment used to reproduce results
- Instructions on how to use the app (allowed input format(s) and expected output(s))
- Unit tests for the underlying model (expected outputs for given inputs)

## Deployment

### Checklist for deployment

### Webserver setup

### Docker and docker-compose

## Development

SupraShare is jointly developed by the [Jelfs Research Group](http://www.jelfs-group.org/) and the Imperial College [Research Software Engineering Team](https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/research-software-engineering/).
