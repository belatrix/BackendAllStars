[![Build Status](https://travis-ci.org/belatrix/BackendAllStars.svg?branch=master)](https://travis-ci.org/belatrix/BackendAllStars)
[![Coverage Status](https://coveralls.io/repos/github/belatrix/BackendAllStars/badge.svg)](https://coveralls.io/github/belatrix/BackendAllStars)
[![Code Health](https://landscape.io/github/belatrix/BackendAllStars/master/landscape.svg?style=flat)](https://landscape.io/github/belatrix/BackendAllStars/master)
[![Documentation Status](https://readthedocs.org/projects/belatrix-connect-backend/badge/?version=latest)](http://belatrix-connect-backend.readthedocs.io/en/latest/?badge=latest)

# Belatrix Connect

Belatrix Connect is a social platform, it uses gamification techniques to engage people with their coworkers and with social events in order to generate a great working environment.

## Why opensource?

We truly believe in open source software, this is the first project that we want to share with the developers' community.

## Installation and Usage

We strongly recommend to use virtualenvwrapper, please review the documentation before to start: [**virtualenvwrapper**](http://virtualenvwrapper.readthedocs.io/en/latest/index.html)

### Steps:

1. Create and setup your **virtual environment**

2. **Clone** this repository:
```
git clone https://github.com/belatrix/BackendAllStars.git .
```
3. Use **pip and local.txt** as a requirements file:
```
pip install -r requirements/local.txt
```
4. Add this line into your **postactivate** script
```
export DJANGO_SETTINGS_MODULE=AllStars.settings.local
```
5. **Restart** your virtual environment

6. Make migrations, migrate, load default data and set default avatar for **tests users**
```
python manage.py makemigrations && python manage.py migrate && python loaddata sample_data/*.json && python manage.py setdefaultavatar
```
7. Create a **new super user**
```
python manage.py createsuperuser
```
8. **Run** your local server
```
python manage.py runserver
```
9. Login into admin portal and then you can use api documentation to test existing endpoints

**Admin site**: [http://127.0.0.1:8000/admin/]( http://127.0.0.1:8000/) 

**API documentation**: [ http://127.0.0.1:8000/api/docs/]( http://127.0.0.1:8000/api/docs)

10. **Have fun!** :D

## Credits

Belatrix Connect is owned and maintained by [Belatrix Software](http://belatrixsf.com).

### Security disclosure
If you believe you have identified a security vulnerability, you should report it as soon as possible via email to [mobilelab@belatrixsf.com](mailto:mobilelab@belatrixsf.com). Please do not post it to a public issue tracker. 

## Wiki

[http://belatrix-connect-backend.readthedocs.io/en/latest/](http://belatrix-connect-backend.readthedocs.io/en/latest/)

## Contribuiting

Development of Belatrix Connect happens at Github: http://github.com/belatrix/BackendAllStars

You are highly encouraged to participate in the development. If you don't like Github (for some reason) you're welcome to send regular patches.

## License

Belatrix Connect is released under the Apache License 2.0. [See LICENSE](https://github.com/belatrix/BackendAllStars/blob/master/LICENSE) for details.
