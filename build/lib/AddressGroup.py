class AddressGroup(object):

    def __init__(self, name):
        self.address = []
        self.name = name

    def add_address(self, address):
        self.address.append(address)

    def get(self, instance):
        if self.name == instance:
            return self

        for a in self.address:
            if a.get(instance):
                return a.get(instance)

        return False

    def __str__(self):
        str = "Group: " + self.name + "\n"
        for a in self.address:
            str += "\t\t\t" + a + "\n"

        return str.rstrip("\n")

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
