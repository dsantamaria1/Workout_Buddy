from google.appengine.ext import ndb

class Session(ndb.Model):
    category = ndb.StringProperty()
    exercises = ndb.StringProperty(repeated=True)
    reps = ndb.StringProperty()
    currWO = ndb.IntegerProperty()
    step = ndb.IntegerProperty()
    active = ndb.BooleanPreperty()
