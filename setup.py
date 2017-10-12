#!/usr/bin/env python

import setuptools
import pathlib

name = "find_size"
version = "0.1"
release = "0.1.0"
here = pathlib.Path(__file__).parent.resolve()

setuptools.setup(
    name=name,
    version=version,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'find_size = find_size.find_size:main',
        ],
    },
    install_requires=[
    ],
    license="LICENSE"
)
