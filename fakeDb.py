import os
from personDb import PersonDb
from groupDb import GroupDb


class FakeDb(object):
    def __init__(self, dbName):
        self.setDbNames(dbName)
        self.personDb = PersonDb(self.personDbName, False)
        self.grouDb = GroupDb(self.groupDbName, False)

    def save(self, fileName = None):
        if fileName == None:
            fileName = self.personDbName
#change to _save
        self.personDb.save(fileName) 
        self.grouDb.save(fileName) 

    def load(self, fileName = None):
        if fileName == None:
            fileName = self.groupDbName
#change to _save
        self.personDb.load(fileName)
        self.grouDb.load(fileName)

    def fileExtension(fileName):
        result = fileName.strip()
        if '.db' not in result:
            result += '.db'
        return result

    def setDbNames(self, dbName):
        self.personDbName = FakeDb.fileExtension(dbName + ".p")
        self.groupDbName = FakeDb.fileExtension(dbName + ".g")

