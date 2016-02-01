import pickle
import os


class PersonDb(object):
    def __init__(self, dbName, autoload = True):
        self.dbName = dbName
        self.db = None
        self.isChanged = False
        if autoload:
            self.setup()

    def setup(self):
        self.db = PersonDb.load(self.dbName)
        self.getGroups()

    def getGroups(self):
        tmp = set()
        for person in self.db:
            for group in person.group:
                tmp.add(person)
        self.groups = tmp

    def add(self, person):
        self.isChanged = True
        self.db.append(person)

    def edit(self, person, newPerson):
        self.isChanged = True
        self.db.index(person)
        self.db[index] = newPerson

    def save(self, data, fileName = None):
        if fileName == None:
            fileName = self.dbName
        with open(fileName,"wb") as pickleOut:
            pickle.dump(data, pickleOut)
            self.dbName = fileName
            self.isChanged = False

    def load(self, fileName = None):
        if fileName == None:
            fileName = self.dbName
        self.dbName = fileName
        self.isChanged = False
        try:
            with open(fileName, "rb") as pickleIn:
                data = pickle.load(pickleIn)
            return data
        except FileNotFoundError:
            return []

