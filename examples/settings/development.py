# -*- coding: utf-8 -*-


# 1) Collections are just like dictionaries, so you can just update them
DBSETTINGS.update(
    host='development.localhost',
)
# other possibility to do that would be:
# DBSETTINGS['host'] = 'development.localhost'


# 2) Using interpolation you can change only interesting part
AWS_S3_CONTENT_URL = '{AWS_S3_DOMAIN}/content-development'


# 3) email backend stays the same - dummy one


# 4) no changes for path to static files
