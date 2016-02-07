import os
from personDb import PersonDb
from groupDb import GroupDb
from eventDb import EventDb
from messagesDb import MessagesDb


class FakeDb(object):
    def __init__(self, dbName, autoload = True):
        self.dbName = dbName
        self.setDbNames(dbName)
        self.personDb = PersonDb(self.personDbName, autoload)
        self.groupDb = GroupDb(self.groupDbName, autoload)
        self.eventDb = EventDb(self.eventDbName, autoload)
        self.messagesDb = MessagesDb(self.messagesDbName, autoload)
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
        self.messagesDb.save(self.messagesDbName)

    def load(self, fileName = None):
        if fileName == None:
            fileName = self.dbName
        self.setDbNames(fileName)
#change to _save
        self.personDb.load(self.personDbName)
        self.groupDb.load(self.groupDbName)
        self.eventDb.load(self.eventDbName)
        self.messagesDb.load(self.messagesDbName)

    def setDbNames(self, dbName):
        self.personDbName = FakeDb.fileExtension(dbName + ".p")
        self.groupDbName = FakeDb.fileExtension(dbName + ".g")
        self.eventDbName = FakeDb.fileExtension(dbName + ".e")
        self.messagesDbName = FakeDb.fileExtension(dbName + ".m")

    def fileExtension(fileName):
        result = fileName.strip()
        if '.db' not in result:
            result += '.db'
        return result
