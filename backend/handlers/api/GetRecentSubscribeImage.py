import json
import webapp2
from domain.Stream import Stream
from domain.Subscribe import Subscribe

class GetRecentSubscribeImage(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        streams = Stream.query()
        sub_stream = Subscribe.query_by_user(user_id)
        sub_stream_ids = [obj.stream for obj in sub_stream.iter()] #list of stream IDs

        #iterate through streams and get last image
        recentImages = []
        streamName = []
        streamIDs = []
        for stream_id in sub_stream_ids:
            stream = Stream.query_by_id(int(stream_id))
            if len(stream.photos) != 0:
                recentImages.append(stream.photos[-1])
                streamName.append(stream.name)
                streamIDs.append(stream_id)

        self.response.write(json.dumps({"recentImages": recentImages, "streamName": streamName,
                                        "id": streamIDs}))
