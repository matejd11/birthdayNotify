import json


class Event(object):
    order = ["name",
            "shortcut"]

    def __init__(self, name, shortcut):
        self.name = name
        self.shortcut = shortcut

    def __str__(self):
        me = self.__dict__
        return str(json.dumps(me, sort_keys = True, indent = 4))

