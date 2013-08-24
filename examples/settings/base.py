# -*- coding: utf-8 -*-

# In base you suppose to define all the settings which are common for
# all evironments. Later in other you'll override or update them.
# Below you see few examples of "confy" features.


# You can use simple dictionaries. Acctualy you can use whatever types
# you want
DBSETTINGS = dict(
    user='user',
    password='pass',
    host='localhost',
    port='9000',
)


# Interpolation example, take a look into development.py and production.py
AWS_S3_DOMAIN = 'http://s3-eu-west-1.amazonaws.com'
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content'


# Importing backend classes example
EMAIL_BACKEND = confy.lazyimport('sample_email_backend.DummyEmailBackend')


# Relative paths - with "confy" you can always define your paths
# relatively to your settings module
#
# SETTINGS_ROOT = confy.rootpath()               # /path/to/project/settings
# PROJECT_ROOT = confy.rootpath('..')            # /path/to/project
STATIC_FILES = confy.rootpath('..', 'static')    # /path/to/project/static
