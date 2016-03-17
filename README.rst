=====
Django Hack Referrals hackref
=====

Hack Referrals is a Django app to monitor and track user referrals.


Quick start
-----------

1. Add "hackgrowth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hackgrowth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^r/', include('hackref.urls')),

3. Run `python manage.py migrate`.

