class ServiceGroup(object):

    def __init__(self, name):
        self.name = name
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    def get(self, instance):
        if self.name == instance:
            return self

        for s in self.services:
            if s.get(instance):
                return s.get(instance)

        return False

    def __str__(self):
        str = "Group: " + self.name + "\n"
        for s in self.services:
            str += "\t\t\t" + s + "\n"

        return str.rstrip("\n")

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
