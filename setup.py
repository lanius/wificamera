# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = f.read()

description = """WifiCamera is a Python module \
for controlling the network camera CS-W07G-CY."""

setup(
    name='wificamera',
    version='0.1',
    url='https://github.com/lanius/wificamera/',
    license='MIT',
    author='lanius',
    author_email='lanius@nirvake.org',
    description=description,
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Capture',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
