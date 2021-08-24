"""Orgnizations API.


This object is based on the following JSON structure that comes back
from InfluxDB.

.. _json-org-structure:

.. code-block:: json

    {
        "links": {
            "self": "/api/v2/orgs/1",
            "members": "/api/v2/orgs/1/members",
            "owners": "/api/v2/orgs/1/owners",
            "labels": "/api/v2/orgs/1/labels",
            "secrets": "/api/v2/orgs/1/secrets",
            "buckets": "/api/v2/buckets?org=myorg",
            "tasks": "/api/v2/tasks?org=myorg",
            "dashboards": "/api/v2/dashboards?org=myorg"
        },
        "id": "string",
        "name": "string",
        "description": "string",
        "createdAt": "2019-08-24T14:15:22Z",
        "updatedAt": "2019-08-24T14:15:22Z",
        "status": "active"
    }
"""

import json as jsonlib
import re
import typing

# 3rd party
import ciso8601

# Local imports
from . import types
from . import obj


class Organizations:
    """Interface to InfluxDB Organizations API.

    Parameters:
        db (influxdb2.core.Influx): Base connection instance.

    """
    def __init__(self, db):
        self._db = db

    def iterate(
        self,
        org: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
    ):
        """Iterate over all orgs in the database.

        Parameters:
            org (str): Optional. Restrict output to only this org based on
                name.
            org_id (str): Optional. Restrict output to only this org based
                on id.
            user_id (str): Optional. Restrict output to only this orgs
                visible by this user id.

        """

        params = {
            "descending": False,
            "limit": 100,
            "offset": 0,
        }

        if org:
            params["org"] = str(org)
        if org_id:
            params["orgID"] = str(org_id)
        if user_id:
            params["user_id"] = str(user_id)

        rsp = self._db.get("/api/v2/orgs", params=params)
        while True:
            for orgdict in rsp.data:
                org = obj.org.Org()
                org.from_dict(orgdict)
                yield org

            if len(rsp.data) == 100:
                params["offset"] += 100
                rsp = self._db.get("/api/v2/orgs", params=params)
            else:
                break
