# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

description = ("WifiCamera is a Python module ",
               "for controlling the network camera CS-W07G-CY.")

setup(
    name='wificamera',
    version='0.1.0',
    packages=find_packages(),
    description=description,
    author='lanius',
    author_email='lanius@nirvake.org',
    license="MIT License",
)
