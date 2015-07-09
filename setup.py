#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements
import platform

NAME = "screen-events"
VERSION = "0.1.0"

install_reqs = []

if platform.system() == 'Darwin':
    reqs = parse_requirements("requirements-mac.txt")

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=[str(ir.req) for ir in install_reqs],
)
