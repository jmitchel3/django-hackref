import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-hackref',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # MIT license
    description='A Django app to create, monitor and track user referral links',
    long_description=README,
    url='https://github.com/jmitchel3/django-hackref',
    author='Justin Mitchel',
    author_email='hello@teamcfe.com',
    install_requires=['Django >= 1.7',
                      'django-allauth >= 0.25.0'
                      ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # MIT license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django referrals growth marketing',
)