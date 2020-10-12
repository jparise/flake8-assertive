#!/usr/bin/env python

import re

from setuptools import setup


def get_version(filename):
    f = open(filename).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", f).group(1)


version = get_version('flake8_assertive.py')
description = open('README.rst').read() + "\n\n" + open('CHANGELOG.rst').read()
github_url = 'https://github.com/jparise/flake8-assertive'

setup(
    name='flake8-assertive',
    version=version,
    description='Flake8 unittest assert method checker',
    long_description=description,
    author='Jon Parise',
    author_email='jon@indelible.org',
    keywords='flake8 testing unittest assert',
    url=github_url,
    download_url=github_url + '/tarball/' + version,
    license='MIT',
    py_modules=['flake8_assertive'],
    entry_points={
        'flake8.extension': ['A50 = flake8_assertive:Checker'],
    },
    install_requires=['flake8'],
    tests_require=['flake8>=3.0.0'],
    test_suite='tests',
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',
    ],
)
