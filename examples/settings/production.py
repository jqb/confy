# -*- coding: utf-8 -*-

# This file will be loaded after "base.py" for production environment
# and it contains ALL the variables imports (or whatever) from
# "base.py" implicitly, which means you don't need to (and acctualy
# you shouldn't) import them here


# Update production db settings changes
DBSETTINGS.update(
    host='db.example.com',
    password='prod_pass',
)


# Production settings for storage
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content-production'


# Override email backend
EMAIL_BACKEND = confy.lazyimport('sample_email_backend.SendgridEmailBackend')
