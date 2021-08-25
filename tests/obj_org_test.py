#!/usr/local/hoplite/bin/python3
import unittest
import os
import sys
import socket

sys.path.insert(0, os.path.realpath(os.path.join("..", "lib")))
import influxdb2

VALID_JSON = """
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
    "id": "abcdef0123456789",
    "name": "example.com",
    "description": "Example Company",
    "createdAt": "2019-08-24T14:15:22Z",
    "updatedAt": "2019-08-24T14:15:22.4485Z",
    "status": "inactive"
}
"""
INVALID_JSON_VALUES = """
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
    "id": "abcdef0123456789",
    "name": "example.com",
    "description": "Example Company",
    "createdAt": "2019-08-24T14:15:22Z",
    "updatedAt": "",
    "status": "inactive"
}
"""

INVALID_JSON = """
[}
"""


class TestOrgs(unittest.TestCase):
    def test_empty(self):
        org = influxdb2.obj.org.Org()

        with self.assertRaises(ValueError):
            org.name
        with self.assertRaises(ValueError):
            org.id
        assert org.description is None
        assert org.updated == 0.0
        assert org.created == 0.0
        assert org.active == True

    def test_invalid(self):
        org = influxdb2.obj.org.Org()

        with self.assertRaises(ValueError):
            org.name = None

    def test_valid_json(self):
        org = influxdb2.obj.org.Org()
        org.from_json(VALID_JSON)

        assert org.id == "abcdef0123456789"
        assert org.name == "example.com"
        assert org.description == "Example Company"
        assert org.created == 1566656122.0
        assert org.updated == 1566656122.4485
        assert org.active == False
        assert org.links["self"] == "/api/v2/orgs/1"

    def test_invalid_json(self):
        org = influxdb2.obj.org.Org()
        with self.assertRaises(ValueError):
            org.from_json(INVALID_JSON)

        with self.assertRaises(ValueError):
            org.from_json(INVALID_JSON_VALUES)

        # Test the _reset function
        with self.assertRaises(ValueError):
            org.name
        with self.assertRaises(ValueError):
            org.id
        assert org.description is None
        assert org.updated == 0.0
        assert org.created == 0.0
        assert org.active == True
        assert len(org.links) == 0


if __name__ == "__main__":
    unittest.main()

