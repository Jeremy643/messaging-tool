class Person:

    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.name = None
    
    def set_name(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.client}, {self.address})'