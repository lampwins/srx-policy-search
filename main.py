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

    print "[1] IP"
    search_type = raw_input("Choose Search Type: ")

    if search_type == "1":

        print "Usage: Enter a single IP address or CIDR notation (/32 is assumed) to search or 'exit' to quit. " \
                  "Surround in quotes to search explicitly, otherwise match containing subnets."
        search = raw_input("Search: ")
        if search == "exit":
            exit(1)

        print "Searching..."

        polices = searcher.search_by_ip(search)

    print "\nPolicies Matching " + search + ":\n\n"
    for p in polices:
        print p
        print
