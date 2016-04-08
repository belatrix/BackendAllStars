# Project: Belatrix AllStars

This is part of Belatrix Gamification project. It is a proposal for backend using Django.

## Local environments with SQLite3

+ Use local.txt as a requirements file with pip
```
pip install -r requirements/local.txt
```
+ Set this line into postactivate script with virtualenvwrapper
```
export DJANGO_SETTINGS_MODULE=AllStars.settings.local
```