#!/usr/bin/python
#-*-python-*-##################################################################
# Copyright 2021-2022 Inesonic, LLC
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

"""
Python module that provides a few resources for debugging.

"""

###############################################################################
# Import:
#

###############################################################################
# Functions:
#

def dump_bytes(data):
    """
    Function you can use to dump an bytes or bytearray object.

    :param data:
        The data to be dumped.

    :return:
        Returns a string representation of the byte array.

    :type date: bytes or bytearray
    :rtype:     str

    """

    s = str()
    for b in data:
        if not s:
            s = "%02X"%int(b)
        else:
            s += " %02X"%int(b)

    return s

###############################################################################
# Main:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
