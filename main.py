from Search import Search
from Configuration import Configuration
import getpass


host = raw_input("Host: ")
user = raw_input("Username: ")
password = getpass.getpass()

config = Configuration(host, user, password)
searcher = Search(config)
print "Config retrieved\n"

while True:

    polices = []
    search = None

    print "[0] Exit/Quit"
    print "[1] IP"
    print "[2] Service"
    search_type = raw_input("Choose Search Type: ")
    print

    if search_type == "1":
        print "Usage: Enter a single IP address or CIDR notation (/32 is assumed) to search." \
                  "Surround in quotes to search explicitly, otherwise match containing subnets."
        search = raw_input("IP to search: ")
        polices = searcher.search_by_ip(search)

    elif search_type == "2":
        print "Usage: Enter protocol and destination port to search"
        protocol = raw_input("Protocol (tcp, udp): ")
        port = raw_input("Port (80, 5000-5002): ")
        search = protocol + "/" + port
        polices = searcher.search_by_service(protocol, port)

    print "\nSearching...\n"

    print "\nPolicies Matching " + search + ":\n\n"
    for p in polices:
        print p
        print
