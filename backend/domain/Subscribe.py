from google.appengine.ext import ndb
from Stream import Stream

class Subscribe(ndb.Model): #contains streams the user is Subscribed to
    user = ndb.StringProperty()
    stream = ndb.StringProperty() #stream_id

    @classmethod
    def query_by_user(cls, user_key):
        return Subscribe.query(Subscribe.user == str(user_key))

    @classmethod
    def subscribed(cls, stream_id, user_id):
        sub = Subscribe.query(ndb.AND(Subscribe.user==str(user_id), Subscribe.stream==str(stream_id)))
        return len(sub.fetch())>0

    @classmethod
    def delete_subscribe(cls, stream_ids, user_id):
      subscribes = cls.query_by_user(user_id)
      todelete = [sub.key for sub in subscribes.iter() if int(sub.stream) in stream_ids]
      ndb.delete_multi(todelete)
