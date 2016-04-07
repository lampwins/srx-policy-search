import re
from Policy import Policy
from Address import Address
from AddressGroup import AddressGroup
from ServiceGroup import ServiceGroup
from Service import Service
from Configuration import Configuration
import getpass


#client = paramiko.SSHClient()
#client.load_system_host_keys()
#client.set_missing_host_key_policy(paramiko.WarningPolicy())
#client.connect("192.168.187.5", username="nuandersonjd", password="John199527_")
#stdin, stdout, stderr = client.exec_command('show configuration security address-book | display set | match 153.9.252.0')

address_objects = []
search_objects = []
policy_names = []
policies = []

host = raw_input("Host: ")
user = raw_input("Username: ")
password = getpass.getpass()

config = Configuration(host, user, password)

print "Config retrieved"
search = raw_input("IP Address to search: ")

print "Searching..."

for line in config.get_filtered_lines("address", [search], []):
    line = line.strip('\n')
    line = line.rstrip()
    m = re.search('address (.+?) ', line)
    if m:
        address_objects.append(m.group(1))
        search_objects.append(m.group(1))

for a in address_objects:
    #stdin, stdout, stderr = client.exec_command(
    #    'show configuration security address-book | display set | match ' + a + ' | except "global address  "')
    for line in config.get_filtered_lines("address", [a], ["global address  "]):
        line = line.strip('\n')
        line = line.rstrip()
        m = re.search('address-set (.+?) ', line)
        if m:
            search_objects.append(m.group(1))

for s in search_objects:
    #stdin, stdout, stderr = client.exec_command(
    #    'show configuration security policies | display set | match ' + s)
    for line in config.get_filtered_lines("policy", [s], []):
        line = line.strip('\n')
        line = line.rstrip()
        m = re.search('policy (.+?) ', line)
        if m and m.group(1) not in policy_names:
            policy_names.append(m.group(1))

#print "Found these polices:"
#for p in policy_names:
    #print p


def get_address(address):
    for p in policies:
        if p.get_address(address):
            return p.get_address(address)
    return False


def get_generic_service(lines):
    sprotocol = "N/A"
    sdestination_port = "0"
    for service_line in lines:
        service_line = service_line.strip('\n')
        service_line = service_line.rstrip()
        if " protocol " in service_line:
            sprotocol = re.search('protocol (.*)', service_line)
            sprotocol = sprotocol.group(1)
        elif " destination-port " in service_line:
            sdestination_port = re.search('destination-port (.*)', service_line)
            sdestination_port = sdestination_port.group(1)
    return sprotocol, sdestination_port


def get_junos_default_service(service):
    #stdin, stdout, stderr = client.exec_command(
    #    'show configuration groups junos-defaults applications | display set | match "' + service + ' "')
    return get_generic_service(config.get_filtered_lines("junos-service", [service + " "], []))


for p in policy_names:
    # stdin, stdout, stderr = client.exec_command(
    #    'show configuration security policies | display set | match "policy ' + p + ' "')
    src = []
    dest = []
    services = []
    action = None
    description = None
    src_zone = None
    dest_zone = None

    #print "searching policy " + p

    for policy_line in config.get_filtered_lines("policy", ["policy " + p + " "], []):
        policy_line = policy_line.strip('\n')
        policy_line = policy_line.rstrip()
        for address_type in ["source-address", "destination-address"]:
            if address_type in policy_line:
                target_address = re.search(address_type + ' (.*)', policy_line)
                if target_address:
                    target_address = target_address.group(1)
    
                    if target_address == "any":
                        src.append(Address("any", "any", "any"))
                        continue  # "any" address, move on
    
                    #stdin, stdout, stderr = client.exec_command(
                    #    'show configuration security address-book | display set | except "description|address-set" | match ' + target_address)
    
                    #print "\tfound " + address_type + " " + target_address
    
                    stdout = config.get_filtered_lines("address", [target_address], ["description", "address-set"])
                    if len(stdout) != 0:
    
                        # single address
    
                        target_address_line = stdout[0]
                        target_address_line = target_address_line.strip('\n')
                        target_address_line = target_address_line.rstrip()
    
                        #print "\t\tsingle address"
    
                        if "dns-name" in target_address_line:
                            atype = "dns"
                            target_address_value_search = re.search('address ' + target_address + ' dns-name (.*)',
                                                                    target_address_line)
                        else:
                            atype = "ipv4"
                            target_address_value_search = re.search('address ' + target_address + ' (.*)',
                                                                    target_address_line)
    
                        target_address_value = target_address_value_search.group(1)
                        if address_type == "source-address":
                            src.append(Address(target_address, atype, target_address_value))
                        else:
                            dest.append(Address(target_address, atype, target_address_value))
    
                        #print "\t\ttype " + atype
                        #print "\t\tvalue " + target_address_value
    
                        ##
    
                    else:
                        #group
    
                        #print "\t\tgroup object"
    
                        group = AddressGroup(target_address)
    
                        #stdin, stdout, stderr = client.exec_command(
                        #    'show configuration security address-book global | display set | except "description" | match address-set | match ' + target_address)
    
                        #print "\t\tsearching address-book for " + target_address
    
                        for group_target_address_line in config.get_filtered_lines("address", ["address-set", target_address], ["description"]):
                            group_target_address_line = group_target_address_line.strip('\n')
                            group_target_address_line = group_target_address_line.rstrip()

                            #print group_target_address_line
                            #exit()
    
                            group_target_address = re.search(' address (.*)', group_target_address_line)
                            group_target_address = group_target_address.group(1)
                            #stdin, stdout, stderr = client.exec_command(
                            #    'show configuration security address-book | display set | except "description|address-set" | match ' + group_target_address)
                            for group_target_address_actual_line in config.get_filtered_lines("address", [group_target_address], ["description", "address-set"]):
                                group_target_address_actual_line = group_target_address_actual_line.strip('\n')
                                group_target_address_actual_line = group_target_address_actual_line.rstrip()
                                if "global address " in group_target_address_actual_line:
                                    # single address
    
                                    if "dns-name" in group_target_address_actual_line:
                                        atype = "dns"
                                        target_address_value_search = re.search(
                                            'address ' + group_target_address + ' dns-name (.*)',
                                            group_target_address_actual_line)
                                    else:
                                        atype = "ipv4"
                                        target_address_value_search = re.search('address ' + group_target_address + ' (.*)',
                                                                                group_target_address_actual_line)
    
                                    target_address_value = target_address_value_search.group(1)
                                    group.add_address(
                                        Address(group_target_address, atype, target_address_value))
    
                                    #print "\t\tfound " + address_type + " " + group_target_address
                                    #print "\t\t\ttype " + atype
                                    #print "\t\t\tvalue " + target_address_value

                        if address_type == "source-address":
                            src.append(group)
                        else:
                            dest.append(group)
        #  services
        if "match application " in policy_line:
            service = re.search('match application (.*)', policy_line)
            service = service.group(1)
            protocol = None
            destination_port = None
            service_objcet = None

            if service == "any":
                service_objcet = Service("any", "any", "any")
            elif "junos-" in service:
                protocol, destination_port = get_junos_default_service(service)
                service_objcet = Service(service, protocol, destination_port)
            else:
                #stdin, stdout, stderr = client.exec_command(
                #    'show configuration applications application-set ' + service + ' | display set')
                stdout = config.get_filtered_lines("service", ["application-set", service], ["description"])
                if len(stdout) != 0:
                    #  services in the set
                    service_objcet = ServiceGroup(service)
                    for service_set_line in stdout:
                        service_set_line = service_set_line.strip('\n')
                        service_set_line = service_set_line.rstrip()
                        if " application " in service_set_line:
                            service_set_service = re.search('application (.*)', service_set_line)
                            service_set_service = service_set_service.group(1)
                            #stdin, stdout, stderr = client.exec_command(
                            #    'show configuration applications application' + service_set_service + ' | display set')
                            stdout = config.get_filtered_lines("service", [service_set_service], ["application-set", "description"])
                            if " term " not in service_set_line[0]:
                                #  found the actual service
                                protocol, destination_port = get_generic_service(stdout)
                                service_objcet.add_service(Service(service_set_service, protocol, destination_port))
                            else:
                                #  termed service object
                                terms = set()
                                for lines in stdout:
                                    group_term = re.search(' term (.+?) ', service_set_line)
                                    group_term = group_term.group(1)
                                    terms.add(group_term)
                                for term in terms:
                                    protocol, destination_port = get_generic_service(config.get_filtered_lines("service", [service_set_service, term], ["application-set", "description"]))
                                    service_objcet.add_service(Service(term, protocol, destination_port))

                else:
                    #  regular service
                    #stdin, stdout, stderr = client.exec_command(
                    #    'show configuration applications application' + service + ' | display set')
                    protocol, destination_port = get_generic_service(config.get_filtered_lines("service", [service], ["application-set", "description"]))
                    service_objcet = Service(service, protocol, destination_port)

            services.append(service_objcet)

        #  action
        if action is None:
            if " then " in policy_line and " log " not in policy_line:
                action = re.search('then (.+?) ', policy_line)
                action = action.group(1)
        #  description
        if " description " in policy_line:
            description = re.search('description (.*)', policy_line)
            description = description.group(1)
            description = description.rstrip('"')
        # zones
        if src_zone is None:
            src_zone = re.search('from-zone (.+?) ', policy_line)
            src_zone = src_zone.group(1)
        if dest_zone is None:
            dest_zone = re.search('to-zone (.+?) ', policy_line)
            dest_zone = dest_zone.group(1)

    if description is None:
        description = ""
    policies.append(Policy(p, description, src, dest, action, services, src_zone, dest_zone))

print "\nPolicies Matching :\n\n"
for p in policies:
    print p
    print
