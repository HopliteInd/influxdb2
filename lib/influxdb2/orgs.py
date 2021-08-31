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

"""Orgnizations API.

Query and manage the administrative organizations in InfluxDB.
"""

import typing

# 3rd party

# Local imports
from . import obj
from . import types


class Organizations:
    """Interface to InfluxDB Organizations API.

    Parameters:
        db (influxdb2.core.Influx): Base connection instance.

    """

    def __init__(self, db):
        self._db = db

    def iterate(
        self,
        descending: bool = False,
        org: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
    ) -> typing.Iterable[obj.org.Org]:
        """Iterate over all orgs in the database.

        Parameters:
            descending (bool): Default: False. If true sort results in
                descending order by name.  Default is to do ascending.
            org (str): Optional. Restrict output to only this org based on
                name.
            org_id (str): Optional. Restrict output to only this org based
                on id.
            user_id (str): Optional. Restrict output to only this orgs
                visible by this user id.

        Returns:
            Iterable of :class:`influxdb2.obj.org.Org` objects.
        """

        offset = 0

        orgs = self.list(descending, 100, offset, org, org_id, user_id)
        while True:
            for org in orgs:
                yield org

            if len(orgs) == 100:
                offset += 100
                orgs = self.list(descending, 100, offset, org, org_id, user_id)
            else:
                break

    def list(
        self,
        descending: bool = False,
        limit: int = 20,
        offset: int = 0,
        org: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
    ) -> typing.List[obj.org.Org]:
        """List organizations.

        Optionally you can pass in filters to restrict based on user, or org.

        Parameters:
            descending (bool): Default: False. If true sort results in
                descending order by name.  Default is to do ascending.
            limit (int): Default 20.  Limit the number of responses that come
                back from the api.  Used in conjunction with ``offset`` to
                impliment paging.
            offset (int): Default 0. Offset into the query set to return
                results.  Used in conjunction with ``limit`` to impliment
                paging.
            org (str): Optional. Restrict output to only this org based on
                name.
            org_id (str): Optional. Restrict output to only this org based
                on id.
            user_id (str): Optional. Restrict output to only this orgs
                visible by this user id.

        Returns:
            list of :class:`influxdb2.obj.org.Org`

        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.
        """

        class_name = "%s.%s.list" % (__name__, __class__.__name__)
        types.ensure_type(class_name, "descending", descending, bool)
        types.ensure_type(class_name, "limit", limit, int)
        types.ensure_type(class_name, "offset", offset, int)
        types.ensure_type(class_name, "org", org, (str, type(None)))
        types.ensure_type(class_name, "org_id", org_id, (str, type(None)))
        types.ensure_type(class_name, "user_id", user_id, (str, type(None)))

        if limit < 1 or limit > 100:
            raise ValueError(
                "Limit must be within the bounds of 1 to 100 not %d" % limit
            )

        params = {
            "descending": descending,
            "limit": limit,
            "offset": offset,
            "org": org,
            "orgID": org_id,
            "userID": user_id,
        }
        rsp = self._db.get("/api/v2/orgs", params=params)
        retval = []
        if rsp.status_code == 200:
            for orgdict in rsp.json():
                org = obj.org.Org()
                org.from_dict(orgdict)
                retval.append(org)
        else:
            self.api_error(rsp)
        return retval

    def create(
        self, name: str, description: typing.Optional[str]
    ) -> obj.org.Org:
        """Create a new organizatoin in InfluxDB.

        Parameters:
            name: Name of the organization.
            description(str): *Optional*  A longer description of the
                organization.

        Returns:
            :class:`obj.org.Org` object for the new org


        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.
        """
        class_name = "%s.%s.create" % (__name__, __class__.__name__)
        types.ensure_type(class_name, "name", name, str)
        types.ensure_type(
            class_name, "description", description, (str, type(None))
        )

        payload = {"name": name}
        if description:
            payload["description"] = description
        rsp = self._db.post("/api/v2/orgs", json=payload)

        if rsp.status_code == 201:
            org = obj.org.Org()
            org.from_dict(rsp.json())
        else:
            self.api_error(rsp)

        return org

    def get(self, org_id: str) -> obj.org.Org:
        """Get a specific org based on it's ID.

        Parameters:
            org_id: Org ID from InfluxDB

        Returns:
            :class:`obj.org.Org` object for the desired org

        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.

        """
        class_name = "%s.%s.get" % (__name__, __class__.__name__)
        types.ensure_id(class_name, "org_id", org_id)

        rsp = self._db.get("/api/v2/orgs/%s" % org_id)

        if rsp.status_code == 200:
            org = obj.org.Org()
            org.from_dict(rsp.json())
        else:
            self.api_error(rsp)

        return org

    def update(self, org_id: str, name: str, description: str) -> obj.org.Org:
        """Update a specific org based on it's ID.

        Parameters:
            org_id: Org ID from InfluxDB
            name: Name of the organization.
            description(str): *Optional*  A longer description of the
                organization.

        Returns:
            :class:`obj.org.Org` object for the updated org

        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.

        """
        class_name = "%s.%s.get" % (__name__, __class__.__name__)
        types.ensure_id(class_name, "org_id", org_id)
        types.ensure_type(class_name, "name", name, str)
        types.ensure_type(
            class_name, "description", description, (str, type(None))
        )

        payload = {
            "name": name,
            "description": description,
        }

        rsp = self._db.patch("/api/v2/orgs/%s" % org_id, json=payload)

        if rsp.status_code == 200:
            org = obj.org.Org()
            org.from_dict(rsp.json())
        else:
            self.api_error(rsp)

        return org

    def delete(self, org_id: str) -> obj.org.Org:
        """Delete a specific org based on it's ID.

        Parameters:
            org_id: Org ID from InfluxDB

        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.

        """
        class_name = "%s.%s.get" % (__name__, __class__.__name__)
        types.ensure_id(class_name, "org_id", org_id)

        rsp = self._db.delete("/api/v2/orgs/%s" % org_id)

        if rsp.status_code == 204:
            pass
        else:
            self.api_error(rsp)

    def secrets(self, org_id: str) -> typing.List[obj.common.Secret]:
        """Get a list of secrets for an Org base on it's ID.

        Parameters:
            org_id: Org ID from InfluxDB

        Returns:
            List of :class:`obj.common.Secret` object(s) for the requested org

        Raises:
            ValueError when an incoming parameter is of the incorrect type.
            :class:`exceptions.InfluxHTTPError` when a generic HTTP error
                comes back.
            :class:`exceptions.InfluxAPIError` when a known error payload
                returns from the server.

        """
        class_name = "%s.%s.get" % (__name__, __class__.__name__)
        types.ensure_id(class_name, "org_id", org_id)

        rsp = self._db.get("/api/v2/orgs/%s/secrets" % org_id)

        retval = []
        if rsp.status_code == 200:
            json = rsp.json()
            if "secrets" in json:
                for secret in json["secrets"]:
                    retval.append(obj.common.Secret(secret))
            else:
                raise exceptions.InfluxError("Invalid server response")
        else:
            self.api_error(rsp)

        return retval
