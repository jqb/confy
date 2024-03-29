# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


import confy


setup(
    name='confy',
    version=confy.VERSION,
    description=(
        'Pragmatic and flexible configuration '
        'loader that makes your app settings clean.'
    ),
    author='Jakub Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='https://pypi.python.org/pypi/confy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(exclude=("tests*", "examples*")),
    include_package_data=True,
    zip_safe=False,
)

# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI
