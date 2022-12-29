# -*- coding: utf-8 -*-
import confy


# Some immaginary API settings
api_domain = "http://api.com"
API_ADD = '{api_domain}/add/'
API_DELETE = '{api_domain}/delete/'


# Some S3 places
s3_assets_domain = 'http://s3-eu-west-1.amazonaws.com'
CONTENTURL = '{s3_assets_domain}/project-assets/content/'
SITECONTENTURL = '{s3_assets_domain}/project-assets/sitecontent/'


FAKE_BACKEND_CLASS = confy.lazyimport('tests.fake.backend.FakeBackend')


DATABASE = {
    'ENGINE': confy.lazyimport('tests.fake.backend.FakeBackend'),
    'NAME': 'testdb',
    'USER': 'test',
    'PASSWORD': 'test',
    'HOST': 'test.db.com',
    'PORT': '9000',

    'testdata': {
        # this file does not exists, just cheking if this dict will changed into collection
        'fixtures': confy.rootpath('..', 'fixtures', 'testdata.json')
    },
}
