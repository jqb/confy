# -*- coding: utf-8 -*-

# 1) db settings changes
DBSETTINGS['host'] = 'db.example.com'


# 2) Production settings for storage
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content-production'


# 3) Override email backend
EMAIL_BACKEND = confy.lazyimport('sample_email_backend.SendgridEmailBackend')
