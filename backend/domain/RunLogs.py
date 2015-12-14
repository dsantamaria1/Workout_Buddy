from google.appengine.ext import ndb

class RunLogs(ndb.Model):
    RunHistory = ndb.IntegerProperty(repeated=True)
    #owner = ndb.StringProperty()

    @classmethod
    def query_by_id(cls, key):
        return cls.get_by_id(key)
