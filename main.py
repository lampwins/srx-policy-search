import getpass

from srxpolicysearch.Search import Search

from srxpolicysearch.Configuration import Configuration

host = raw_input("Host: ")
user = raw_input("Username: ")
password = getpass.getpass()

config = Configuration(host, user, password)
searcher = Search(config)
print "Config retrieved\n"

while True:

    policies = []
    search = None

    print "[0] Exit/Quit"
    print "[1] IP"
    print "[2] Service"
    print "[3] Action"
    print "[4] Policy name"
    print "[5] List all policies"
    search_type = raw_input("Choose Search Type: ")
    print

    if search_type == "0":
        print "Bye."
        exit(1)

    elif search_type == "1":
        print "Usage: Enter a single IP address or CIDR notation (/32 is assumed) to search." \
                  "Surround in quotes to search explicitly, otherwise match containing subnets."
        search = raw_input("IP to search: ")
        print "\nSearching...\n"
        policies = searcher.search_by_ip(search)

    elif search_type == "2":
        print "Usage: Enter protocol and destination port to search"
        protocol = raw_input("Protocol (tcp, udp): ")
        if protocol not in ["tcp", "udp"]:
            print "Protocol not valid."
            search = None
        else:
            port = raw_input("Port (80, 5000-5002): ")
            search = protocol + "/" + port
            print "\nSearching...\n"
            policies = searcher.search_by_service(protocol, port)

    elif search_type == "3":
        print "Usage: Enter policy action to search"
        search = raw_input("Action (permit, deny, reject): ")
        if search not in ["permit", "deny", "reject"]:
            print "Action is not valid.\n"
            search = None
        else:
            print "\nSearching...\n"
            policies = searcher.search_by_action(search)

    elif search_type == "4":
        print "Usage: Enter policy name"
        search = raw_input("Name: ")
        print "\nSearching...\n"
        policies = searcher.search_by_name(search)

    elif search_type == "5":
        print "\nSearching...\n"
        policies = searcher.search_by_all()

    if search is not None:
        print "\nPolicies Matching " + search + ":\n\n"
        for p in policies:
            print p
            print
