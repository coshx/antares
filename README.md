# Antares
Explainable AI through decision trees.

## What is it?
Antares allows maintainters of AI systems to offer end-users explanations for classification and regression results.

# Setup
## API Setup with Pipenv

  1. Install [pipenv](https://pipenv.readthedocs.io/en/latest/install/).
  1. Run `pipenv install` from the project's root.
  1. Activate the virtualenv before developing using `pipenv shell`
  
##Secret Key setup
Copy the `config.ini.example` file and create a `config.ini` file. Fill in the secret keys either by generating your own or asking an admin for one.

## Setup Redis
Ensure you have a version of Redis installed on your computer. You can find a guide on how to install [here](https://redis.io/topics/quickstart). If you are on OSX we recommend using homebrew, a guide can be found [here](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298).

Once installed you can start your Redis server using this command `redis-server /usr/local/etc/redis.conf` and can ensure it is running via `redis-cli ping`. If you get the response `PONG` the server is running!

Finally, ensure the redis python client is pointing to the right server. If you haven't configured anything in a custom manner for the installation, the default configuration should be good. Otherwise you will have to change the port, and password field.

## Setup Web Server
Run `yarn` from the `webapp` directory and issue `yarn start` to start the development server at https://localhost:3000
# Tests
The API uses [pytest](https://docs.pytest.org/en/latest/) to run tests. From the project's root, run:

        pytest
        
# API Documentation
The API documentation can be found [here](https://docs.google.com/document/d/1CQLR_zFgXHEbdwGeiKLSJD_VmxccLGciM70mgwdi3rc/edit)

# Linting

## ESLint
To run ESLint use `node_modules/.bin/eslint . --ext .js`.
