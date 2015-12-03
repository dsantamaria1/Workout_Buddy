import json

import webapp2
from domain.Stream import Stream
from domain.Subscribe import Subscribe

class UserManagement(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        own_stream = Stream.query_by_author(user_id)
        own_stream_ids = [obj.key.id() for obj in own_stream.iter()]

        sub_stream = Subscribe.query_by_user(user_id)
        sub_stream_ids = [obj.stream for obj in sub_stream.iter()]
        r = {'own_stream': own_stream_ids, 'sub_stream': sub_stream_ids}
        self.response.write(json.dumps(r))
        #return r
