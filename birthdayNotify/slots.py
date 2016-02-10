import json


class Slot(object):
    def __init__(self, name, listOfPeople = None):
        if listOfPeople == None:
            listOfPeople = []
        self.listOfPeople = listOfPeople
        self.name = name

    def convert(self):
        dictionary = (self.__dict__).copy()
        return dictionary

    def __str__(self):
        me = self.convert()
        return str(json.dumps(me, sort_keys = True, indent = 4))

