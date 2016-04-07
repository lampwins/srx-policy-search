class Service(object):
    def __init__(self, name, protocol, port):
        self.name = name
        self.protocol = protocol
        self.port = port

    def get(self, instance):
        if self.name == instance:
            return self
        else:
            return False

    def __str__(self):
        return self.name + " - " + self.protocol + " - " + self.port

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
