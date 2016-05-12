# SRX Policy Search

This is a simple Python script that searches a Juniper SRX policy for references to a provided search term.
You can search policies by either IP address or service.

IP address searches can be either explicit or by default include
policies that reference containing subnets. You may also search by CIDR notation.

Service based searches ask for a destination protocol and port and currently only support UDP and TCP searches.

The polices are normalized into a simple data model which could be used to translate into another system.

Also included is a basic CLI in `main.py` with which you can interact.