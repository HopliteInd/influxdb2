Simple Examples
===============

.. contents:: API Examples

Orgs API
--------

.. code-block:: python

    import influxdb2

    influxdb_url = "https://example.com:8086/"
    influxdb_auth_token = "1234567890abcdef"
    influx = influxdb2.connect(influxdb_url, influxdb_auth_token)


    # Iterate through all orgs
    for org in influx.orgs.iterate():
        print(org.name)

