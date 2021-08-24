"""Exceptions for influxdb2 API.

"""

import typing


class InfluxError(Exception):
    """Base exception for all errors in the influxdb2 package."""

    def __init__(self, message):
        super().__init__()
        self._message = message

    @property
    def message(self) -> str:
        """(str) Error message associated with the exception."""
        return str(self._message)

    def __str__(self):
        return str(self._message)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._message))


class NetworkError(InfluxError):
    """Raised when a network error happens."""


class InfluxHTTPError(InfluxError):
    """Base exception for errors derived from HTTP requests."""

    def __init__(self, code: int, data: any, message: str):
        super().__init__(message)
        self._code = code
        self._data = data

    @property
    def code(self) -> int:
        """(int) HTTP return code"""
        return int(self._code)

    @property
    def data(self) -> any:
        """(any) Data associated with the HTTP Error."""
        return self._data

    def __repr__(self):
        return "%s(%s,%s,%s)" % (
            self.__class__.__name__,
            repr(self.code),
            repr(self.data),
            repr(self.message),
        )


class AuthenticationDenied(InfluxHTTPError):
    def __init__(self):
        super().__init__(
            401, {"error": "Authentication Denied"}, "Authentication Denied"
        )

