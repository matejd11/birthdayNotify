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
        self.db = self.load(self.dbName)

    def add(self, person):
        self.isChanged = True
        self.db.append(person)

    def remove(self, index):
        self.isChanged = True
        self.db.pop(index)

    def edit(self, index, newPerson):
        self.isChanged = True
        self.db[index] = newPerson

    def save(self, fileName = None):
        if fileName == None:
            fileName = self.dbName
        with open(fileName,"wb") as pickleOut:
            pickle.dump(self.db, pickleOut)
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

