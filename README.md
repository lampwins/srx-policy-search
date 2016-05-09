# srx-policy-search

This is a simple Python script that searches a Juniper SRX policy for references to a provided IP address.
It returns all polices (in their entirety) for which the ip address is a part of. This accounts for cases in which
the IP is the subject of more than more address object or is a member of an address group (address-set).