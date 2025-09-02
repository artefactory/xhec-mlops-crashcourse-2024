# Best Practices Guide

## Intro

As we saw in the introduction to MLOps, enabling easy collaboration in a project is a hard task. Among other things we need to:

- Guarantee the reproducibility of the code in different environments
- Make it easy for all developers to read and understand code
- Detect mistakes and bugs that are hidden in the code

In this guide, we will cover some of the important steps to fix these problems.

## Code structure

The use of python scripts is almost always prefered to notebooks when we want to ensure the reproducibility and clarity of the code. Notebooks are a great tool to perform exploration and quickly test some aspects of the code. However, scripts allow for more modularity in development and allow a more ligthweight environment to be run.

Going from notebooks to scripts is, by itself, a simple task. However, it can also be the very first time that we are confronted with a project structure. The goal here is to present one of the many possible ways of structuring a project. Here is a quick overview of all the components that we usually employ during a project:

```
├── .github                       <- Where we set up interactions with GitHub such as actions and templates
├── .gitlab-ci.yml                <- Where we define a CI if we are using GitLab instead of GitHub
├── docs                          <- Project documentation, often generated automatically by tools like `Sphinx` or `mkdocs`
├── config                        <- Config variables stored in yaml, toml or py files
├── lib                           <- Main Package. This is where the code lives. Sometimes it is also called `src`
│   ├── main.py                   <- Entrypoint
│   ├── lib1                      <- Library functions 1
│   │   ├── {file1}.py            <- 1st library script
│   │   └── {file1}.py            <- 2nd library script
│   ├── lib2                      <- Library functions 2
│   └── utils                     <- Where utils scripts and functions live (shared across libs)
├── notebooks                     <- Where the jupyter notebooks are stored
├── tests                         <- Where the tests live
├── Dockerfile                    <- Project containerization
├── pyproject.toml                <- Package configuration also used to configure tools such as linters, etc
├── uv.lock                       <- Automatically generated lockfile for reproducible dependencies
├── Makefile                      <- Commands to ease up development cycle
└── README.md                     <- The top-level README for developers using this project
```

Every project has its own needs and might not require all of these files or might ask for new ones. Indeed, this very repository does not follow this exact structure to accomodate for the specificities of this lecture. However, increasing the standardization of the placement of these files is crucial to ensure that any developer can quickly read and understand your work in the future.

### Demo

- Check out the structure of this folder and navigate the files to see what is there and what is missing

## Python Environment and Dependency Management with uv

The first step in any reproducible project is establishing a clean, consistent, and fast development environment. Historically, the Python ecosystem has offered a fragmented set of tools for this purpose, each with its own trade-offs. To solve common development issues—such as cross-developer inconsistencies, missing production dependencies, and complex version conflicts—we are standardizing on uv, a next-generation toolchain for Python. This guide will explain what `uv` is, why it represents a fundamental leap forward for our workflows, and how to use it effectively in your day-to-day work.

### Motivations

Here are some common development issues:

- Many developers are involved in the same project, but work with different Python version. They might obtain different results while executing similar code
- Critical packages are installed on the development server, but are missing on the production server
- Conflicts in library versions among different projects

In order to avoid these embarrassing situations, the project configuration needs to be explicit so that results are reproducible (on a local or remote server, by any developer, ...).

> That's why any project must come with its virtual environment that is responsible for managing the Python version, as well as all the dependencies.

### What is uv? The New Standard for Python Tooling

uv represents a new generation of Python package managers, designed to address common pain points in the Python ecosystem such as slow installation times, dependency conflicts, and environment management complexity.

### Why uv is the Superior Choice for Our MLOps Workflow

`uv` offers several key advantages that make it ideal for our MLOps workflows:

- **Speed**: `uv` is written in Rust and is significantly faster than traditional Python package managers like `pip` and `conda`. This speed translates directly to faster build times for CI/CD pipelines and quicker local development iterations.
- **Simplicity**: `uv` streamlines common operations like adding dependencies and syncing environments, reducing the cognitive load on developers.
- **Integration**: It's designed to work seamlessly with `pyproject.toml`, aligning with modern Python packaging standards.

### Setting up a virtual environment

#### Creating and Managing Environments

##### Initializing a New Project:

The uv init command bootstraps a new project with a modern, standardized structure.

```bash
uv init my-ml-project
cd my-ml-project
```

This command creates a pyproject.toml for configuration, a .python-version file to pin the Python version, a README.md, and a .gitignore.

uv makes environment creation explicit and simple. By default, it creates a .venv directory in the project root.

### Handle dependencies

In your base environment, there should not be any Python packages. This isolates the dependencies of any project, avoiding future compatibility problems. Therefore, you must always install dependencies from within your virtual environment.

The `pyproject.toml` file serves as the single source of truth for your project's direct dependencies.

#### Adding a Dependency:

Use uv add. This command automatically resolves the latest compatible version, adds the dependency to pyproject.toml, and updates the uv.lock file in a single, atomic operation.

```bash
uv add "pandas>=2.0" scikit-learn
```

#### Installing from Lockfile (The Main Workflow):

uv sync is the command that will be used most frequently. It synchronizes the virtual environment to match the exact state defined in uv.lock, adding, removing, or updating packages as needed.

```bash
uv sync
```

### Demo

- Let's create a new environment to run our hello world project using `uv` script. Make sure you are at `best-practices` and run:

```bash
uv sync
```

then

```bash
source .venv/bin/activate
```

## Locally check your code

You now have a functioning local environment where you can develop python code. Still, it is common for us to make silly mistakes while coding. Over time, these mistakes can compound and add up to a large unexpected failure or just a general decline in code quality. We can employ simple and effective tools to help us overcome these small mistakes when developing.

### Linting

_Linters_ perform a _static_ evaluation of the code to look for bugs and errors. They are useful as they help in identifying potential issues in the code before it is run. As they perform static evaluation, they cannot catch any RunTime errors. However, a linter can check for syntax errors, type mismatches, and code smells. The most used linters in Python include:

- [Pylint](https://pypi.org/project/pylint/)
- [Pyflakes](https://pypi.org/project/pyflakes/)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Ruff](https://github.com/astral-sh/ruff)

Each linter has its own way of functioning and caveats, so choosing which one might be a matter of just sticking to what your pairs already use or looking for a specific feature. In this repo, we use `flake8` whose configuration can be found in `./.flake8`

### Demo

- Go to `best-practices` folder and lint the `best-practices` folder using flake8

```bash
flake8 .
```

### Automatic Formatting

Good formatting is essential to ensure that your code is readable and comprehensible. However, it is probably the area of coding in which it is the easiest to make a mistake. That is why we generally use tools that format the code automatically, ensuring that we are always PEP compliant. The most used tool for this end is [Black](https://github.com/psf/black). We also often use a tool to organize imports in a logical manner called [isort](https://pycqa.github.io/isort/). The configuration for both tools can be found in the `./pyproject.toml` file.

There are other commonly used tools like [nbstripout](https://github.com/kynan/nbstripout) and [bandit](https://bandit.readthedocs.io/en/latest/) that provide different functionalities, but that have not been used in this project.

### Demo

- Run `isort` to format the imports

```bash
isort .
```

- Run `black` to format the code

```bash
black .
```

### Pre-commit Hooks

Git provides a useful tool to help putting these technique into practice. Pre-commit hooks allow you to perform these code checks every time you make a commit. The `pre-commit` packages helps to use this tool, by creating a customizable config file for the pre-commits. You can find it [here](./.pre-commit-config.yaml).

Before using the pre-commits, you must install them, by running in your terminal:

```bash
pre-commit install -t pre-commit
```

### Demo

- Create a commit with the changes and see that all check pass

## Git

Working with a clean and legible git history is key to rendering your commit history usable. The whole point of using `git` is to keep track of the changes in code and collaborate better. Achieving that requires establishing rules that go beyond the simple practices we keep when working alone.

- If you want to learn more about the branching strategies most commonly used today: [what are the Best Git Branching Strategies](https://www.abtasty.com/blog/git-branching-strategies/) goes through the most commonly used branching strategies
- More details on the Gitflow framework: [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- Standardized way of writing commit messages: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- If you want to master more advanced git functionalities: [Learning Git Branching](https://learngitbranching.js.org/)

## Continuous Integration

## Continuous Integration (CI)

Continuous Integration (CI) is a software development practice that involves frequently integrating code changes made by multiple developers into a shared repository. The main goal of CI is to streamline and automate the process of integrating code, running tests, and identifying and fixing bugs early in the development cycle. CI ensures that all changes are tested and incorporated into the main codebase in a consistent and reliable manner. It helps in maintaining code quality, reducing integration issues, and enhancing collaboration among team members. By automating the integration process, CI also enables faster feedback loops, making it easier to catch and resolve issues promptly, leading to improved software stability and quicker delivery of new features. Overall, CI is essential for achieving efficient, robust, and reliable software development.

Common checks performed by a Continuous Integration (CI) system include:

- **Code compilation:** This is the first step in many CI pipelines. The code is compiled to check for any syntax errors.
- **Unit testing:** These are the tests written by developers to check the functionality of a small piece of code or a "unit". The CI system runs these tests to ensure that the new changes have not broken any existing functionality.
- **Integration testing:** These tests check the interaction between different units of code. They are run to ensure that the units of code work correctly when integrated.
- **Static code analysis:** This involves checking the code for potential errors, bugs, or deviations from coding standards without executing the program.
- **Security testing:** This involves checking the code for potential security vulnerabilities, like secrets leaking

### CICD and Github Actions

Continuous Integration (CI), Continuous Delivery (CD), and GitHub Actions are all practices and tools used in modern software development to automate the process of integrating code changes, testing, and deployment.

CD is a step further than CI and involves the automated delivery of the integrated code to the production environment. It ensures that the software can be released at any time. While CI deals with the build and test stages of the development cycle, CD covers the deployment stages.

[GitHub Actions](https://docs.github.com/en/actions) is a CI/CD tool provided by GitHub. It allows you to automate, customize, and execute your software development workflows right in your GitHub repository. You can write individual tasks, called actions, and combine them to create a custom workflow. Workflows are custom automated processes that you can set up in your repository to build, test, package, release, or deploy any code project on GitHub.

We included an example CI workflow in the [./.github/workflows/ci.yaml](./.github/workflows/ci.yaml) file. It does:

- Copy the current repo into the GitHub Action
- Set up python
- Install requirements: ensures there are no conflicts in the requirements
- Run pre-commit hooks: ensures developer installed pre-commit hooks and thus linted and formatted the code
