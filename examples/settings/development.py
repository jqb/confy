# -*- coding: utf-8 -*-

# This file will be loaded after "base.py" and it contains ALL the
# variables imports or whatever from "base.py" implicitly, which means
# you don't need to (and acctualy you shouldn't) import them here


# To update dictionaries - use update method
DBSETTINGS.update(
    host='development.localhost',
)


# Using interpolation you can change only interesting part
# AWS_S3_DOMAIN and AWS_S3_CONTENT_URL were defined in base.py so we
# can override AWS_S3_CONTENT_URL to environment specific value
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content-development'


# EMAIL_BACKEND stays the same - dummy one would be the one what you
# expect from development environment :)


# STATIC_FILES does not need any changes, too
