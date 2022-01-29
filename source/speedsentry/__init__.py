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
This Python module provides an API to simplify access to the SpeedSentry REST
API.

This module defines the following classes for your use:

+-----------------------------+-----------------------------------------------+
| Class                       | Function                                      |
+=============================+===============================================+
| SpeedSentry                 | The main SpeedSentry API.  Methods in this    |
|                             | class will generally return one or more       |
|                             | instances of the classes listed below.        |
+-----------------------------+-----------------------------------------------+
| Capabilities                | Typed dictionary holding information about    |
|                             | the capabilities you are granted under your   |
|                             | subscription.                                 |
+-----------------------------+-----------------------------------------------+
| HostScheme                  | Typed dictionary holding returned information |
|                             | for one of your sites.                        |
+-----------------------------+-----------------------------------------------+
| Monitor                     | Typed dictionary holding returned monitor     |
|                             | settings for a single monitor.                |
+-----------------------------+-----------------------------------------------+
| MonitorEntry                | Typed dictionary holding a monitor update     |
|                             | entry.  You can use this class with the       |
|                             | SpeedSentry.monitor_update method to change   |
|                             | your monitor settings.                        |
+-----------------------------+-----------------------------------------------+
| Region                      | Typed dictionary holding data on a single     |
|                             | region we monitor your site from.             |
+-----------------------------+-----------------------------------------------+
| Event                       | Typed dictionary holding data on a single     |
|                             | event.                                        |
+-----------------------------+-----------------------------------------------+
| LatencyEntry                | Typed dictionary holding a single raw latency |
|                             | entry.                                        |
+-----------------------------+-----------------------------------------------+
| AggregatedLatencyEntry      | Typed dictionary holding a single aggregated  |
|                             | latency entry.                                |
+-----------------------------+-----------------------------------------------+
| SpeedSentryException        | Base class for all SpeedSentry exceptions.    |
+-----------------------------+-----------------------------------------------+
| CustomerIdentifierException | Exception that is raised when the a provided  |
|                             | customer identifier is invalid.               |
+-----------------------------+-----------------------------------------------+
| CustomerSecretException     | Exception that is raised when a provided      |
|                             | customer secret is invalid.                   |
+-----------------------------+-----------------------------------------------+
| CommunicationErrorException | Exception that is raised when a communication |
|                             | error is detected.                            |
+-----------------------------+-----------------------------------------------+
| DecodingErrorException      | Exception that is raised when the received    |
|                             | data could not be decoded.                    |
+-----------------------------+-----------------------------------------------+

"""

###############################################################################
# Imports:
#

from .speedsentry import __version__ as __version__
from .speedsentry import Capabilities as Capabilities
from .speedsentry import HostScheme as HostScheme
from .speedsentry import Monitor as Monitor
from .speedsentry import MonitorEntry as MonitorEntry
from .speedsentry import Region as Region
from .speedsentry import Event as Event
from .speedsentry import LatencyEntry as LatencyEntry
from .speedsentry import AggregatedLatencyEntry as AggregatedLatencyEntry

from .exceptions import SpeedSentryException as SpeedSentryException
from .exceptions import CustomerIdentifierException as CustomerIdentifierException
from .exceptions import CustomerSecretException as CustomerSecretException
from .exceptions import CommunicationErrorException as CommunicationErrorException
from .exceptions import DecodingErrorException as DecodingErrorException

from .speedsentry import SpeedSentry as SpeedSentry

###############################################################################
# Test code:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
