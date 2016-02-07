import os
from birthdayNotify.personDb import PersonDb
from birthdayNotify.groupDb import GroupDb
from birthdayNotify.eventDb import EventDb


class FakeDb(object):
    def __init__(self, dbName, autoload = True):
        self.dbName = dbName
        self.setDbNames(dbName)
        self.personDb = PersonDb(self.personDbName, autoload)
        self.groupDb = GroupDb(self.groupDbName, autoload)
        self.eventDb = EventDb(self.eventDbName, autoload)
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
        self.groupDb.save(self.groupDbName)
        self.eventDb.save(self.eventDbName)

    def load(self, fileName = None):
        if fileName == None:
            fileName = self.dbName
        self.setDbNames(fileName)
#change to _save
        self.personDb.load(self.personDbName)
        self.groupDb.load(self.groupDbName)
        self.eventDb.load(self.eventDbName)

    def setDbNames(self, dbName):
        self.personDbName = FakeDb.fileExtension(dbName + ".p")
        self.groupDbName = FakeDb.fileExtension(dbName + ".g")
        self.eventDbName = FakeDb.fileExtension(dbName + ".e")

    def fileExtension(fileName):
        result = fileName.strip()
        if '.db' not in result:
            result += '.db'
        return result

