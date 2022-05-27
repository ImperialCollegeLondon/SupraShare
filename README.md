# SupraShare

A platform for sharing trained machine learning models for chemistry.

## Overview

This repo acts as a template for creating an interactive web app for one trained model.

A [Docker image of the containerised app](https://github.com/ImperialCollegeLondon/SupraShare/pkgs/container/suprashare%2Fsuprashare) is automatically generated [using GitHub actions](https://github.com/ImperialCollegeLondon/SupraShare/blob/develop/.github/workflows/ci.yml) when changes are merged into the main branch.

The image is added to the webserver at [suprashare.rcs.ic.ac.uk](https://suprashare.rcs.ic.ac.uk) by manually updating (i) the [docker-compose.yml file](https://docs.docker.com/compose/compose-file/) (ii) the [reverse proxy config](https://caddyserver.com/docs/caddyfile) and (iii) the static index page (front page of the web site), all within the virtual machine running the webserver.

## Template structure

The code in this template is separated into several submodules depending on its function.

TODO: 1 sentence/bullet point per file describing its purpose.

```mermaid
  graph TD;
      Components-->Layout;
      Model-->Callbacks;
      Callbacks-->App;
      Layout-->App;
 ```

## Development

SupraShare is jointly developed by the [Jelfs Research Group](http://www.jelfs-group.org/) and the Imperial College [Research Software Engineering Team](https://www.imperial.ac.uk/admin-services/ict/self-service/research-support/rcs/research-software-engineering/).

Each newly created app based on this template should include:

- Details of any pulication and archived data relating to the model, including DOIs
- A detailed specification of the programming environment used to reproduce results
- Instructions on how to use the app (allowed input format(s) and expected output(s))
- Unit tests for the underlying model (expected outputs for given inputs)
