# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


import confy


setup(
    name='confy',
    version=confy.VERSION,
    description='',
    author='Jakub Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='https://github.com/jqb/confy/tree/ver-%s' % confy.VERSION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(exclude=("tests*",)),
    include_package_data = True,
    zip_safe=False,
    install_requires = [
        'six==1.3.0',
    ],
)

# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI
