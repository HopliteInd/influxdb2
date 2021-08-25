"""Organization Object


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
from .. import types

INVALID = "-invalid-"


class Org:  # pylint: disable=R0902,C0103
    """Object describing an InfluxDB Organization."""

    ID_REGEX = re.compile("^[a-f0-9]{16}$")

    def __init__(
        self,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        org_id: typing.Optional[str] = None,
    ):
        self._name = name if name else INVALID
        # Subtle, but empty string "" becomes None
        self._description = description if description else None
        self._org_id = org_id if org_id else INVALID

        self._active = True
        self._created_at = 0
        self._updated_at = 0
        self._links = {}

    def _reset(self):
        self._name = INVALID
        self._description = None
        self._org_id = INVALID
        self._active = True
        self._created_at = 0
        self._updated_at = 0
        self._links = {}

    @property
    def name(self):
        """(str) Name of the organization."""
        if self._name == INVALID:
            raise ValueError(
                "%s.name referenced before being assigned a value."
                % (__class__.__name__)
            )
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError(
                "%s.name must be a string." % (__class__.__name__)
            )

        if value == INVALID:
            raise ValueError(
                "%s.name %s is a restricted value."
                % (__class__.__name__, repr(INVALID))
            )

        if not value:
            raise ValueError(
                "%s.name must not be empty." % (__class__.__name__)
            )

        self._name = value

    @property
    def description(self) -> types.NullStr:
        """(str or None) Description of the organization."""
        return self._description

    @description.setter
    def description(self, value: types.NullStr):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Description must be a string or None.")

        self._description = value

    @property
    def id(self) -> str:
        """(str) Organization ID from InfluxDB."""
        if self._org_id == INVALID:
            raise ValueError(
                "%s.id reference before being assigned a value."
                % (__class__.__name__)
            )
        return self._org_id

    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise ValueError("%s.id must be a string." % (__class__.__name__))

        if not self.ID_REGEX.match(value):
            raise ValueError(
                "%s.id must be a 16 character hex string."
                % (__class__.__name__)
            )
        self._org_id = value

    @property
    def created(self) -> float:
        """(float) Timestamp of when the org was created.

        The value is seconds since Jan 1, 1970 00:00:00 GMT.

        Raises:
            ValueError: when an invalid value is encountered.
        """
        return self._created_at

    @created.setter
    def created(self, value: types.TimeVal):
        if isinstance(value, (int, float)):
            self._created_at = float(value)
        elif isinstance(value, str):
            dt = ciso8601.parse_datetime(value)
            self._created_at = dt.timestamp()
        else:
            raise ValueError(
                "Invalid type for a timestamp: %s" % (type(value))
            )

    @property
    def updated(self) -> float:
        """(float) Timestamp of when the org was last updated.

        The value is seconds since Jan 1, 1970 00:00:00 GMT.

        Raises:
            ValueError: when an invalid value is encountered.
        """
        return self._updated_at

    @updated.setter
    def updated(self, value: types.TimeVal):
        if isinstance(value, (int, float)):
            self._updated_at = float(value)
        elif isinstance(value, str):
            dt = ciso8601.parse_datetime(value)
            self._updated_at = dt.timestamp()
        else:
            raise ValueError(
                "Invalid type for a timestamp: %s" % (type(value))
            )

    @property
    def active(self) -> bool:
        """(bool) Whether or not the organization is active."""
        return self._active

    @active.setter
    def active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(
                "%s.active must be a bool value." % (__class__.__name__)
            )
        self._active = value

    @property
    def links(self) -> dict:
        """(dict) Links associated with this org."""
        return self._links

    @links.setter
    def links(self, value):
        if not isinstance(value, dict):
            raise ValueError(
                "%s.links Must be a dictionary not [%s]"
                % (__class__.__name__, type(value))
            )
        # Duplicate the links to prevent odd corruption
        self._links = {str(x): str(value[x]) for x in value}

    def from_dict(self, data: dict):
        """Fill object from a dictionary object.

        Parameters:
            data: Dictionary containing an org response from InfluxDB.

                See the :ref:`JSON Org Structure <json-org-structure>` for
                details on what the dictionary should look like.
        """

        try:
            self.id = data["id"]
            self.name = data["name"]
            self.description = data["description"]
            self.created = data["createdAt"]
            self.updated = data["updatedAt"]
            status = data.get("status", "active")
            self.active = status == "active"
            self.links = data["links"]
        except ValueError as err:
            self._reset()
            raise ValueError(
                "%s.from_dict() Invalid dictionary, missing key [%s]"
                % (__class__.__name__, err)
            ) from None

    def from_json(self, data: typing.Union[str, bytes]):
        """Fill object from a json string.

        Parameters:
            data: Dictionary containing an org response from InfluxDB.

                See the :ref:`JSON Org Structure <json-org-structure>` for
                details on what the JSON should look like.
        """

        try:
            dictdata = jsonlib.loads(data)
        except jsonlib.JSONDecodeError as err:
            raise ValueError(
                "%s.from_json() Invalid json data: %s"
                % (__class__.__name__, err)
            ) from None

        try:
            self.from_dict(dictdata)
        except ValueError as err:
            raise ValueError(
                "%s.from_json() Invalid json data: %s"
                % (__class__.__name__, err)
            ) from None
