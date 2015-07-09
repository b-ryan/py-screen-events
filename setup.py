#!/usr/bin/env python
from setuptools import setup
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
    description="Monitor computer screen for lock / awake events",
    author="Buck Ryan",
    author_email="buck.ryan@gmail.com",
    url="https://github.com/b-ryan/py-screen-events",
    py_modules=["screen_events"],
    install_requires=[str(ir.req) for ir in install_reqs],
)
