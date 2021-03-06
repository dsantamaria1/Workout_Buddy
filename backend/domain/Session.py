from google.appengine.ext import ndb

class Session(ndb.Model):
    category = ndb.StringProperty()
    exercises = ndb.StringProperty(repeated=True)
    reps = ndb.StringProperty()
    currWO = ndb.IntegerProperty()
    step = ndb.IntegerProperty()
    active = ndb.BooleanProperty()
    totalWOs = ndb.IntegerProperty()
    completed = ndb.BooleanProperty()
    started = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_by_id(cls, key):
        return cls.get_by_id(key)
