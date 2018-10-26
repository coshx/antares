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

## Running Tests
This project uses [pytest](https://docs.pytest.org/en/latest/) to run tests. From the project's root, run:

        pytest
