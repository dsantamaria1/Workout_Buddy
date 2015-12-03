from google.appengine.ext import ndb
from google.appengine.api import users

class Stream(ndb.Model):
    name = ndb.StringProperty()
    author = ndb.StringProperty()
    email = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    photos = ndb.IntegerProperty(repeated=True)
    cover = ndb.StringProperty()
    views = ndb.IntegerProperty()
    updated_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_by_author(cls, author_key):
        return Stream.query(Stream.author == author_key)

    @classmethod
    def query_by_id(cls, stream_id):
        return cls.get_by_id(stream_id)

    #search by string in "name" and in "tags"
    @classmethod
    def query_by_name(cls, text):
      r = []
      if len(text.strip()) == 0:
          return r
      for stream in Stream.query():
        if text.lower() in stream.name.lower():
          r.append(stream)
        if (text.lower() in stream.email.lower()) and (stream.email not in r):
            r.append(stream)
        else:
            for tag in stream.tags:
                if text.lower() in tag.lower():
                    r.append(stream)
                    break
      return r

    @classmethod
    def name_exist(cls, text):
        if len(text.strip()) == 0:
            return False
        for stream in Stream.query():
            if text.lower() == stream.name.lower():
                return True
        return False

    @classmethod
    def delete_streams(cls, stream_ids):
      streams = [cls.query_by_id(p).key for p in stream_ids]
      ndb.delete_multi(streams)
