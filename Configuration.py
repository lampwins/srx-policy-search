import paramiko


class Configuration(object):

    client = paramiko.SSHClient()

    def __init__(self, host, username, password):

        print "Retrieving config..."

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.client.connect(host, username=username, password=password)
        self.client.load_system_host_keys()

        stdin, stdout, stderr = self.client.exec_command(
            'show configuration security policies | display set | no-more')

        self.policy = stdout.readlines()

        stdin, stdout, stderr = self.client.exec_command(
            'show configuration security address-book global | display set | no-more')

        self.address_book = stdout.readlines()

        stdin, stdout, stderr = self.client.exec_command(
            'show configuration groups junos-defaults applications | display set | no-more')

        self.junos_services = stdout.readlines()

        stdin, stdout, stderr = self.client.exec_command(
            'show configuration applications | display set | no-more')

        self.services = stdout.readlines()

        self.client.close()

    def get_lines(self, section, match_terms, except_terms):

        return [x for x in section if all(m in x for m in match_terms) and not any(e in x for e in except_terms)]

    def get_filtered_lines(self, section, match_terms, except_terms):

        if section == "policy":
            return self.get_lines(self.policy, match_terms, except_terms)
        elif section == "address":
            return self.get_lines(self.address_book, match_terms, except_terms)
        elif section == "service":
            return self.get_lines(self.services, match_terms, except_terms)
        elif section == "junos-service":
            return self.get_lines(self.junos_services, match_terms, except_terms)
        else:
            return []
