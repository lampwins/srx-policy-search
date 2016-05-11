class Policy:
    def __init__(self, name, description, src, dest, action, services, src_zone, dest_zone):
        self.name = name
        self.description = description
        self.src = src
        self.dest = dest
        self.action = action
        self.services = services
        self.src_zone = src_zone
        self.dest_zone = dest_zone

    def get_address(self, address):
        for s in self.src:
            if s.get(address):
                return s.get(address)
        for d in self.dest:
            if d.get(address):
                return d.get(address)
        return False

    def get_service(self, service):
        for s in self.services:
            if s.get(service):
                return s.get(service)
        return False

    def __str__(self):
        str = self.name + ":\n"
        str += "\tsrc zone: " + self.src_zone + "\n"
        str += "\tsrc ip's:\n"
        for a in self.src:
            str += "\t\t" + a + "\n"
        str += "\tdest zone: " + self.dest_zone + "\n"
        str += "\tdest ip's:\n"
        for a in self.dest:
            str += "\t\t" + a + "\n"
        str += "\tservices:\n"
        for s in self.services:
            str += "\t\t" + s + "\n"
        str += "\taction: " + self.action + "\n"
        str += "\tdescription: \"" + self.description + "\""

        return str
