class Address(object):
    def __init__(self, name, atype, value):
        self.name = name
        self.type = atype
        self.value = value

    def get(self, instance):
        if self.name == instance:
            return self
        else:
            return False

    def __str__(self):
        return self.name + " - " + self.type + " - " + self.value

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
