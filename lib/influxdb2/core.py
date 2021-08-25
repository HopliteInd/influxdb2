"""Core API components.

"""

import collections
import json as jsonlib
import typing

# 3rd party
import requests

# Local imports
from . import exceptions
from . import orgs

Response = collections.namedtuple("Response", ["code", "data"])


class Influx:
    """Core class for InfluxDB connections."""

    def __init__(self, url: str, token: str, org: typing.Optional[str] = None):

        self._url = url
        self._token = token
        self._org = org

        self._http = requests.Session()
        self._http.headers.update({"authorization": "Token %s" % token})

        self._modules = {
            "orgs": None,
        }

    def _request(
        self,
        method: str,
        path: str,
        ignore_401: bool = False,
        **kwargs,
    ):

        url = "%s/%s" % (self._url.rstrip("/"), path.lstrip("/"))

        try:
            req = self._http.request(method, url, **kwargs)
            try:
                retval = Response(req.status_code, req.json())
            except jsonlib.JSONDecodeError:
                retval = Response(req.status_code, req.raw)

            if retval.code == 401 and not ignore_401:
                raise exceptions.AuthenticationDenied()

        except IOError as err:
            raise exceptions.NetworkError(str(err)) from None

        return retval

    def get(self, path, ignore_401: bool = False, params=None, **kwargs):
        """Sends a GET request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            params: (optional) Dictionary, list of tuples or bytes to send
                in the query string.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        kwargs.setdefault("allow_redirects", True)
        return self._request(
            "get", path, ignore_401=ignore_401, params=params, **kwargs
        )

    def options(self, path, ignore_401: bool = False, **kwargs):
        """Sends an OPTIONS request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        kwargs.setdefault("allow_redirects", True)
        return self._request("options", path, ignore_401=ignore_401, **kwargs)

    def head(self, path, ignore_401: bool = False, **kwargs):
        """Sends a HEAD request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        kwargs.setdefault("allow_redirects", False)
        return self._request("head", path, ignore_401=ignore_401, **kwargs)

    def post(
        self, path, ignore_401: bool = False, data=None, json=None, **kwargs
    ):
        """Sends a POST request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            data: (optional) Dictionary, list of tuples, bytes, or
                file-like object to send in the body of the request.
            json: (optional) json data to send in the body of the request.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        return self._request(
            "post",
            path,
            ignore_401=ignore_401,
            data=data,
            json=json,
            **kwargs,
        )

    def put(self, path, ignore_401: bool = False, data=None, **kwargs):
        """Sends a PUT request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            data: (optional) Dictionary, list of tuples, bytes, or
                file-like object to send in the body of the request.
            json: (optional) json data to send in the body of the request.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        return self._request(
            "put", path, ignore_401=ignore_401, data=data, **kwargs
        )

    def patch(
        self, path, ignore_401: bool = False, data=None, json=None, **kwargs
    ):
        """Sends a PATCH request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                :class:`AuthorizationDeneied` exception when a 401 response
                code is encountered.
            data: (optional) Dictionary, list of tuples, bytes, or
                file-like object to send in the body of the request.
            json: (optional) json data to send in the body of the request.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.
        """

        return self._request(
            "patch",
            path,
            ignore_401=ignore_401,
            data=data,
            json=json,
            **kwargs,
        )

    def delete(self, path, ignore_401: bool = False, **kwargs):
        """Sends a DELETE request.

        Parameters:
            path: API Endpoint path
            ignore_401: (optional) If ``True`` then don't raise an
                    :class:`AuthorizationDeneied` exception when a 401 response
                    code is encountered.
            kwargs: Additional arguments that the requests library takes

        Returns: ``Response`` named tuple.

        """
        return self._request("delete", path, ignore_401=ignore_401, **kwargs)

    @property
    def orgs(self):
        """Orgs query module"""
        if not self._modules["orgs"]:
            self._modules["orgs"] = orgs.Organizations(self)

        return self._modules["orgs"]
