# Antares
Explainable AI through decision trees.

## What is it?
Antares allows maintainters of AI systems to offer end-users explanations for classification and regression results.

## Setup with Pipenv (Recommended)

  1. Install [pipenv](https://pipenv.readthedocs.io/en/latest/install/).
  1. Run `pipenv install` from the project's root.
  1. Activate the virtualenv before developing using `pipenv shell`

## Setup with Anaconda

Use [Anaconda](http://conda.pydata.org/docs/installation.html) to install project dependencies.

  1. Clone this repo.
  1. Install [Anaconda](http://conda.pydata.org/docs/installation.html). Or if you would like a lighter installation, follow the instructions to install [Miniconda](http://conda.pydata.org/docs/install/quick.html) instead.
  1. From the project root, run `conda env create -f environment.yml` to install the Python dependencies for the backend. This will create a `conda` environment called `antares`.
  1. Activate the `antares` environment using `source activate antares` on Linux/OS X or `activate antares` on Windows. You can deactivate the conda environment using `source deactivate` on Linux/OS X or `deactivate` on Windows.
  
 ## Setup Redis
 
 Ensure you have a version of Redis installed on your computer. You can find a guide on how to install [here](https://redis.io/topics/quickstart). If you are on OSX we recommend using homebrew, a guide can be found [here](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298).

Once installed you can start your Redis server using this command `redis-server /usr/local/etc/redis.conf` and can ensure it is running via `redis-cli ping`. If you get the response `PONG` the server is running!

Finally, ensure the redis python client is pointing to the right server. If you haven't configured anything in a custom manner for the installation, the default configuration should be good. Otherwise you will have to change the port, and password field.

## Running Tests
This project uses [pytest](https://docs.pytest.org/en/latest/) to run tests. From the project's root, run:

        pytest
