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

"""Core API components.

"""

import collections
import http
import json as jsonlib
import logging
import typing

# 3rd party
import requests

# Local imports
from . import exceptions
from . import orgs

logging.getLogger(__name__).addHandler(logging.NullHandler())


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

    def api_error(self, req: requests.Response):
        """Throw an API exception on errors.

        Parameters:
            req(requests.Response): A ``Response`` object from the ``requests``
                library showing an error.

        Raises:
            :class:`exceptions.InfluxAPIError` on an API error.
            :class:`exceptions.InfluxHTTPError` on a regular HTTP error.
        """
        log.getLogger("%s.%s.api_error" % (__name__, __class__.__name__))

        try:
            json = req.json()
            code = json["code"]
            message = json["message"]
            op = json.get("op", "")
            influx_err = json.get("err", "")
        except KeyError as err:
            logging.error("Non api error response [%d]", req.status_code)
            try:
                tmp = http.HTTPStatus(req.status_code)
                msg = "%d %s" % (tmp.value, tmp.phrase)
            except ValueError:
                msg = "Unknown error code [%d]" % (req.status_code)

            raise exceptions.InfluxHTTPError(
                req.code,
                req.raw,
                msg,
            ) from None
        raise exceptions.InfluxAPIError(
            req.status_code, code, message, op, influx_err
        )

    def _request(
        self,
        method: str,
        path: str,
        ignore_401: bool = False,
        **kwargs,
    ) -> requests.Response:

        url = "%s/%s" % (self._url.rstrip("/"), path.lstrip("/"))

        try:
            req = self._http.request(method, url, **kwargs)

            if req.status_code == 401 and not ignore_401:
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
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

        Returns: ``requests.Response`` object.
        """

        return self._request("delete", path, ignore_401=ignore_401, **kwargs)

    @property
    def orgs(self):
        """Orgs query module"""
        if not self._modules["orgs"]:
            self._modules["orgs"] = orgs.Organizations(self)

        return self._modules["orgs"]
