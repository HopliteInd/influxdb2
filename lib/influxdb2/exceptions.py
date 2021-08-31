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

"""Exceptions for influxdb2 API.

"""


class InfluxError(Exception):
    """Base exception for all errors in the influxdb2 package."""

    def __init__(self, message):
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        """Error message associated with the exception."""
        return str(self._message)

    def __str__(self):
        return str(self._message)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._message))


class NetworkError(InfluxError):
    """Raised when a network error happens."""


class InfluxHTTPError(InfluxError):
    """Base exception for errors derived from HTTP requests."""

    def __init__(self, status: int, data: any, message: str):
        super().__init__(message)
        self._code = code
        self._data = data

    @property
    def status(self) -> int:
        """HTTP status code for the failed request."""
        return int(self._status)

    @property
    def data(self) -> any:
        """Body that came back from the HTTP Error."""
        return self._data

    def __repr__(self):
        return "%s(%s,%s,%s)" % (
            self.__class__.__name__,
            repr(self.status),
            repr(self.data),
            repr(self.message),
        )


class InfluxAPIError(InfluxError):
    """Exception raised for errors from the InfluxDB API.

    Parameters:
        status: HTTP Status code generating the error.
        code: Status code from InvluxDB's API.
        message: Human readable message describing the error.
        op: Describes the logical code operation during error. Useful for
            debugging.
        err: A stack of errors that occurred during processing of the request.
            Useful for debugging.

    """

    def __init__(
        self, status: int, code: str, message: str, op: str, err: str
    ):
        super().__init__(message)
        self._status = status
        self._code = code
        self._op = op
        self._err = err

    @property
    def status(self) -> int:
        """HTTP status code for the failed request."""
        return int(self._status)

    @property
    def code(self) -> str:
        """InfluxDB description of the error code"""
        return int(self._code)

    @property
    def op(self) -> str:
        """Describes the logical code operation during error."""
        return int(self._op)

    @property
    def err(self) -> str:
        """Stack of errors that occurred during processing of the request."""
        return self._data

    def __repr__(self):
        return "%s(%s,%s,%s,%s,%s)" % (
            self.__class__.__name__,
            repr(self.status),
            repr(self.code),
            repr(self.message),
            repr(self.op),
            repr(self.err),
        )


class AuthenticationDenied(InfluxHTTPError):
    """Raised when a bad password or user name is encountered."""

    def __init__(self):
        super().__init__(
            401, {"error": "Authentication Denied"}, "Authentication Denied"
        )
