import pymongo

class mdb(object):
    
    def __init__(self, db, collection):
        self.host = "127.0.0.1"
        self.port = 27017
        self.db = db
        self.collection = collection
        
    def con(self):
        return pymongo.MongoClient(self.host, self.port)
    
    def db(self, db):
        self.db = db
        
    def collection(self, collection):
        self.collection = collection
    
    def perform(self):
        return self.con()[self.db][self.collection]
        