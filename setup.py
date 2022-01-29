#!/usr/bin/python
#-*-python-*-##################################################################
# Copyright 2021-2022 Inesonic, LLC
#
#   This program is free software; you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or (at your
#   option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#   License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
###############################################################################

"""
Module that installs the Inesonic SpeedSentry Python API.

For details on this package, see:

    https://documentation.speedsentry.inesonic.com

For product information, see:

    https://speedsentry.inesonic.com

The details of this module were based on the sample PyPI package available at:

    https://github.com/pypa/sampleproject

"""

###############################################################################
# Imports:
#

# Always prefer setuptools over distutils
import setuptools
import pathlib
import glob
import os

###############################################################################
# Globals:
#

README_FILE = "README.rst"
"""
The project description in RST format.

"""

README_MIME_TYPE = "text/x-rst; charset=UTF-8"
"""
The mime type of our README file.

"""

SOURCE_DIRECTORY = "source"
"""
The directory containing the package source.

"""

PACKAGE_NAME = "speedsentry"
"""
The package name.

"""

PACKAGE_DIRECTORY = "speedsentry"
"""
The name of the package directory under our setup directory.

"""

VERSION_SOURCE_FILE = "speedsentry.py"
"""
The source file containing the version number.

"""

DESCRIPTION = "Inesonic SpeedSentry Python API"
"""
The description for this package.

"""

HOME_PAGE = "https://speedsentry.inesonic.com"
"""
The package homepage.

"""

AUTHOR = "Inesonic, LLC"
"""
The package author.

"""

AUTHOR_EMAIL = "inquiries@autonoma.inesonic.com"
"""
Email to send package inquiries to.

"""

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    'Programming Language :: Python :: 3 :: Only',
]
"""
List of classifiers used by PyPI.

"""

KEYWORDS = [
    'speedsentry',
    'rest'
    'api'
]
"""
Keywords used by PyPI to help search for this project.

"""

MINIMUM_PYTHON_VERSION = "3.5"
"""
The minimum required Python version.

"""

MAXIMUM_PYTHON_VERSION = "4.0"
"""
The maximum python version (exclusive)

"""

DEPENDENCIES = [ 'requests >= 2.26.0' ]
"""
List of packages this package depends on.

"""

EXAMPLES_DIRECTORY = 'examples'
"""
The name of the examples directory.

"""

PROJECT_URLS = {
    'Home Page' : 'https://speedsentry.inesonic.com',
    'Documentation' : 'https://documentation.speedsentry.inesonic.com'
}
"""
List of project URLs to display on the home PyPI home page.

"""

POST_INSTALLATION_MESSAGE_1 = """
Thank you for installing the Inesonic SpeedSentry API.  You can file our
API documentation at:

    %s

We have also installed the following examples.  You can use these examples to
better understand how to use the Inesonic SpeedSentry Python API in your
project:
"""
"""
The post installation message to place first.

"""

POST_INSTALLATION_MESSAGE_2 = """
Thank you !
"""
"""
The post installation message to place after the list of examples.

"""
###############################################################################
# Functions:
#

def get_version(source_file):
    version = None
    with open(source_file, 'r') as fh:
        l = fh.readline()
        while l and not version:
            if l.startswith('__version__ = '):
                sections = l.strip().split('=')
                if len(sections) == 2:
                    version = sections[1].strip().replace('"', '')
            if not version:
                l = fh.readline()

    return version

###############################################################################
# Setup:
#

package_setup_directory = pathlib.Path(__file__).parent.resolve()


readme_file = os.path.join(package_setup_directory, README_FILE)
with open(readme_file, 'r') as fh:
    long_description = fh.read()


version_file = os.path.join(
    package_setup_directory,
    SOURCE_DIRECTORY,
    PACKAGE_DIRECTORY,
    VERSION_SOURCE_FILE
)
version = get_version(version_file)


examples_directory = os.path.join(package_setup_directory, EXAMPLES_DIRECTORY)
example_files = [ str(x.relative_to(package_setup_directory))
                  for x in pathlib.Path(examples_directory).iterdir()
]


setuptools.setup(
    name = PACKAGE_NAME,
    version = version,
    description = DESCRIPTION,
    long_description = long_description,
    long_description_content_type = README_MIME_TYPE,
    url = HOME_PAGE,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    classifiers = CLASSIFIERS,
    keywords = ", ".join(KEYWORDS),
    package_dir = { '': SOURCE_DIRECTORY },
    packages = setuptools.find_packages(where = SOURCE_DIRECTORY),
    python_requires = ">=%s, < %s"%(
        MINIMUM_PYTHON_VERSION,
        MAXIMUM_PYTHON_VERSION
    ),
    install_requires = DEPENDENCIES,
    scripts = example_files,
    project_urls = PROJECT_URLS
)


print(POST_INSTALLATION_MESSAGE_1%PROJECT_URLS['Documentation'])
for example_file in example_files:
    print("    %s"%example_file)

print(POST_INSTALLATION_MESSAGE_2)
