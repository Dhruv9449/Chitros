# Chitros

Social media backend API built on FastAPI  
Try it here - https://chitros.dhruvshah.ml/docs

<br>

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Requirements](#requirements)
- [Setting-up and Installation](#setting-up-and-installation)
  - [Cloning repository](#cloning-repository)
  - [Configuring environment variables](#configuring-environment-variables)
  - [Using Docker](#using-docker)
    - [Running locally](#running-locally)
    - [Deploying in production](#deploying-in-production)
  - [Without using docker](#without-using-docker)
    - [Setting up a virtual environment](#setting-up-virtual-environment)
    - [Installing dependencies](#installing-dependencies)
    - [Migrating changes to the database](#migrating-changes-to-the-database)
    - [Running the server](#run-the-server)
- [Using the API](#using-the-api)
  - [Interactive documentation](#interactive-documentation)
  - [Thunder Client](#thunder-client)
  - [Frontend Integration](#frontend-integration)
- [License](#license)

<br>

## Features

Chitros has all the basic social media features such as -

- [x] Creating, modifying and deleting user profiles
- [x] Authentication using JWT access tokens
- [x] Creating, modifying and deleting posts
- [x] Following-Followers relationships
- [x] Sending and receiving follow requests
- [x] Likes, comments and replies
- [x] Viewing feed sorted by likes and date of upload
- [x] Pagination of feed

<br>

## Tech stack

**Web framework** - [FastAPI](https://fastapi.tiangolo.com/)  
**Database** - [PostgreSQL](https://www.postgresql.org/)  
**ORM** - [Sqlalchemy](https://www.sqlalchemy.org/)  
**Database migration tool** - [Alembic](https://alembic.sqlalchemy.org/)

<br>

## Requirements

[Python version 3.9](https://www.python.org/)  
[PostgreSQL version 14](https://www.postgresql.org/)

<br>
<br>

## Setting up and Installation

### Cloning Repository

Clone this repository by running in your terminal-

```sh
git clone git@github.com:Dhruv9449/Chitros.git
```

or

```sh
git clone https://github.com/Dhruv9449/Chitros.git
```

<br>
<br>

### Configuring Environment Variables

Configure your environment variables by creating a `.local`(if you want to run development server locally) and a `.production`(if you want to deploy in production) file as shown in `.example` in the `Chitros/.env/` directory for docker.  

For running it without docker, create a `local.env` file in the `Chitros/` directory.

#### Database variables
- `DATABASE_USERNAME` - Database username.
- `DATABASE_SERVER` - Database server name.
- `DATABASE_PASSWORD` - Database password.
- `DATABASE_HOSTNAME` - Database host name.
- `DATABASE_NAME` - Database name.
- `DATABASE_PORT` - Database port(Usually 5432).  


#### Postgres database variables(for docker)
- `POSTGRES_USER` - Postgres database username.
- `POSTGRES_PASSWORD` - Postgres database password.
- `POSTGRES_DB` - Postgres database name.
- `POSTGRES_HOST` - Postgres database host name.
- `POSTGRES_SERVER` - Postgres database server name.
- `POSTGRES_PORT` - Postgres database port(Usually 5432).


#### JWT authentication variables
- `SECRET_KEY` - Secret SSH key encoding your JWTs.
- `ALGORITHM` - Algorithm for encoding JWTs.
- `ACCESS_TOKEN_EXPIRE_MINUTES` - The time after which a JWT should expire.


#### CORS variables
- `CORS_ORIGIN_WHITELIST` - Whitelisted URLs from which the API can receive requests.

Use `.env.example` for reference.

<br>
<br>

## Using Docker

### Running locally

To run the server locally to view changes using hot reload, use the command - 

```sh
docker compose -f docker-compose-dev.yml up --build
```

This should start a local development server at `0.0.0.0:8000`

<br>
<br>

### Deploying in production

To deploy the server in production, use the following command - 

```sh
docker compose up --build
```

This should start production server, listening to requests at `0.0.0.0:80`

<br>
<br>

## Without using Docker

### Setting up Virtual Environment

Install `virtualenv` and set up a virtual environment in the working directory using the following commands -

```sh
pip install virtualenv
virtualenv venv
```

Now, activate the virtual environment -

#### Windows

```cmd
C:\Users\Username\Chitros> .\venv\Scripts\activate
```

#### Linux

```sh
user@hostname:~/Chitros$ source venv/bin/activate
```

Refer to the [official virtualenv documentation](https://virtualenv.pypa.io) for any further help.

<br>
<br>

### Installing dependencies

To install all the dependancies for this project run the following command in your terminal -

```sh
pip install -r requirements.txt
```

<br>
<br>


### Migrating changes to the database

Before running the server we need to migrate the changes made to the database using alembic. Run the following command -

```sh
alembic upgrade head
```

This should create the necessary changes to the database.

<br>
<br>

### Run the server!

We can start the ASGI uvicorn server with the following commands -

```sh
uvicorn app.main:app
```

**Note:** You need to be in the `Chitros/` directory while running this command.

<br>
<br>

## Using the API

- Data is received in the form of **Form Fields** for creation and updation.
- Responses are in form of **JSON**.

<br>

### Interactive documentation

You can try out the API using the interactive docs that are generated by Swagger UI. These can be accessed using the URL - `http://127.0.0.1:8000/docs` or `http://localhost/docs`

**Note**- You can also try out the API in the existing deployment at `https://chitros.dhruvshah.ml/docs`.

<br>
<br>

### Thunder Client

If you are using VS code then you can also try out the API using the [Thunder Client extension](https://www.thunderclient.com/).

- Install the extension and then you can import the **thunderclient environment** from `Chitros/thunderclient/thunder-environment_Chitros.json`.
- After this you can import the **thunderclient requests collection** from `Chitros/thunderclient/thunder-collection_Chitros.json`.

<br>
<br>

### Frontend Integration

If you want to use this API and build a frontend for it, you might want to use the sqlite3 database instead of postgres, to do that comment out the code under `# For postgres` and uncomment the code under `# For sqlite3` in `Chitros/app/db/db_setup.py` and `Chitros/app/db/models.py`.

You will also add the frontend URL in the `CORS_ORIGIN_WHITELIST` in the environment variables file.  
For example, for react you would set `CORS_ORIGIN_WHITELIST=http://localhost:3000, http://localhost:3001`.

<br>
<br>

## License

Copyright © 2022 Dhruv9449  
[MIT License](LICENSE)

<br>
<br>
<p align="center">
Developed with ❤️ by <a href="https://github.com/Dhruv9449" target=_blank>Dhruv Shah</a>
</p>
</p>
