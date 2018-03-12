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

This app is configured with `heroku pg:psql`. 
To test locally,Ensure that [PostgreSQL](https://www.postgresql.org) is installed and running and configure the database URI located in `__init__.py`

Initilise the database:

`$ python flaskmigrations.py db init`

Migrate the database:

`$ python flaskmigrations.py db migrate`

Upgrade the database:

`$ python flaskmigrations.py db upgrade`

Run the app:

`$ python app.py`



