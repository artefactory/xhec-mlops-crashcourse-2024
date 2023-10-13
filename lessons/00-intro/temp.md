# Code structure

Going from notebooks to scripts is, by itself, a simple task. However, it can also be the very first time that we are confronted with a project structure. The goal here is to present one of the many possible ways of structuring a project. Here is a quick overview of all the components that we usually employ during a project:

```
├── .github                      <- Where we set up interactions with GitHub such as actions and templates
├── docs                         <- Project documentation, often generated automatically by tools like `Sphinx`
├── config                       <- Config variables
│   ├── env                      <- Environment specific
│   │   ├── dev.yml
│   │   ├── debug.yml
│   │   └── prod.yml
│   └── constants.py              <- Constants used in python scripts that are environment agnostic
├── bin                           <- Executable scripts
├── lib                           <- Main Package. This is where the code lives. Sometimes it is also called `src`
│   ├── main.py                   <- Entrypoint
│   ├── lib1                      <- Library functions 1
│   │   ├── {file1}.py            <- 1st library script
│   │   └── {file1}.py            <- 2nd library script
│   ├── lib2                      <- Library functions 2
│   └── utils                     <- Where utils scripts and functions live (shared across libs)
├── notebooks                     <- Where the jupyter notebooks are stored
├── tests                         <- Where the tests live
│   ├── unit_tests
│   └── integration_tests
├── Dockerfile                    <- Project containerization
├── requirements.in               <- Python packages used by project
├── requirements.txt              <- Automatically generated requirements (adding all nested dependencies from requirements.in)
├── environment.yml               <- conda environment file (specifying virtual env name, python version and python packages)
├── .flake8                       <- linter config
├── .gitignore                    <- files not to be tracked
├── pytest.ini                    <- pytest config
├── pyproject.toml                <- package configuration
├── CONTRIBUTING.md               <- Contribution guidelines
├── Makefile                      <- commands to ease up development cycle
└── README.md                     <- The top-level README for developers using this project
```

Every project has its own needs and might not require all of these files or might ask for other ones. Indeed, this very repository does not follow this exact structure to accomodate for the specificities of this lecture. However, increasing the standardization of the placement of these files is crucial to ensure that any developer can quickly read and understand your work in the future.

# Python virtual environments

Once your project is set up, it is time to ensure that you have the proper environment to run your code.

## Motivations

Here are some common development issues:

- Many developers are involved in the same project, but work with different Python version. They might obtain different results while executing similar code
- Critical packages are installed on the development server, but are missing on the production server
- Conflicts in library versions among different projects

In order to avoid these embarrassing situations, the project configuration needs to be explicit so that results are reproducible (on a local or remote server, by any developer, ...).

> That's why any project must come with its virtual environment that is responsible for managing the Python version, as well as all the dependencies.

A virtual environment is always summarized in a requirements.txt (pip-fashion) or a environment.yml (conda-fashion) file, located at the root of the project. It takes the following form:

- For `requirements.txt`

```
pandas==1.1.0
```

- For `environment.yml`

```
name: envname
channels:
  - conda-forge
dependencies:
  - pandas=1.1.0
```

## Setting up a virtual environment

We will present 2 options: using `virtualenv` or `conda`

### Virtualenv

```
# Install virtualenv package
$ pip install virtualenv

# Create the virtual environment
$ virtualenv venv --python=python3.x

# Activate it
$ source venv/Scripts/activate  # Windows
$ source venv/bin/activate  # Unix
```

### Conda

If you have a Miniconda installed:

```
# Create env
$ cd <this repository>
$ conda env create --file environment.yml

# Activate your environment:
$ conda activate envname

# Check python:
(envname) $ which python # Unix
(envname) $ where python # Windows

# In order to stop using this virtual environment:
(envname) $ deactivate
```

Once activated, the command line starts with (`envname`) to let you know which environment you're in. The environment must always be activated while working in the project.

## Handle dependencies

In your base environment, there should not be any Python packages. This isolates the dependencies of any project, avoiding future compatibility problems. Therefore, you must always install dependencies from within your virtual environment.

### Virtualenv

```
$ source venv/bin/activate  # Activate env
(venv) $ pip install -r requirements.txt
```

If you need to amend the dependencies of the project, then simply run:

```
(venv) $ pip install mypackage
# You can have an exhaustive view of your environment:
(venv) $ pip list | grep pandas
pandas (1.1.0)
```

You should not forget to add this new dependence to `requirements.txt`. Our recommended way is to have a `requirements.in`:

- Just add a line in the file, specifying the version (example: `pandas==1.0.1`)
- Overwrite `requirements.txt` file by re-generating it:

```
(venv) $ pip-compile requirements.in
```

This will automatically parse all your nested dependencies into `requirements.txt` thus ensuring full reproducibility. The only caveats are that it requires an additional package, `pip-tools` and that it takes some time to compile long and complex requirements.

### Conda

If the name is correctly specified in the `environment.yml` file, then there is no need to run the following command from within the virtual environment:

```
conda env update --file environment.yml --prune
```

If you need to amend the dependencies of the project, then simply run:

```
$ conda activate envname  # Activate env
(envname) $ conda install -c conda-forge jupyter
(envname) $ conda list | grep python
python                    3.8.8           h4e93d89_0_cpython    conda-forge
```

You should not forget to add this new dependence to `environment.yml`. To get the best of both words, our recommended way is:

- All requirements need to be exported in a `requirements.txt` as explained in the `virtualenv` section above
- Use `environment.yml` to specify your environement name, your python and pip version and get packages dependencies directly from `requirements.txt`

```
dependencies: # Versions should be taken care of
  - python=3.7
  - pip=21.0.1
  - pip:
    - -r requirements.txt
```

## Conda VS Pip

*TL;DR*: use conda.

These two resources are worth reading:

- Stack Overflow: [What is the difference between Pip and Conda](https://stackoverflow.com/questions/20994716/what-is-the-difference-between-pip-and-conda)
- Anaconda blog: [Understanding the difference between Conda and Pip](https://www.anaconda.com/blog/understanding-conda-and-pip)

# Locally check your code

You now have a functioning local environment where you can develop python code. Still, it is common for us to make silly mistakes while coding. Over time, these mistakes can compound and add up to a large unexpected failure or just a general decline in code quality. We can employ simple and effective tools to help us overcome these small mistakes when developing.

## Linting

*Linters* perform a *static* evaluation of the code to look for bugs and errors. They are useful as they help in identifying potential issues in the code before it is run. As they perform static evaluation, they cannot catch any RunTime errors. However, a linter can check for syntax errors, type mismatches, and code smells. The most used linters in Python include:

- [Pylint](https://pypi.org/project/pylint/)
- [Pyflakes](https://pypi.org/project/pyflakes/)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Ruff](https://github.com/astral-sh/ruff)

Each linter has its own way of functioning and caveats, so choosing which one might be a matter of just sticking to what your pairs already use or looking for a specific feature. In this repo, we use `flake8` whose configuration can be found in `./.flake8`

## Automatic Formatting

Good formatting is essetial to ensure that your code is readable and comprehensible. However, it is probably the area of coding in which it is the easiest to make a mistake. That is why we generally use tools that format the code automatically, ensuring that we are always PEP compliant. The most used tool for this end is [Black](https://github.com/psf/black). We also often use a tool to organize imports in a logical manner called [isort](https://pycqa.github.io/isort/). The configuration for both tools can be found in the `./pyproject.toml` file.

## Automatic Docstrings (?)

TODO

# Git Flow

TODO

# Continuous Integration

TODO
