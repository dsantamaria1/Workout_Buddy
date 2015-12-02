from google.appengine.ext import ndb

class Exercise(ndb.Model):
    name = ndb.StringProperty();
    photos = ndb.IntegerProperty(repeated=True)
