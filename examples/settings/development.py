# -*- coding: utf-8 -*-

# 1) Collections are just like dictionaries, so you can just update them
DBSETTINGS.update(
    host='development.localhost',
)
# other possibilities to do that would be:
# DBSETTINGS.host = 'development.localhost'
# DBSETTINGS['host'] = 'development.localhost'


# 2) Using interpolation you can change only interesting part
AWS_S3_CONTENT_URL = '{AWS_S3_CONTENT_URL}/content-development'
