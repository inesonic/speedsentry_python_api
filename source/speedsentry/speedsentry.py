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

"""

###############################################################################
# Imports:
#

from typing import Union
import base64
import json

from .exceptions import *
from . import outbound_rest_api_v1 as outbound_rest_api_v1
from . import dictionary_object as dictionary_object

###############################################################################
# Globals:
#

__version__ = "1.0.0"
"""
The package version number.  This version number differs from Inesonic's
standard scheme in order to comply with PEP 440.

"""

###############################################################################
# Payload classes:
#

Capabilities = dictionary_object.build_read_only_class(
    "Capabilities",
    "You can use this class to hold information about capabilities available "
    "to a customer under their subscription.",
    {
        "maximum_number_monitors" :
            "The maximum number of monitors that can be configured under this "
            "subscription.",
        "polling_interval" :
            "The polling interval per monitor in seconds.",
        "customer_active" :
            "A value that holds True if the customer has verified their "
            "email address.",
        "multi_region_checking" :
            "A value that holds True if customer monitors are checked and "
            "their latency is measured from multiple geographic regions.",
        "supports_wordpress" :
            "A value that holds True if WordPress specific REST endpoints are "
            "supported.",
        "supports_rest_api" :
            "A value that holds True if the full REST API is supported under "
            "this subscription.",
        "supports_content_checking" :
            "A value that holds True if you can enable content change "
            "monitoring under your subscription.",
        "supports_keyword_checking" :
            "A value that holds True if you can enable and use content "
            "keyword checking under your subscription.",
        "supports_post_method" :
            "If True, then you can use any of the available HTTP methods.  "
            "If False, then only the HTTP GET method is supported.",
        "supports_latency_tracking" :
            "If True, then latency will be measured for all monitors.",
        "supports_ssl_expiration_checking" :
            "If True, then the expiration data on all your SSL keys will be "
            "checked.  Events will be generated if your SSL keys are about to "
            "expire.",
        "supports_ping_based_polling" :
            "A value that holds True if your servers will be checked using "
            "echo ICMP messages in addition to normal HTTP messages.  The use "
            "of ping messages allows for faster reporting of a down server.  "
            "Note that ping based polling will be performed automatically "
            "after your server is tested to confirm that ping messages are "
            "not blocked.",
        "supports_maintenance_mode" :
            "A value that holds True if the customer can use maintenance "
            "mode.",
        "supports_rollups" :
            "A value that holds True if the customer can receive weekly "
            "rollups via Email.",
        "paused" :
            "A value that holds True if the customer has enabled maintenance "
            "mode."
    }
)

HostScheme = dictionary_object.build_read_only_class(
    "HostScheme",
    "You can use this class to hold information about a specific host being "
    "checked by one or more monitors.  The class also includes host specific "
    "information such as the SSL expiration date/time if supported by your "
    "subscription.",
    {
        "host_scheme_id" :
            "The numeric ID used to reference this host/scheme entry.",
        "url" :
            "The URL used to access this host.  This will generally be of the "
            "form https://myhost.com or similar.",
        "ssl_expiration_timestamp" :
            "The Unix timestamp when the hosts's SSL certificate will expire."
    }
)

Monitor = dictionary_object.build_read_only_class(
    "Monitor",
    "You can use this class to hold information about a specific monitor you "
    "have configured.",
    {
        "monitor_id" :
            "The numeric ID used to reference this monitor entry.",
        "host_scheme_id" :
            "The host/scheme ID of the host and scheme associated with this "
            "monitor.",
        "user_ordering" :
            "A zero based numeric value indicating the relative order of "
            "monitors on the website settings page.",
        "path" :
            "The path portion of the URL for this monitor, including query "
            "strings.",
        "url" :
            "The full URL for this monitor.  This value is not stored but is "
            "derived from the monitor's path and monitor's host/scheme entry.",
        "method" :
            "The method used to access this endpoint.  Values will be either "
            "\"get\", \"head\", \"post\", \"put\", \"delete\", \"options\", "
            "or \"patch\".",
        "content_check_mode" :
            "Value indicating if content should be checked for changes or for "
            "specific keyword.  Supported values are \"no_check\", "
            "\"content_match\", \"all_keywords\", or \"any_keywords\".",
        "keywords" :
            "A list of keywords to be checked.  The contents of this entry "
            "will be ignored if the content_check_mode value is not "
            "\"all_keywords\" or \"any_keywords\".",
        "post_content_type" :
            "A value indicating the support post content types.  The value "
            "supplied is used to specify the \"Content-Type\" header field "
            "sent to the endpoint.  Supported values are \"text\", \"json\", "
            "and \"xml\".",
        "post_user_agent" :
            "A value indicating the user agent string to be sent to the the "
            "remote endpoint.",
        "post_content" :
            "The raw content to be sent to the remote endpoint during a post."
    }
)

MonitorEntry = dictionary_object.build_read_write_class(
    "MonitorEntry",
    "You can use this class to update or change your monitors.  This class "
    "contains a slightly different set of attributes from the Monitor class.",
    {
        "uri" :
            "You can populate this attribute with either a full URL to the "
            "endpoint you want monitored or you can populate this attribute "
            "with the path.  If a path is used then the host and scheme will "
            "be taken from the previous entry based on the user ordering you "
            "specify.  This is the only required field.",
        "method" :
            "You can use this attribute to specify whether the endpoint "
            "should be tested using HTTP GET, HEAD, POST, etc.  An HTTP "
            "GET method will be used if this parameter is not net.  The "
            "supplied value should be the HTTP method in lower case.",
        "content_check_mode" :
            "You can use this attribute to specify the content check mode to "
            "use for this endpoint.   Supported values are \"no_check\", "
            "\"content_match\", \"all_keywords\", or \"any_keywords\".  If "
            "not specified, then \"no_check\" will be used.",
        "keywords" :
            "You can use this attribute to specify a list of keywords to be "
            "used to check received content.  The list can contain either "
            "strings or bytes objects.  Strings will be converted to UTF-8 "
            "encoded bytes objects automatically.",
        "post_content_type" :
            "You can use this attribute to specify the content type sent by "
            "a HTTP POST message.  The value will be ignored if you specify "
            "an HTTP GET message.  Supported values are  \"text\", \"json\", "
            "and \"xml\".  If not specified, then \"text\" will be used.",
        "post_user_agent" :
            "You can use this attribute to specify the User-Agent string to "
            "include in the HTTP POST header message.  The value is ignored "
            "for HTTP GET messages.",
        "post_content" :
            "You can use this attribute to specify the content to send during "
            "HTTP POST messages.  The value is ignored for HTTP GET "
            "messages.  You can use either string or bytes objects.  String "
            "objects will be automatically UTF-8 encoded."
    }
)

Region = dictionary_object.build_read_only_class(
    "Region",
    "You can use this class to hold information about a region.",
    {
        "region_id" :
            "The numeric ID used to identify this region.",
        "description" :
            "A short textual description of this region."
    }
)

Event = dictionary_object.build_read_only_class(
    "Event",
    "You can use this class to hold information about an event.",
    {
        "event_id" :
            "The numeric ID used to identify this event.",
        "monitor_id" :
            "The numeric ID of the monitor that triggered this event.",
        "timestamp" :
            "The Unix timestamp indicating when the event occurred.",
        "event_type" :
            "The event type.  Supported values are \"working\", "
            "\"no_response\", \"content_changed\", \"keywords\", "
            "\"ssl_certificate_expiring\", \"ssl_certificate_renewed\", "
            "\"customer_1\", \"customer_2\", ... \"customer_10\"."
    }
)

LatencyEntry = dictionary_object.build_read_only_class(
    "LatencyEntry",
    "You can use this class to hold information about a latency datapoint.",
    {
        "monitor_id" :
            "The monitor ID of the monitor where this measurement was taken.",
        "timestamp" :
            "The Unix timestamp indicating when this measurement was taken.",
        "latency" :
            "The measured latency value, in seconds.",
        "region_id" :
            "The region ID of the region where the Inesonic polling server "
            "that took this measurement is located."
    }
)

AggregatedLatencyEntry = dictionary_object.build_read_only_class(
    "AggregatedLatencyEntry",
    "You can use this class to hold information about an aggregation of "
    "latency entries.  This class is similar to LatencyEntry except that it "
    "holds additional statistical data.",
    {
        "monitor_id" :
            "The monitor ID of the monitor where this measurement was taken.",
        "timestamp" :
            "The Unix timestamp indicating when a single randomly selected "
            "sample from the original population was taken.",
        "latency" :
            "The measured latency value, in seconds, of a single randomly "
            "selected value from the original population.",
        "region_id" :
            "The region ID of the region where the Inesonic polling server "
            "that took this measurement is located.",
        "average" :
            "The average latency measured across the original population that "
            "this aggregation represents.",
        "variance" :
            "The population variance of the original population that this "
            "aggregation represents.",
        "minimum" :
            "The lowest measured or best latency found in the original "
            "population.",
        "maximum" :
            "The maximum or worst latency found in the original population.",
        "start_timestamp" :
            "The earliest timestamp of any sample in the original population.",
        "end_timestamp" :
            "The most recent or latest timestamp of any sample in the "
            "original population.",
        "number_samples" :
            "The number of raw samples in the original population that were "
            "used to generate this aggregation."
    }
)


###############################################################################
# Class SpeedSentry:
#

class SpeedSentry(object):
    """
    Class you can use to access the SpeedSentry REST API.

    """

    SECRET_LENGTH = outbound_rest_api_v1.SECRET_LENGTH
    """
    The expected length of the customer secret after decoding, in bytes.

    """

    AUTHORITY = "https://rest.speedsentry.inesonic.com"
    """
    The authority for the customer REST API.

    """

    def __init__(self, customer_identifier, customer_secret):
        """
        Method you can use to initialize the SpeedSentry REST API.

        :param customer_identifier:
            Your customer identifier encoded as an ASCII string of 16
            hexidecimal digits.

        :param customer_secret:
            Your customer secret.  If you supply the secret as a string then
            the secret will be decoded.  If you supply the secret as a bytes or
            bytearray object, then the secret will be used, unmodified.

        :type customer_identifier: str
        :type customer_secret:     str, bytes, or bytearray.

        """

        if len(customer_identifier) != 16:
            raise CustomerIdentifierException(
                "invalid customer identifier length."
            )

        try:
            customer_identifier_value = int(customer_identifier, 16)
        except:
            raise CustomerIdentifierException(
                "customer identifier must contain only the digits 0 through 9 "
                "and A through F (case insensitive)."
            )

        if customer_identifier_value < 0:
            raise CustomerIdentifierException(
                "invalid customer identifier value."
            )

        if isinstance(customer_secret, str):
            try:
                secret = base64.b64decode(customer_secret, validate = True)
            except:
                raise CustomerSecretException("Invalid base-64 string")
        else:
            secret = customer_secret

        if len(secret) != SpeedSentry.SECRET_LENGTH:
            raise CustomerSecretException("Invalid secret length.")

        self.__rest_api = outbound_rest_api_v1.Server(
            customer_identifier = customer_identifier,
            customer_secret = secret,
            authority = SpeedSentry.AUTHORITY
        )


    def capabilities_get(self) -> Capabilities:
        """
        Method you can use to obtain information on what features are supported
        by your subscription.

        :return:
            Returns a Capabilities instance you can use to determine the
            features supported by your subscription.

        :rtype: Capabilities

        """

        response = self.__post_message(
            slug = "/v1/capabilities/get",
            message = dict()
        )

        if 'capabilities' not in response:
            raise CommunicationErrorException(
                status_message = "/v1/capabilities/get : missing capabilities"
            )

        return Capabilities(response['capabilities'])


    def hosts_get(self, host_scheme_id : int) -> HostScheme:
        """
        Method you can use to obtain a single host/scheme entry indexed by
        host/scheme ID.

        :param host_scheme_id:
            The host/scheme ID of the desired host/scheme.

        :return:
            Returns single HostScheme instance.

        :type host_scheme_id: int
        :rtype:               HostScheme

        """

        response = self.__post_message(
            slug = "/v1/hosts/get",
            message = { 'host_scheme_id' : host_scheme_id }
        )

        if 'host_scheme' in response:
            result = HostScheme(response['host_scheme'])
        else:
            raise CommunicationErrorException(
                status_message = "/v1/hosts/get : missing response data"
            )

        return result


    def hosts_list(self) -> dict:
        """
        Method you can use to obtain a dictionary of host/scheme instances
        indexed by host/scheme ID.

        :return:
            Returns a dictionary of HostScheme instances indexed by the
            host/scheme ID.

        :rtype: dict of HostScheme instances

        """

        response = self.__post_message(
            slug = "/v1/hosts/list",
            message = dict()
        )

        if 'host_schemes' in response:
            result = dict()
            for host_scheme_id, host_entry in response['host_schemes'].items():
                result[host_scheme_id] = HostScheme(host_entry)
        else:
            raise CommunicationErrorException(
                status_message = "/v1/hosts/list : missing response data"
            )

        return result


    def monitors_get(self, monitor_id : int) -> Monitor:
        """
        Method you can use to obtain information on a single monitor.

        :param monitor_id:
            The ID of the desired monitor.

        :return:
            Returns a Monitor instance describing this monitor.

        :type monitor_id: int
        :rtype:           Monitor instance

        """

        response = self.__post_message(
            slug = "/v1/monitors/get",
            message = { 'monitor_id' : monitor_id }
        )

        if 'monitor' in response:
            monitor_data = response['monitor']
            result = self.__post_process_monitor(monitor_data)
        else:
            raise CommunicationErrorException(
                status_message = "/v1/monitors/get : missing response data"
            )

        return result


    def monitors_list(self, order_by : str = "monitor_id") -> dict:
        """
        Method you can use to obtain a list of all monitors.

        :param order_by:
            A string indicating the desired method the monitors should be
            indexed.  Supported values are "monitor_id", "user_ordering",
            or "url".

        :return:
            Returns a dictionary of Monitor instances.

        :type order_by: str
        :rtype:         dict of Monitor instances

        """

        response = self.__post_message(
            slug = "/v1/monitors/list",
            message = { 'order_by' : order_by }
        )

        print(json.dumps(response, indent = 4));
        if 'monitors' in response:
            result = dict()
            monitors_data = response['monitors']
            for k, monitor_data in monitors_data.items():
                if isinstance(monitor_data, dict):
                    result[k] = self.__post_process_monitor(monitor_data)
                else:
                    result[k] = [ self.__post_process_monitor(md)
                                  for md in monitor_data
                                ]
        else:
            raise CommunicationErrorException(
                status_message = "/v1/monitors/list : missing response data"
            )

        return result


    def monitors_update(self, monitor_data : list):
        """
        Method you can use to update monitor settings.

        :param monitor_data:
            A list of MonitorEntry instances.  The first entry has a user
            ordering of 0, the second entry has a user ordering of 1, etc.

        :type monitor_data: list

        """

        message = list()
        number_entries = len(monitor_data)
        for i in range(number_entries):
            entry = dict(monitor_data[i])
            if 'post_content' in entry:
                post_content = entry['post_content']
                if isinstance(post_content, str):
                    post_content = post_content.encode('utf-8')

                entry['post_content'] = base64.b64encode(
                    post_content
                ).decode('utf-8')

            if 'keywords' in entry:
                keywords = list()
                for keyword in entry['keywords']:
                    if isinstance(keyword, str):
                        kw = base64.b64encode(keyword.encode('utf-8'))
                    else:
                        kw = base64.b64encode(keyword)

                    keywords.append(kw.decode('utf-8'))

                entry['keywords'] = keywords

            message.append(entry)

        self.__post_message(
            slug = "/v1/monitors/update",
            message = message
        )


    def regions_get(self, region_id : int) -> Region:
        """
        Method you can use to obtain information on a single region.

        :param region_id:
            The ID of the desired region.

        :return:
            Returns a Region instance describing this region.

        :type region_id: int
        :rtype:          Region instance

        """

        response = self.__post_message(
            slug = "/v1/regions/get",
            message = { 'region_id' : region_id }
        )

        if 'region' in response:
            result = Region(response['region'])
        else:
            raise CommunicationErrorException(
                status_message = "/v1/regions/get : missing response data"
            )

        return result


    def regions_list(self) -> dict:
        """
        Method you can use to obtain a dictionary holding information on all
        regions.  The dictionary will be indexed by region ID.

        :return:
            Returns a dictionary of regions by region ID.

        :rtype: dict

        """

        response = self.__post_message(slug = "/v1/regions/list",message = {})
        if 'regions' in response:
            result = dict()
            for region_id, region_data in response['regions'].items():
                result[int(region_id)] = Region(region_data)
        else:
            raise CommunicationErrorException(
                status_message = "/v1/regions/list : missing response data"
            )

        return result


    def events_get(self, event_id : int) -> Event:
        """
        Method you can use to obtain information on a single event.

        :param event_id:
            The ID of the desired event.

        :return:
            Returns an Event instance describing the event.

        :type event_id: int
        :rtype:         Event instance

        """

        response = self.__post_message(
            slug = "/v1/events/get",
            message = { 'event_id' : event_id }
        )

        if 'event' in response:
            result = Event(response['event'])
        else:
            raise CommunicationErrorException(
                status_message = "/v1/events/get : missing response data"
            )

        return result


    def events_list(
        self,
        start_timestamp : int = None,
        end_timestamp : int = None
        ) -> list:
        """
        Method you can use to obtain a list of events.

        :param start_timestamp:
            An optional starting Unix timestamp for events.  A value of None
            means no start time.

        :param end_timestamp:
            An optional ending Unix timestamp for events.  A value of None
            means no end time.

        :return:
            Returns a list of events.

        :type start_timestamp: int or None
        :type end_timestamp:   int or None
        :rtype:                list

        """

        message = dict()
        if start_timestamp is not None:
            message['start_timestamp'] = start_timestamp

        if end_timestamp is not None:
            message['end_timestamp'] = end_timestamp

        response = self.__post_message(
            slug = "/v1/events/list",
            message = message
        )

        if 'events' in response:
            result = list()
            for event in response['events']:
                result.append(Event(event))
        else:
            raise CommunicationErrorException(
                status_message = "/v1/events/list : missing response data"
            )

        return result


    def events_create(
        self,
        message : str,
        type_index = None,
        monitor_id = None
        ):
        """
        Method you can use to generate a customer event.

        :param message:
            The message to be sent as part of the event.

        :param type_index:
            A value indicating the type of customer event to be created.  A
            value of 1 indicates customer_1, a value of 2 indicates customer_2,
            etc.  If not specified, then customer_1 is used.

        :param monitor_id:
            An optional monitor ID you can tie to this message.  If not
            specified or None, then the first monitor ID is used.

        :type message:    str
        :type monitor_id: int or None

        """

        msg = { 'message' : message }
        if monitor_id is not None:
            msg['monitor_id'] = monitor_id

        if type_index is not None:
            msg['type'] = type_index

        self.__post_message(slug = "/v1/events/create", message = msg)


    def status_get(self, monitor_id : int) -> str:
        """
        Method you can use to obtain status on a specific monitor.

        :param monitor_id:
            The ID of the desired monitor.

        :return:
            Returns a string holding "unknown", "working", or "failed"
            indicating the last reported status for this monitor.

        :type monitor_id: int
        :rtype:           str

        """

        response = self.__post_message(
            slug = "/v1/status/get",
            message = { 'monitor_id' : monitor_id }
        )

        if 'monitor_status' in response:
            result = response['monitor_status']
        else:
            raise CommunicationErrorException(
                status_message = "/v1/status/get : missing response data"
            )

        return result


    def status_list(self) -> dict:
        """
        Method you can use to obtain a dictionary holding the status for each
        monitor under your subscription.

        :return:
            Returns a dictionary holding the status of each monitor under your
            subscription.  The dictionary is keyed by monitor ID.  Each entry
            holds one of "unknown", "working", or "failed" indicating the last
            reported status for the monitor.

        :rtype: dict

        """

        response = self.__post_message(
            slug = "/v1/status/list",
            message = dict()
        )

        if 'monitor_status' in response:
            monitor_status = response['monitor_status']
            result = { int(k) : v for k, v in monitor_status.items() }
        else:
            raise CommunicationErrorException(
                status_message = "/v1/status/list : missing response data"
            )

        return result


    def multiple_list(self) -> dict:
        """
        Method you can use to obtain a dictionary holding multiple useful
        values in a single request.

        :return:
            Returns a dictionary holding:
                * A dictionary of monitors by user order.
                * A dictionary of authorities by host/scheme ID.
                * A dictionary of events in chronological order.
                * A dictionary of monitor status values by monitor ID.

        :rtype: dict

        """

        response = self.__post_message(
            slug = "/v1/multiple/list",
            message = dict()
        )

        if 'monitors' in response       and \
           'host_schemes' in response   and \
           'events' in response         and \
           'monitor_status' in response     :
            events = list()
            for event in response['events']:
                events.append(Event(event))

            raw_monitor_status = response['monitor_status']
            monitor_status = { int(k) : v
                               for k, v in raw_monitor_status.items()
                             }

            authorities = dict()
            for host_scheme_id, host_entry in response['host_schemes'].items():
                authorities[host_scheme_id] = HostScheme(host_entry)

            raw_monitors_data = response['monitors']
            monitors = dict()
            for k, monitor_data in raw_monitors_data.items():
                if isinstance(monitor_data, dict):
                    monitors[k] = self.__post_process_monitor(monitor_data)
                else:
                    monitors[k] = [ self.__post_process_monitor(md)
                                    for md in monitor_data
                                  ]

            result = {
                'authorities' : authorities,
                'monitors' : monitors,
                'events' : events,
                'status' : monitor_status
            }
        else:
            raise CommunicationErrorException(
                status_message = "/v1/status/list : missing response data"
            )

        return result


    def latency_list(self, **kwargs) -> tuple:
        """
        Method you can use to obtain latency entries.  Information can be
        limited to a specific timeframe, region, and/or monitor.

        :param start_timestamp:
            An optional starting Unix timestamp for events.  A value of None
            means no start time.

        :param end_timestamp:
            An optional ending Unix timestamp for events.  A value of None
            means no end time.

        :param region_id:
            An optional region ID.  If specified, then only values for this
            region will be included.  Note that this parameter is mutually
            exclusive with monitor_id.

        :param monitor_id:
            An optional monitor ID.  If specified, then only values for this
            monitor will be included.  Note that this parameter is mutually
            exclusive with region_id.

        :return:
            Returns a tuple holding a list of LatencyEntry instances followed
            by a list of AggregatedLatencyEntry instances.  The most recent
            values will be in the first list.  The second list represents an
            aggregation of older values stored at a lower resolution and with
            additional information.

        :rtype: tuple

        """

        response = self.__post_message(
            slug = "/v1/latency/list",
            message = kwargs
        )

        if 'recent' in response and 'aggregated' in response:
            recent = response['recent']
            aggregated = response['aggregated']

            result = (
                [ LatencyEntry(s) for s in recent ],
                [ AggregatedLatencyEntry(s) for s in aggregated ]
            )
        else:
            raise CommunicationErrorException(
                status_message = "/v1/latency/list : missing response data"
            )

        return result


    def latency_plot(self, **kwargs) -> bytes:
        """
        Method you can use to obtain a pre-generated plot of latency data.

        :param monitor_id:
            An optional numeric monitor ID indicating the monitor of interest.
            Data aggregated from all monitors will be used if this parameter is
            not included.

        :param region_id:
            An optional numeric region ID indicating the region we want latency
            plots for.  Data aggregated for all regions will be used if this
            parameter is not included.

        :param start_timestamp:
            An optional Unix timestamp indicating the start date/time to be
            used for the plot data.  IF excluded, then the oldest existing data
            will be included.

        :param end_timestamp:
            An optional Unix timestamp indicating the end date/time to be used
            for the plot data.  If excluded, now is assumed.

        :param title:
            An optional title to place on the plot.

        :param x_axis_label:
            An optional label to apply to the horizontal axis.

        :param y_axis_label:
            An optional label to apply to the vertical axis.

        :param minimum_latency:
            The lower bounds for the latency values to plot.  If excluded, then
            a reasonable lower bound will be selected based on the source data.

        :param maximum_latency:
            The upper bounds for the latency values to plot.  If excluded, then
            a reasonable upper bound will be selected based on the source data.

        :param log_scale:
            A boolean value indicating that a log scale should be used for
            latency values.  A linear scale will be used by default.  This
            value is only used for history plots.

        :param width:
            The desired plot width, in pixels.  Value can range from 100 to
            2048.   The value 1024 will be used by default.

        :param height:
            The desired plot height in pixels.  Value can range from 100 to
            2048.  The value 768 will be used by default.

        :param plot_type:
            The plot type to be generated.  Supported values are "history" and
            "histogram".  A history plot will be generated by default.

        :param format:
            The format of the returned data.  Value can be "jpg" or "png".  PNG
            encoded plots will be returned by default.

        :return:
            Returns a bytes object holding the plot image.

        :type monitor_id:      int
        :type region_id:       int
        :type start_timestamp: int
        :type end_timestamp:   int
        :type title:           str
        :type x_axis_label:    str
        :type y_axis_label:    str
        :type minimum_latency: float
        :type maximum_latency: float
        :type log_scale:       bool
        :type width:           int
        :type height:          int
        :type plot_type:       str
        :type format:          str
        :rtype:                bytes

        """

        return self.__rest_api.post_binary_message(
            slug = "/v1/latency/plot",
            message = kwargs
        )


    def __post_message(self, slug : str, message : dict) -> dict:
        """
        Method used internally to post a message and check for successful
        status.

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

        response = self.__rest_api.post_message(slug = slug, message = message)
        if 'status' in response:
            status = response['status']
            if status != 'OK':
                raise CommunicationErrorException(
                    status_message = "%s : %s"%(slug, status)
                )
        else:
            raise CommunicationErrorException(
                status_message = "%s : unexpected response"%slug
            )

        return response


    def __post_process_monitor(self, monitor_data : dict) -> dict:
        """
        Method used internally to decode base-64 encoded entries.

        :param monitor_data:
            The raw received monitor data.

        :return:
            Returns a Monitor instance holding the processed data.

        :type monitor_data: dict
        :rtype:             Monitor

        """

        processed = monitor_data;
        keywords = list()
        for raw_keyword in monitor_data['keywords']:
            try:
                decoded_keyword = base64.b64decode(
                    raw_keyword,
                    validate = True
                )
            except:
                raise DecodingErrorException(
                    status_message = "could not decode keywords."
                )

            keywords.append(decoded_keyword)

        processed['keywords'] = keywords

        try:
            post_content = base64.b64decode(
                monitor_data['post_content'],
                validate = True
            )
        except:
            raise DecodingErrorException(
                status_message = "could not decode post content."
            )

        processed['post_content'] = post_content

        return Monitor(processed)

###############################################################################
# Test code:
#

if __name__ == "__main__":
    import sys
    sys.stderr.write(
        "*** This module is not intended to be run as a script..\n"
    )
    exit(1)
