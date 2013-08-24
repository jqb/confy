# -*- coding: utf-8 -*-
import os
from pprint import pprint


# MAKE SURE TO READ "confy" from this repo ###############
import sys

def here(*path):
    absolute_here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(absolute_here, *path))

sys.path.insert(0, here('..'))
###########################################################


# Change 'development' into 'production' and
# take a look how output changes
os.environ.setdefault('CONFIGURATION_MODE', 'development')


###########################################################
from settings import config

# Take a look into settings/__init__.py and change "confy.merge" into
# "confy.define_module" to be able simply import settings like this:
#
# import settings


pprint(config.DBSETTINGS)
pprint(dict(config.DBSETTINGS))
pprint(config.AWS_S3_CONTENT_URL)
pprint(config.EMAIL_BACKEND)
pprint(config.STATIC_FILES)
