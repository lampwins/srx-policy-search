# SRX Policy Search

This is a simple Python script that searches a Juniper SRX policy for references to a provided search term.
You can search policies by either IP address, service, or action.

####Setup
You will need to connect to a device and retrieve its configuration. Then you need a search object.
```
config = Configuration('192.168.1.1', 'username', 'password')
searcher = Search(config)
```
Now you can begin searching. All search methods return a list of `Policy` objects or an empty list is there
are no matches.

####IP Address
IP address searches can be either explicit or by default include
policies that reference containing subnets. You may also search by CIDR notation.
```
policies = searcher.search_by_ip('10.0.0.1')  # includes subnets like 10.0.0.0/8
policies = searcher.search_by_ip('192.168.0.0/24')  # CIDR - includes subnets
policies = searcher.search_by_ip('"172.16.1.1"')  # Explicit - assumes /32
policies = searcher.search_by_ip('"172.24.1.0/24"')  # Explicit CIDR
```
The `Policy` class has a `__str__` method so a simple two liner can print all your policies.


####Service
Service based searches ask for a destination protocol and port and currently only support UDP and TCP searches.
```
policies = searcher.search_by_service('tcp', '443')
```

####Action
Action based searches ask for one of the three standard SRX policy actions to match on.
```
policies = searcher.search_by_action('deny')  # permit, deny, and reject
```

####Further Use

The polices are normalized into a simple `Policy` data model which could be used to translate into another system.

Also included is a basic CLI in `main.py` which makes used of everything mentioned above.
```
[0] Exit/Quit
[1] IP
[2] Service
[3] Action
Choose Search Type:
```