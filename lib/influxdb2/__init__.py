# Copyright 2021 Hoplite Industries, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python interface to the InfluxDB 2.0 HTTP API.

Project License
===============

Copyright 2021 Hoplite Industries, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this package except in compliance with the License.
You may obtain a copy of the License at

* Included Apache :download:`LICENSE <../LICENSE>` file.
* http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Package Contents
================

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
        :class:`core.Influx` instance.
    """
    return core.Influx(url, token)
