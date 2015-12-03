from google.appengine.ext import ndb

class Photo(ndb.Model):
    stream_id = ndb.StringProperty()
    comment = ndb.StringProperty()
    image = ndb.BlobProperty()
    updated_time = ndb.DateTimeProperty(auto_now_add=True)
    Latitude = ndb.FloatProperty()
    Longitude = ndb.FloatProperty()

    @classmethod
    def query_by_id(cls, photo_id):
        return cls.get_by_id(photo_id)
