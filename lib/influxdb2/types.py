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

"""Defining custom types and type enforcement helpers.

"""

import enum
import re
import typing

NullStr = typing.TypeVar("NullStr", str, None)
"""String that can be None."""

TimeVal = typing.TypeVar("TimeVal", str, int, float)
"""A timestamp (str - iso8601 format) or number representing a timestamp."""


ID_REGEX = re.compile("^[a-f0-9]{16}$")
"""Regex to validate a string is a syntactically valid ID in InfluxDB."""


def ensure_type(
    src: str,
    name: str,
    value: typing.Any,
    obj_type: typing.Type[typing.Union[typing.Any, typing.Tuple[type, type]]],
):
    """Ensure the type cast of an object.

    Parameters:
        src: Source function name.
        name: Variable name for the object in ``value``.
        value: Object to ensure the type of.
        obj_type: Type of object that value must be.  This may be a tuple of
            types as well.

    Raises:
        ValueError: If the type does not match  ``obj_type``
    """

    if not isinstance(value, obj_type):
        raise ValueError(
            "%s '%s' must be of type(s) %s not: '%s'"
            % (src, name, repr(obj_type), type(value))
        )


def ensure_id(
    src: str,
    name: str,
    value: str,
):
    """Ensure a variable is a syntactically valid id within InfluxDB

    Parameters:
        src: Source function name.
        name: Variable name for the id in ``value``.
        value: Object to validate that it's of the correct ID syntax.

    Raises:
        ValueError: If the value is not a valid id.
    """

    if not isinstance(value, str):
        raise ValueError(
            "%s '%s' must be of type 'str' not: '%s'"
            % (src, name, type(value))
        )
    if not ID_REGEX.match(value):
        raise ValueError(
            "%s '%s' does not match ID syntax (16 digit hex)" % (src, name)
        )
