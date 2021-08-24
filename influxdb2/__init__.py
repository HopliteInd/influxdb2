"""InfluxDB 2.0 Python API

"""

import logging

# Local imports
from . import core
from . import exceptions
from . import obj
from . import orgs
from . import types

logging.getLogger(__name__).addHandler(logging.NullHandler())


def connect(url: str, token: str):
    """Get an InfluxDB "connection" object.

    Parameters:
        url: Base URL to your InfluxDB instance.
            Example: https://localhost:8086/
        token: Valid token for your user to log in with.
            Example: abcdef1234567890

    Returns:
        :class:`influxdb2.core.Influx` instance.
    """
    return core.Influx(url, token)
