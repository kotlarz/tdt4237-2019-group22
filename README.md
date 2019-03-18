# sec

## Get started
It's recommended to have a look at: https://www.djangoproject.com/start/

Basic tutorial that walks trough what the different files does.
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

Create a virtualenv https://docs.python-guide.org/dev/virtualenvs/


## Local setup

### Environment variables
The application requires the following environment variables to be set
* BEELANCE_SECRET_KEY
* BEELANCE_EMAIL_HOST
* BEELANCE_EMAIL_HOST_USER
* BEELANCE_EMAIL_HOST_PASSWORD
* BEELANCE_EMAIL_PORT
* BEELANCE_DEFAULT_ADMIN_PASSWORD

### Setup with Docker
Install Docker and Docker Compose if you haven't already done so.

Clone the project to your machine.

Run `docker-compose up` inside the main folder with environment variables set, example:

`BEELANCE_SECRET_KEY=my_secret_key BEELANCE_EMAIL_HOST=my_email_host BEELANCE_EMAIL_HOST_USER=my_email_host_user BEELANCE_EMAIL_HOST_PASSWORD=my_email_password BEELANCE_EMAIL_PORT=my_port BEELANCE_DEFAULT_ADMIN_PASSWORD=my_admin_password docker-compose up`


### Installation with examples for ubuntu. Windows and OSX is mostly the same

Fork the project and clone it to your machine.

#### Setup and activation of virtualenv (env that prevents python packages from being installed globaly on the machine)

`pip install virtualenv`

`virtualenv -p python3 env`

`source env/bin/activate`


#### Install python requirements

`pip install -r requirements.txt`


#### Migrate database

`python sec/manage.py migrate`


#### Create superuser

Create a local admin user by entering the following command:

`python sec/manage.py createsuperuser`

Only username and password is required


#### Start the app

Run `python sec/manage.py runserver` inside the main folder with environment variables set, example:

`BEELANCE_SECRET_KEY=my_secret_key BEELANCE_EMAIL_HOST=my_email_host BEELANCE_EMAIL_HOST_USER=my_email_host_user BEELANCE_EMAIL_HOST_PASSWORD=my_email_password BEELANCE_EMAIL_PORT=my_port BEELANCE_DEFAULT_ADMIN_PASSWORD=my_admin_password python sec/manage.py runserver`

#### Add initial data

Add initial data go to the url the app is running on localy after `runserver` and add `/admin` to the url.

Add some categories and you should be all set.

or by entering

`python sec/manage.py loaddata seed.json`
