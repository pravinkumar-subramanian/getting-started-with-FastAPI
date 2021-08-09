# Getting Started with FastAPI

This project is bootstrapped with [FastAPI](https://fastapi.tiangolo.com/).

## Overview of this project

When you are done with running the FastAPI, you will see user and security module in the API list.

1. User APIs will allow you to **CRUD (create, read, update and delete)** user details.
2. Security APIs will fetch data from the table **security** which will have details of user logins. These APIs are created for you to know how to maintain separate modules for each function. You can try replicating the same for other functions (like creating CRUD for data table and maintaining separate model, schema and crud).

I am using PostgreSQL database for storing all the data. So all the parameters are defined for PostgreSQL in this project. But all the SQL databases should follow the same steps mentioned below.

## Follow the below steps to use FastAPI

### Step 1: Create .env file

> Note: .env file should have all the below parameters

DEFAULT_DATABASE_URI=postgresql://<username>:<password>@<localhost or ip>:<port>/postgres?sslmode=prefer
DATABASE_URI=postgresql://<username>:<password>@<localhost or ip>:<port>/  
DATABASE_NAME=<database_name>  
SCHEMA_NAME=<schema name>
PROJECT=<project name>
DESCRIPTION=This is the backend server for your application
ROOT_USER=<rootuser@gmail.com>  
ROOT_USER_PASSWORD=<password>
ENCRYPTION=HS256  
TOKEN_EXPIRY=60  
TOKEN_SECRET=<random15text>

### Step2: Run below scripts one by one

In the project directory, you can run:

## `python -m venv env`

create a virtual environment
go to VS Code: File -> Preferences -> Settings -> Extensions -> Scroll down and find "Edit in settings.json".

For VS code version < 1.56, add

> "terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]

For VS code version >= 1.56, add

> "terminal.integrated.profiles.windows": {  
>  "PowerShell": {  
>  "source": "PowerShell",  
>  "icon": "terminal-powershell",  
>  "args": ["-ExecutionPolicy", "Bypass"]  
>  }  
> },  
> "terminal.integrated.defaultProfile.windows": "PowerShell"

## `env\Scripts\activate`

Starts the virtual environment to maintain package **versions** during pip install

## `pip install -r requirements.txt`

This will install all the dependencies mentioned in the requirements.txt file.

> Make sue the Microsoft Visual C++ version is greater than 14.0.
> To install latest version of Microsoft Visual C++, download and open [Build Tools installer](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Under **Workload**, select and install **C++ build tools**

## `uvicorn main:app --reload`

This will start the uvicorn server with **main.py** file as root file and **--reload** automatically reloads when there is a change in files.
After running this command, you can find the database and schemas created in the database server.

### Step3: Insert the rootuser into the Users table

Open [SwaggerUI](http://localhost:8000/api/docs/), expand **default** tag APIs and execute **/api/rootuser** to create the root user. Now click the **Authorize** button and use the credentials defined in .env file to use protected APIs.

```diff
You are good to go!!!
```

## General commands used during devlopment from scratch

### `pip install fastapi[all]`

installs all the below dependencies
'''
MarkupSafe-1.1.1 aiofiles-0.5.0 aniso8601-7.0.0
async-exit-stack-1.0.1 async-generator-1.10 certifi-2020.12.5
chardet-4.0.0 click-7.1.2 colorama-0.4.4
dnspython-2.1.0 email-validator-1.1.2 fastapi-0.63.0
graphene-2.1.8 graphql-core-2.3.2 graphql-relay-2.0.1
h11-0.12.0 idna-3.1 itsdangerous-1.1.0 jinja2-2.11.2
orjson-3.4.6 promise-2.3 pydantic-1.7.3
python-dotenv-0.15.0 python-multipart-0.0.5 pyyaml-5.3.1
requests-2.25.1 rx-1.6.1 six-1.15.0 starlette-0.13.6
typing-extensions-3.7.4.3 ujson-3.2.0 urllib3-1.26.2
uvicorn-0.13.3 watchgod-0.6 websockets-8.1
'''

### `pip install gunicorn databases[postgresql] psycopg2`

installs all the below dependencies
'''
asyncpg-0.21.0
databases-0.4.1
gunicorn-20.0.4
sqlalchemy-1.3.22
'''

1. asyncpg is a database interface library designed specifically for PostgreSQL and Python/asyncio.
   asyncpg is an efficient, clean implementation of PostgreSQL server binary protocol for use with Python’s asyncio framework.
2. Green Unicorn’ is a Python WSGI (Web Server Gateway Interface) HTTP Server for UNIX
3. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns,
   designed for efficient and high-performing database access,
   adapted into a simple and Pythonic domain language.
4. psycopg2 executes SQL queries, whereas SQLAlchemy creates query and executes it. SQLAlchemy needs libraries like psycopg2

### `pip install PyJWT passlib`

visit [JWT Token creation](https://jwt.io/) for more details

### `pip install pandas`

installs all the below dependencies

1. python-dateutil
2. numpy
3. pandas
