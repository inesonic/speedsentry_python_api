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
This Python module provides a generic dictionary object that allows you to
dynamically create object attributes from a dictionary.

To use this module, use the functions build_read_only_class and/or
build_read_write_class to create class types.  The classes will accept a
dictionary in their __init__ method that will be used to populate the values
of the created attributes.

"""

###############################################################################
# Imports:
#

from typing import Union
from typing import Any

import textwrap
import copy

###############################################################################
# Functions:
#

def build_read_only_class(
    class_name : str,
    class_description : str,
    attribute_descriptions: dict
    ):
    """
    Method that builds a customer object with a given name and read-only
    properties.

    :param class_name:
        The name to assign to objects of this type.

    :param class_description:
        The docstring used to describe this dynamically generated class.

    :param attribute_descriptions:
        The dictionary holding the attribute descriptions.  The dictionary
        should be with each value being a description.  Only keyed attributes
        will be created.

    :return:
        Returns dynamically generated type you can use to represent returned
        JSON data.

    :type description: dict
    :rtype:            class

    """

    def __init__(_self, dictionary):
        dict.__init__(_self, dictionary)

    __init__.__doc__ = """
Method that initializes the %s class.

:param dictionary:
    The dictionary containing the desired element values.

:type dictionary: dict

"""%class_name

    class_type = type(
        class_name,
        ( dict, ),
        {
            "__doc__" : __wrap(class_description),
            "__init__" : __init__
        }
    )

    def __deepcopy__(_self, memo, _ct = class_type):
        d = { k : copy.deepcopy(v, memo) for k, v in _self.items() }
        return _ct(d)

    __deepcopy__.__doc__ = """
Method that performs a deep copy of this class.

:param memo:
    The dictionary used as a memo during the copy.

:return:
    Returns an instance of %s

:type memo: dict
:rtype:     %s
"""%(
        class_name,
        class_name
    )

    setattr(class_type, "__deepcopy__", __deepcopy__)

    for key, docstring in attribute_descriptions.items():
        def getter_function(_self, _key = key):
            return _self[_key]

        def setter_function(_self, _value, _key = key):
            raise AttributeError("attribute %s is read-only"%_key)

        p = property(
            fget = getter_function,
            fset = setter_function,
            doc = __wrap(docstring)
        )

        setattr(class_type, key, p)

    return class_type


def build_read_write_class(
    class_name : str,
    class_description : str,
    attribute_descriptions: dict
    ):
    """
    Method that builds a customer object with a given name and read-write
    properties.

    :param class_name:
        The name to assign to objects of this type.

    :param class_description:
        The docstring used to describe this dynamically generated class.

    :param attribute_descriptions:
        The dictionary holding the attribute descriptions.  The dictionary
        should be with each value being a description.  Only keyed attributes
        will be created.

    :return:
        Returns dynamically generated type you can use to represent returned
        JSON data.

    :type description: dict
    :rtype:            class

    """

    def __init__(_self, dictionary):
        dict.__init__(_self, dictionary)

    __init__.__doc__ = """
Method that initializes the %s class.

:param dictionary:
    The dictionary containing the desired element values.

:type dictionary: dict

"""%class_name

    class_type = type(
        class_name,
        ( dict, ),
        {
            "__doc__" : __wrap(class_description),
            "__init__" : __init__
        }
    )

    def __deepcopy__(_self, memo, _ct = class_type):
        d = { k : copy.deepcopy(v, memo) for k, v in _self.items() }
        return _ct(d)

    __deepcopy__.__doc__ = """
Method that performs a deep copy of this class.

:param memo:
    The dictionary used as a memo during the copy.

:return:
    Returns an instance of %s

:type memo: dict
:rtype:     %s
"""%(
        class_name,
        class_name
    )

    setattr(class_type, "__deepcopy__", __deepcopy__)

    for key, docstring in attribute_descriptions.items():
        def getter_function(_self, _key = key):
            return _self[_key]

        def setter_function(_self, _value, _key = key):
            _self[_key] = _value

        p = property(
            fget = getter_function,
            fset = setter_function,
            doc = __wrap(docstring)
        )

        setattr(class_type, key, p)

    return class_type


def __wrap(text : str) -> str:
    """
    Function that wraps text, inserting newlines.

    :param text:
        The text to be wrapped.

    :return:
        Returns the text with newlines inserted.

    :type text: str
    :rtype:     str

    """

    return "\n".join(textwrap.wrap(text))

###############################################################################
# Test code:
#

if __name__ == "__main__":
    Type1 = build_read_only_class(
        class_name = "Type1",
        class_description = "Test class 1",
        attribute_descriptions = {
            'a' : 'attribute a',
            'b' : 'attribute b',
            'c' : 'attribute c'
        }
    )

    dictionary_1 = {
        'a' : 1,
        'b' : 'b1',
        'c' : 2
    }

    obj1 = Type1(dictionary_1)

    print("obj1.a", str(obj1.a))
    print("obj1.b", str(obj1.b))
    print("obj1.c", str(obj1.c))

    try:
        obj1.b = 5
    except AttributeError as e:
        print("Got expected exception: %s"%str(e))


    Type2 = build_read_write_class(
        class_name = "Type2",
        class_description = "Test class 2",
        attribute_descriptions = {
            'd' : 'attribute d',
            'e' : 'attribute e',
        }
    )

    dictionary_2 = {
        'd' : obj1,
        'e' : 'foo'
    }

    obj2 = Type2(dictionary_2)

    print("obj2.d", str(obj2.d))
    print("obj2.e", str(obj2.e))

    print("Modifying obj2:")
    obj2.d = 5

    print("obj2.d", str(obj2.d))
    print("obj2.e", str(obj2.e))
