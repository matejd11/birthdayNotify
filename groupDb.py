import pickle
import os


class GroupDb(object):
    def __init__(self, dbName, autoload = False):
        self.dbName = dbName
        self.db = None
        self.isChanged = False
        if autoload:
            self.setup()

    def setup(self):
        self.db = self.load(self.dbName)

    def add(self, group):
        self.isChanged = True
        self.db.append(group)

    def edit(self, group, newGroup):
        self.isChanged = True
        self.db.index(group)
        self.db[index] = newGroup

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

