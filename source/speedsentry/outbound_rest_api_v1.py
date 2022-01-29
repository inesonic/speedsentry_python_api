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
Python module that can be used to send messages via a generic webhook
mechanism.

This module will include support for posting messages only if the requests
module and related dependencies are included.

"""

###############################################################################
# Import:
#

from typing import Union

import time
import struct
import hashlib
import hmac
import json
import base64
import requests

from .exceptions import CommunicationErrorException

###############################################################################
# Globals:
#

DEFAULT_TIME_DELTA_SLUG = "td"
"""
The default slug to use to obtain time deltas.

"""

HASH_ALGORITHM = hashlib.sha256
"""
The hashing algorithm to be used to generate the key.

"""

HASH_BLOCK_SIZE = 64
"""
The block length to use for the HMAC.

"""

SECRET_LENGTH = HASH_BLOCK_SIZE - 8
"""
The required secret length.  Value is selected to provide good security while
also minimizing computation time for the selected hash algorithm.

"""

###############################################################################
# Class Server:
#

class Server(object):
    """
    Class that tracks information about a remote server.

    """

    def __init__(
        self,
        customer_identifier : str,
        customer_secret : bytes,
        authority : str,
        time_delta_slug : str = DEFAULT_TIME_DELTA_SLUG,
        ):
        """
        Method that initializes the Server class.

        :param customer_identifier:
            Your customer identifier encoded as an ASCII string of 16
            hexidecimal digits.

        :param customer_secret:
            Your customer secret.

        :param authority:
            The server authority.

        :param time_delta_slug:
            The endpoint used to determine the time delta between this
            machine and the server.

        :type customer_identifier: str
        :type customer_secret:     bytes
        :type authority:           str
        :type time_delta_slug:     str

        """

        super().__init__()

        self.__customer_identifier = customer_identifier
        self.__customer_secret = customer_secret
        self.__authority = self.__fix_authority(authority)
        self.__time_delta_slug = self.__fix_slug(time_delta_slug)
        self.__current_time_delta = 0


    def post_message(self, slug : str, message : dict) -> dict:
        """
        Method that will issue a request to a remote server.  If needed, the
        method will query for an updated time delta and perform a retry.

        Note that this method will raise an exception if communication was not
        successful.

        :param slug:
            The slug to be used.

        :param message:
            A dictionary holding the message to be sent.

        :return:
            Returns a dictionary with the response.

        :type slug:    str
        :type message: dict
        :rtype:        dict

        """

        fixed_slug = self.__fix_slug(slug)
        response = self.__post_message(fixed_slug, message)
        if response is None:
            new_time_delta = self.__time_delta()
            if new_time_delta is not None:
                self.__current_time_delta = new_time_delta
                response = self.__post_message(fixed_slug, message)
                if response is None:
                    raise CommunicationErrorException(status_code = 401)

        return response


    def post_binary_message(self, slug : str, message : dict) -> dict:
        """
        Method that will issue a request to a remote server.  If needed, the
        method will query for an updated time delta and perform a retry.

        Note that this method will raise an exception if communication was not
        successful.

        :param slug:
            The slug to be used.

        :param message:
            A dictionary holding the message to be sent.

        :return:
            Returns a dictionary with the response.

        :type slug:    str
        :type message: dict
        :rtype:        dict

        """

        fixed_slug = self.__fix_slug(slug)
        response = self.__post_binary_message(fixed_slug, message)
        if response is None:
            new_time_delta = self.__time_delta()
            if new_time_delta is not None:
                self.__current_time_delta = new_time_delta
                response = self.__post_binary_message(fixed_slug, message)
                if response is None:
                    raise CommunicationErrorException(status_code = 401)

        print(str(type(response)))
        return response


    def __time_delta(self): # -> Union(int, NoneType)
        """
        Function you can use to determine the system clock time delta between
        us and a remote server.

        :param website_url:
            The website URL to determine the time delta with.

        :param webhook:
            The time-delta webhook on the remote server.

        :return:
            Returns the measured time delta, in seconds.

        :type website_url: str
        :type webhook:     str
        :rtype:            int or None

        """

        url = "%s/%s"%(self.__authority, self.__time_delta_slug)

        message_payload = { 'timestamp' : int(time.time()) }
        payload = json.dumps(message_payload)

        response = requests.post(
            url,
            data = payload,
            headers = {
                'User-Agent' : 'Inesonic, LLC',
                'Content-Type' : 'application/json',
                'Content-Length' : str(len(payload))
            }
        )

        if response.status_code == 200:
            try:
                json_result = json.loads(response.text)
            except:
                raise CommunicationErrorException(
                    status_message = "/td : not JSON response"
                )

            if 'status' in json_result:
                if len(json_result) == 2         and \
                   'status' in json_result       and \
                   'time_delta' in json_result   and \
                   json_result['status'] == 'OK'     :
                    try:
                        result = int(json_result['time_delta'])
                    except:
                        raise CommunicationErrorException(
                            status_message = "/td : invalid returned value"
                        )
                else:
                    raise CommunicationErrorException(
                        status_message = json_response['status']
                    )
            else:
                raise CommunicationErrorException(
                    status_message = "/td : unexpected response"
                )
        else:
            raise CommunicationErrorException(
                status_code = response.status_code
            )

        return result


    def __post_message(
        self,
        slug : str,
        message : dict
        ): # -> Union(dict, NoneType):
        """
        Method that will issue a request to a remote server.

        :param slug:
            The slug to be used.

        :param message:
            A dictionary holding the message to be sent.

        :return:
            Returns a dictionary with the response or None if the provided hash
            was invalid.

        :type slug:    str
        :type message: dict
        :rtype:        dict or None

        """

        url = "%s/%s"%(self.__authority, slug)
        raw_message = json.dumps(message).encode('utf-8')

        hash_time_value = int(
              (int(time.time()) + self.__current_time_delta)
            / 30
        )

        hash_time_data = struct.pack('<Q', hash_time_value)
        key = self.__customer_secret + hash_time_data

        raw_hash = hmac.new(
            key = key,
            msg = raw_message,
            digestmod = HASH_ALGORITHM
        ).digest()

        encoded_message = base64.b64encode(raw_message)
        encoded_hash = base64.b64encode(raw_hash)

        message_payload = {
            'cid' : self.__customer_identifier,
            'data' : encoded_message.decode('utf-8'),
            'hash' : encoded_hash.decode('utf-8')
        }

        payload = json.dumps(message_payload)
        response = requests.post(
            url,
            data = payload,
            headers = {
                'User-Agent' : 'Python API: ' + self.__customer_identifier,
                'Content-Type' : 'application/json',
                'Content-Length' : str(len(payload))
            }
        )

        if response.status_code == 200:
            try:
                result = json.loads(response.text)
            except:
                raise CommunicationErrorException(
                    status_message = "%s : not JSON response"
                )
        elif response.status_code == 401:
            result = None
        else:
            raise CommunicationErrorException(
                status_code = response.status_code
            )

        return result


    def __post_binary_message(
        self,
        slug : str,
        message : dict
        ): # -> Union[bytes, NoneType]
        """
        Method that will issue a request to a remote server that expects a
        binary response.

        :param slug:
            The slug to be used.

        :param message:
            A dictionary holding the message to be sent.

        :return:
            Returns a bytes object holding the response.  The value None is
            returned if the message could not be authenticated.

        :type slug:    str
        :type message: dict
        :rtype:        bytes or None

        """

        url = "%s/%s"%(self.__authority, slug)
        raw_message = json.dumps(message).encode('utf-8')

        hash_time_value = int(
              (int(time.time()) + self.__current_time_delta)
            / 30
        )

        hash_time_data = struct.pack('<Q', hash_time_value)
        key = self.__customer_secret + hash_time_data

        raw_hash = hmac.new(
            key = key,
            msg = raw_message,
            digestmod = HASH_ALGORITHM
        ).digest()

        encoded_message = base64.b64encode(raw_message)
        encoded_hash = base64.b64encode(raw_hash)

        message_payload = {
            'cid' : self.__customer_identifier,
            'data' : encoded_message.decode('utf-8'),
            'hash' : encoded_hash.decode('utf-8')
        }

        payload = json.dumps(message_payload)
        response = requests.post(
            url,
            data = payload,
            headers = {
                'User-Agent' : 'Python API: ' + self.__customer_identifier,
                'Content-Type' : 'application/json',
                'Content-Length' : str(len(payload))
            }
        )

        if response.status_code == 200:
            result = response.content
        elif response.status_code == 401:
            result = None
        else:
            raise CommunicationErrorException(
                status_code = response.status_code
            )

        return result


    def __fix_slug(self, slug : str) -> str:
        """
        Method used to fix a provided slug, removing leading and trailing
        slashes.

        :param slug:
            The slug to be cleaned.

        :return:
            Returns the cleaned slug.

        :type slug: str
        :rtype:     str

        """

        if slug.startswith('/'):
            slug = slug[1:]

        if slug.endswith('/'):
            slug = slug[:-1]

        return slug


    def __fix_authority(self, authority : str) -> str:
        """
        Method used to fix a provided authority, removing trailing slashes.

        :param authority:
            The authority to be fixed.

        :return:
            Returns the cleaned authority.

        :type authority: str
        :rtype:          str

        """

        if authority.endswith('/'):
            authority = authority[:-1]

        return authority

###############################################################################
# Main:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
