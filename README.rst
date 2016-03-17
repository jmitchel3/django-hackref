=====
Welcome to django-hackref!
=====

.. image:: https://badge.fury.io/py/django-hackref.svg
    :target: https://badge.fury.io/py/django-hackref

.. image:: https://travis-ci.org/jmitchel3/django-hackref.png
   :target: http://travis-ci.org/jmitchel3/django-hackref

.. image:: https://img.shields.io/pypi/v/django-hackref.svg
    :target: https://pypi.python.org/pypi/django-hackref

.. image:: https://coveralls.io/repos/github/jmitchel3/django-hackref/badge.svg?branch=master 
    :target: https://coveralls.io/github/jmitchel3/django-hackref?branch=master

Hack Referrals is a Django app to create, monitor and track user referral links.


Quick start
-----------

1. Install via "pip"::

    pip install django-hackref

2. Add "hackref" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hackref',
    ]

3. Include the polls URLconf in your project urls.py like this::

    url(r'^r/', include('hackref.urls')),

4. Run `python manage.py migrate`.

