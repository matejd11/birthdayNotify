import os
from personDb import PersonDb
from groupDb import GroupDb


class FakeDb(object):
    def __init__(self, dbName, autoload = True):
        self.dbName = dbName
        self.setDbNames(dbName)
        self.personDb = PersonDb(self.personDbName, autoload)
        self.grouDb = GroupDb(self.groupDbName, autoload)
        if autoload:
            self.setup()

    def setup(self):
        self.db = self.load(self.dbName)

    def save(self, fileName = None):
        if fileName == None:
            fileName = self.personDbName
        self.setDbNames(fileName)
#change to _save
        self.personDb.save(self.personDbName)
        self.grouDb.save(self.groupDbName)

    def load(self, fileName = None):
        if fileName == None:
            fileName = self.dbName
        self.setDbNames(fileName)
#change to _save
        self.personDb.load(self.personDbName)
        self.grouDb.load(self.groupDbName)

    def setDbNames(self, dbName):
        self.personDbName = FakeDb.fileExtension(dbName + ".p")
        self.groupDbName = FakeDb.fileExtension(dbName + ".g")

    def fileExtension(fileName):
        result = fileName.strip()
        if '.db' not in result:
            result += '.db'
        return result

