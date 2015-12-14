from google.appengine.ext import ndb

class Run(ndb.Model):
    time = ndb.FloatProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_by_id(cls, key):
        return cls.get_by_id(key)
