[![Build Status](https://travis-ci.org/belatrix/BackendAllStars.svg?branch=master)](https://travis-ci.org/belatrix/BackendAllStars)
[![Coverage Status](https://coveralls.io/repos/github/belatrix/BackendAllStars/badge.svg)](https://coveralls.io/github/belatrix/BackendAllStars)
[![Code Health](https://landscape.io/github/belatrix/BackendAllStars/master/landscape.svg?style=flat)](https://landscape.io/github/belatrix/BackendAllStars/master)

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
