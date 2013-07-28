# -*- coding: utf-8 -*-


# 1) Collection example
DBSETTINGS = dict(
    user='user',
    password='pass',
    host='localhost',
)


# 2) Interpolation example, take a look into development.py and production.py
AWS_S3_DOMAIN = 'http://s3-eu-west-1.amazonaws.com'
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content'


# 3) Importing backend classes example
EMAIL_BACKEND = confy.lazyimport('sample_email_backend.DummyEmailBackend')


# 4) relative paths
# with confy you can always define your paths relatively to your settings module
# SETTINGS_ROOT = confy.rootpath()               # /path/to/project/settings
# PROJECT_ROOT = confy.rootpath('..')            # /path/to/project
STATIC_FILES = confy.rootpath('..', 'static')    # /path/to/project/static
