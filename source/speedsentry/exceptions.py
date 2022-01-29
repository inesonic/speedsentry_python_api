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
This Python module provides exception classes for the SpeedSentry REST API.

"""

###############################################################################
# Class SpeedSentryException:
#

class SpeedSentryException(Exception):
    """
    Base class for all SpeedSentry exception classes.

    """

    def __init__(self, error_reason):
        """
        Method that initializes the SpeedSentryException class.

        :param error_reason:
            The reason for this exception.

        :type error_reason: str

        """

        self.__error_reason = str(error_reason)


    @property
    def error_reason(self):
        """
        Read-only property that provides the reason for this error.

        :type: str

        """

        return self.__error_reason


    def __str__(self):
        return self.__error_reason

###############################################################################
# Class CustomerIdentifierException:
#

class CustomerIdentifierException(SpeedSentryException):
    """
    Exception class that is raised when an invalid customer identifier is
    provided.

    """

    def __init__(self, error_reason):
        """
        Method that initializes the CustomerIdentifierException.

        :param error_reason:
            The reason for this exception.

        :type error_reason: str

        """

        super().__init__(error_reason)

###############################################################################
# Class CustomerIdentifierException:
#

class CustomerSecretException(SpeedSentryException):
    """
    Exception class that is raised when an invalid customer secret is provided.

    """

    def __init__(self, error_reason):
        """
        Method that initializes the CustomerSecretException.

        :param error_reason:
            The reason for this exception.

        :type error_reason: str

        """

        super().__init__(error_reason)

###############################################################################
# Class CommunicationErrorException:
#

class CommunicationErrorException(SpeedSentryException):
    """
    Exception class that is raised when an communication error occurs.

    """

    def __init__(self, status_code = None, status_message = None):
        """
        Method that initializes the CommunicationErrorException.

        :param status_code:
            The returned server status code.  A value of None indicates no
            error status.

        :param status_message:
            The failure status message returned by the server.

        :type status_code:    int
        :type status_message: str or None

        """

        if status_code is not None:
            if status_message is not None:
                error_message = "%d : %s"%(status_code, status_message)
            else:
                error_message = "returned status %d"%status_code
        elif status_message is not None:
            error_message = status_message
        else:
            error_message = str()

        super().__init__(error_message)

###############################################################################
# Class DecodingErrorException:
#

class DecodingErrorException(SpeedSentryException):
    """
    Exception class that is raised when received data could not be decoded.

    """

    def __init__(self, status_message = None):
        """
        Method that initializes the DecodingErrorException.

        :param status_message:
            A message describing the error.

        :type status_message: str

        """

        super().__init__(status_message)

###############################################################################
# Test code:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be used as a script.\n"
    )
    exit(1)
