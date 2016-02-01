import os
from personDb import PersonDb
from groupDb import GroupDb


class FakeDb(object):
    def __init__(self, dbName):
        self.dbName = self.fileExtension(dbName)
        self.personDb = PersonDb(self.dbName, False)
        self.grouDb = GrouDb(self.dbName, False)

    def save(self, fileName = 'database'):
        self.personDb.save(fileName) 
        self.grouDb.save(fileName) 

    def load(self, fileName = 'database'):

    def fileExtension(fileName):
        result = fileName.strip()
        if '.json' not in result:
            result += '.json'
        return result
