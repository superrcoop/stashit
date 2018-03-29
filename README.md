<img src="app/static/icons/LOGOICON.png" /> 

Description
-------------------

Safely secure henyting in your online Journal.

Getting Started !
-------------------

This Web app requires the latest version of [Python and Flask](http://flask.pocoo.org)

Clone the repository:

`$ git clone https://github.com/superrcoop/stashit.git`

Go into the repository:

`$ cd stashit`

Install dependencies:

`$ pip install -r requirements.txt`


Deploy
--------

This app is configured with `heroku pg:psql`. 
To test locally,Ensure that [PostgreSQL](https://www.postgresql.org) is installed and running and configure the database URI located in `__init__.py`

Locally: 

~~~~python
app.config['SQLALCHEMY_DATABASE_URI'] =  '<database_url>'
~~~~

Run:

`$ python run.py`

Heroku:

Now we'll face some problem regarding migrating. What we'll do is below in order to bypass the problems.

~~~~
$ heroku run python
>> import os
>> os.environ.get('DATABASE_URL')
'<DATABASE_URL>'
~~~~

`$ export DATABASE_URL=<DATABASE_URL>`

~~~~python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ('DATABASE_URL')
~~~~

Setup database: 

~~~
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
~~~

Run Heroku app: 

`$ heroku open`

View database from heroku-cli:

~~~
$ heroku pg:psql

<heroku-app>::DATABASE=>\c
You are now connected to database "<heroku_database>" as user "<heroku_database_user>"

<heroku-app>::DATABASE=>\dt
                  List of relations
 Schema |      Name       |   Type   |     Owner      
--------+-----------------+----------+----------------
 public | alembic_version | table    | <owner_name>
 public | userstable      | table    | <owner_name>
(2 rows)
~~~

