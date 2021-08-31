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

"""Common objects.


"""

import typing

# Local
from .. import types

class Secret:
    """Object describing a secret key.

    Parameters:
        key (str): Secret key

    """

    def __init__(self, key: typing.Optional[str] = None):
        func_name = "%s.%s" % (__name__, __class__.__name__)
        types.ensure_type(func_name, "key", key, (str, type(None)))
        self._key = key

    @property
    def value(self) -> str:
        """Key value."""
        return self._key

    @property
    def as_bytes(self) -> bytes:
        """Key returned as a byte string."""
        return self._key.encode("utf-8")

    def __bytes__(self):
        return self._key.encode("utf-8")

    def __str__(self):
        return self._key

    def __repr__(self):
        return "%s.%s(%s)" % (__name__, __class__.__name__, "XXX")

