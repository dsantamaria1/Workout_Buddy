import json
import webapp2
from domain.Stream import Stream

class AllStreams(webapp2.RequestHandler):
    def get(self):
        streams = Stream.query()
        all_streams = []
        for s in streams:
            all_streams.append({'name':s.name, 'cover':s.cover, 'id':s.key.id(), 'views':s.views})
        self.response.write(json.dumps({"allstreams": all_streams}))
