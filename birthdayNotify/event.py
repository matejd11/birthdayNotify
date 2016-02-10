import json


class Event(object):
    header = ["name",
              "shortcut"]
    order = ["name",
             "shortcut"]

    def showTable(dataEvent):
        order = Event.order[:]
        header = Event.header[:]

        content = []
        for event in dataEvent.db:
            content.append(event.__dict__)

        return header, content, order

    def __init__(self, name, shortcut):
        self.name = name
        self.shortcut = shortcut

    def __str__(self):
        me = self.__dict__
        return str(json.dumps(me, sort_keys=True, indent=4))
