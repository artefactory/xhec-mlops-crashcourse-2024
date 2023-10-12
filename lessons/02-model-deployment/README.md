# Model Deployment

## Intro

In this module we'll learn how to:

- Deploy a model
- Create a REST API that will serve our model predictions
- Dockerize the API

Machine learning models are complex objects that have many dependencies: specific feature transformations, a set of training data, hyperparameters, ... If all consumers had to deal with this complexity to be able to use these models, large organizations would not be able to extract value from them.

Model deployment is the process of making a machine learning (ML) model accessible to users. It involves creating an interface with which a user can interact with the model we developed. This interface separates the complexity of coding an ML solution from using it. It accepts requests from users and sends back responses computed using a model. In this way, there is a single team of data scientists that are responsible for maintaining these models and all stakeholders in an organization are capable to profit from their work.

More on the rationale of using APIs for Machine Learning [here](https://ubiops.com/the-benefits-of-machine-learning-apis/)

> There are three different types of deployment:
- **Batch (offline)** : recurrent jobs that get automatically executed
- **Web Service (online)** : a server that awaits requests from clients and send back responses
- **Streaming (online)** : a consumer that awaits events from producers and triggers workflows

In this module, we will create a `web service` that can predict the *trip duration* for the NYC Taxi given the *pickup location ID*, *the drop off location ID* and the *number of passengers*.

## 4.2 - Model Deployment

We will use the REST architecture we covered in the theoretical part of the course to build our web service. There are several options of frameworks that allow us to package our model into a web service:

- FastAPI
- Flask
- Django

For this module, we will use FastAPI, a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

## Introduction to FastAPI

If you have never used FastAPI before, please refer to the [tutorial](./fast_api_tutorial/fast_api_tutorial.md) to have an introduction to the framework.

## Model Deployment Lab

Imagine you work in a cab call center in New York. The manager of the call center wants to have a tool to allow the people making cab reservations to have an estimation of the trip duration to give a price estimation. The results will be used by a software engineer who will integrate them in the current platform.

This is a great example of when we would want to create an API for our ML model. The consumers of our model's results are not really worried about all the complexity of training a model: choosing the training set, fine-tuning models, ... All they want is to access the results of this model. Creating an API creates a standard interface that allow them to have what they need and only what they need.

### Goal of this Lab

We want to have a REST API running that can predict *trip duration* for the NYC Taxi given the *pickup location ID*, *the drop off location ID* and the *number of passengers*.

### Part 1

In this first part you will create a simple application that runs locally in your computer.It is a common practice to separate the code of your app from the machine learning code. In this repo, we use the `lib` folder to group the work we developed in the last sessions. All the code related to our application is under the `web_service` folder.

#### 1 - Copy the functions you developed in the last session into the `lib` folder.

> *In the previous lectures, you have packeged your code into two function: `train_model` and `predict`. In order to fulfill the Lab's objective, do you need both these functions?*

#### 2 - We will populate the `web_service/models.py` file with `pydantic` models that will serve as type hints for your app.

Starting by defining your inputs and outputs is often a good idea in app development, because it will guide the decisions you take in designing your sorftware.

* 2.1 - Create a `pydantic` model that specifies the input the user should give.

    >*Do you expect a single value or a list of values*

    >*What are the names of the input variables?*

    >*What are the types of the input variables? Are there any important constraints?*

* 2.1 - Create a `pydantic` model that specifies the output of your API.

    >*Do you expect a single value or a list of values*

    >*What are the names of the input variables?*

    >*What are the types of the input variables? Are there any important constraints?*

#### 3 - It is time to populate the `main.py` file with your app

* 3.1 - Create an `app` using `FastAPI` and a home page for your app.

    > *Think of specifying and displaying useful informatio, such as a title, a description, the app and model versions, etc.*

    > *N.B. It is a good practice to put the configuration of your app inside a config file. We have provided an example in `web_service/app_config.py`

* 3.2 - Create a `run_inference` function and add it to your app.

    > *Do you need to process the input? Or can you use it directly?*

    > *How can you access the model to make an inference?*


### Part 2

In the second part, you will go from a local deployment to a deployment in a Docker container. Every computer has a different set-up, with different software, operating system, and hardware installed. This is a problem, because we do not want our model to work only in one computer (imagine if it suddenly turns off).

Docker allows us to create a reproducible environemnt that can work in any computer that has Docker installed. We can use it to run our app in our local machine, on an on-premise server, or even in the cloud.

#### 4 - Create a requirements file specific for you application

Place your requirements file in `./requirements_app.txt`

> *Try to make this file as minimal as possible. Only list the packages that are absolutely necessary*

#### 5 - Build a Dockerfile that launches your app in the localhost

> *Which are the files that you need? Are you sure that they will be available for anyone who tries to launch the app?*

Reminder of useful Docker commands:

* `docker build -t <image-name:tag> -f <dockerfile-name> .` - Build a Docker image using the Dockerfile in the current directory. [Documentation](https://docs.docker.com/engine/reference/commandline/build/#tag)
* `docker run -p <host-port>:<container-port> <image-name:tag>` - Run a Docker container from an image, mapping the container's port to the host's port. [Documentation](https://docs.docker.com/engine/reference/commandline/run/)
* `docker ps` - List all running Docker containers.
* `docker ps -a` - List all Docker containers, both running and stopped.
* `docker images` - List all Docker images.
* `docker rm <container-id>` - Remove a Docker container.
* `docker rmi <image-id>` - Remove a Docker image.
* `docker stop <container-id>` - Stop a running Docker container.

Useful Dockerfile commands:

* `FROM` - Sets the base image for subsequent instructions. In other words, your Docker image is built on top of this base image.
* `COPY` - Copies new files or directories from <src> and adds them to the filesystem of the container at the path <dest>.
* `WORKDIR` - Sets the working directory for any subsequent `ADD`, `COPY`, `CMD`, `ENTRYPOINT`, `RUN` instructions that follow it in the Dockerfile.
* `RUN` - Executes any commands in a new layer on top of the current image and commit the results.
* `EXPOSE` - Informs Docker that the container listens on the specified network ports at runtime.
* `CMD` - Provides defaults for an executing container. These can include an executable, or they can omit the executable, in which case you must specify an `ENTRYPOINT` instruction.

> **N.B.** In order to launch your app, you will need to use the `0.0.0.0` host inside your app, otherwise your local computer will not be able to communicate with the app running inside the Docker container

### *[Optional] Part 3*

#### 5 - Include an option for the user to choose a specific model from your MlFlow `model registry`

> *You can use versions to control which model you choose*

> *You should deploy an MlFlow server and create a network that allows the app to communicate with it*
