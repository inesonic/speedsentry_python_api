Inesonic SpeedSentry Python API
===============================
This package provides a simple Python API you can use to communicate with
Inesonic SpeedSentry infrastructure.  You can use this API to:

* Configure Inesonic SpeedSentry programmatically.

* Query latency, SSL expiration data, and event histories associated with your Inesonic SpeedSentry subscription.

* Pause and resume monitoring.

* Trigger custom events, using Inesonic SpeedSentry to report those events to you.

For details on Inesonic SpeedSentry, please goto https://speed-sentry.com.

Developer Documentation
-----------------------
The API is designed to be simple to use.  For details on how to integrate
Inesonic SpeedSentry into your site or project, see
https://speedsentry-documentation.inesonic.com

Supported Python Versions
-------------------------
This API is specifically written to work with Python 3.5 and newer.

Dependencies
------------
The only external dependency required by this module is with the Python
Requests package avaialble at https://pypi.org/project/requests/.   If
necessary, the supplied egg should automatically install any required
dependencies.

Installation
------------
To install:

* Clone or download this repository contents.

* Enter the working copy's top level directory.

* Run the command ``python3 setup.py install``.

License And Support
-------------------
This package is licensed under the LGPLv3.

You are welcome to submit patches and/or request new features either through
GitHub or through SpeedSentry's internal support system.
