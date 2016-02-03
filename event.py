class Event(object):
    order = ["name",
             "shortcut"]

    def __init__(self, name, shortcut):
        self.name = name
        self.shortcut = shortcut
