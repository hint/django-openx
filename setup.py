# -*- coding: utf-8 -*-
'''
Setup file for the django_openx module using distutils.
'''

# verify that setuptools are installed
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
setup(
	name='django_openx',
	version='0.1pre',
	packages = ['django_openx'],
	description='A simple python wrapper to the webservices of the openx adserver.',
	author='David Danier',
	author_email='',
	url='http://code.google.com/p/django-openx/',
	include_package_data=True,
	exclude_package_data={
		'': ['README.txt',],
	},
)
