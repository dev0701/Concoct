# CS348-project
## Steps to set up project:

### Create a new environment:

Open a terminal

Check python version-

`python -V` (version should be 3.X)

Create and cd into directory for the project:

`mkdir <project-folder-name> && cd <project-folder-name>`

Create and activate virtual environment:

`python3 -m venv env`

`source env\bin\activate`

Install flask package:

`pip install flask`

`pip install flask-mysql`

Create api directory:

`mkdir api && cd api`

Add files from github repo to the api directory:
`main.py`
`requirements.txt`
`createtables.sql`
`static` folder
`templates` folder


### Install MySQL on local machine: 

Follow instructions on: https://dev.mysql.com/doc/refman/8.0/en/macos-installation-pkg.html

Set password to "Zer0cool"

In a new terminal, cd into the project directory

Activate virtual environemnt:

`source env\bin\activate`

cd into api:

`cd api`

Run the following commands to create an alias for starting MySQL

`alias mysql=/usr/local/mysql/bin/mysql`
`alias mysqladmin=/usr/local/mysql/bin/mysqladmin`

Log into MySQL with the command:

`mysql -u root -p`

enter password "Zer0cool"

Once logged in, create and use the database: 

`CREATE DATABASE Concoct;`

`use Concoct;`

Use `createtables.sql` to create the tables:

`source createtables.sql;`

Verify the tables exist:

`show tables;`

### Run the app: 

In terminal #1 run the command:

`python3 main.py`

Use a browser to access the localhost link to access the web app.
