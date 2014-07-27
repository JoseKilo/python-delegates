#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='python-delegates',
    version='1.0.0',
    author='JoseKilo',
    author_email='jose.eduardo.gd@gmail.com',
    packages=['delegates'],
    include_package_data=True,
    url='https://github.com/JoseKilo',
    license='MIT',
    description='Delegates implementation for Python',
    classifiers=[
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
