#!/usr/bin/env python
import codecs
import os
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def read(relative_path):
    with codecs.open(os.path.join(this_directory, relative_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="tarraz",
    version=get_version("tarraz/version.py"),
    packages=["tarraz"],
    install_requires=["Pillow==9.5.0"],
    entry_points={
        "console_scripts": [
            "tarraz = tarraz.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Topic :: Software Development",
    ],
    url="https://github.com/nitfe/tarraz",
    license="GNU Affero General Public License v3",
    author="Ahmed Jazzar",
    author_email="ahmed@nitfe.com",
    description=(
        "A cross-stitch image generator. Generates a cross stitch "
        "pattern given by a user and generates a DMC colored pattern."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
