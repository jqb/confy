# -*- coding: utf-8 -*-
import os
import confy


# Define loader. It should be awere of possition in file system to
# make "confy.rootpath" feature work properly
confy = confy.loader(__file__)


# All the settings defined inside 'base', 'development' (or other file
# which name might be defined under 'CONFIGURATION_MODE' environ
# variable in this case), and 'local' modules will be merged together
# (if 'local' doesn't exists "confy" won't complain about it becase of
# "silent" param)
config = confy.merge(
    confy.from_modules('base', os.environ.get('CONFIGURATION_MODE', 'development')),
    confy.from_modules('local', silent=True),
)


# If you wish to have all the variables defined on the module level,
# you can simply type:
#
# confy.define_module(__name__, [
#     confy.from_modules('base', os.environ.get('CONFIGURATION_MODE', 'development')),
#     confy.from_modules('local', silent=True),
# ])
#
# this doing exactly what "confy.merge" does plus it defines module in
# "sys.modules" for you
