# Photy
[![Build Status](https://travis-ci.org/andela-amwaleh/Photy.svg?branch=feature%2Ftest)](https://travis-ci.org/andela-amwaleh/Photy)
[![Coverage Status](https://coveralls.io/repos/github/andela-amwaleh/Photy/badge.svg?branch=feature%2Ftest)](https://coveralls.io/github/andela-amwaleh/Photy?branch=feature%2Ftest)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/0a633c70e8c044ef914a7cbaaf743120/badge.svg)](https://www.quantifiedcode.com/app/project/0a633c70e8c044ef914a7cbaaf743120)

A simple image processing tool that uses  [PIL / Pillow](https://pypi.python.org/pypi/Pillow).

### Overview
Photy lets you upload photos , apply filters save or share with friends via social media. Photy  organises and stores your photos online.

### Requirements
Photy is built using the following libraries and Frameworks:

* [Django ](https://www.djangoproject.com/) - Django(1.9) makes it easier to build better Web apps more quickly and with less code.
* [PIL / Pillow](https://pypi.python.org/pypi/Pillow) - Python Image library
* [Flat ui](https://github.com/designmodo/Flat-UI) - Flat UI is based on Bootstrap.
* [Postgress](http://www.postgresql.org/) -  powerful, open source object-relational database system.
* [Jquery/Ajax](https://jquery.com/) -  JavaScript Library.
* [Pillow](https://github.com/python-pillow/Pillow/) - Pillow is the friendly PIL fork by Alex Clark and Contributors.
* [Dropzone](https://github.com/enyo/dropzone) - a light weight JavaScript library that turns an HTML element into a dropzone.

#### Requirements
To install and run this application you need to have python installed on your system


### Installation
To install the build locally 
```
$ git clone https://github.com/andela-amwaleh/Photy.git
$ cd photy
$ pip install -r requirements.txt
```

### Run your build
```
$ python django-photo-application/manage.py runserver 
```

### Running the test
To run your test
```
$ python manage.py test
```
### Coverage
```
$ coverage run manage.py test

