import json

import webapp2
from domain.Photo import Photo
from domain.Stream import Stream

class GetAllPhotos(webapp2.RequestHandler):
    def get(self):
        PhotoDistances = []
        streams = Stream.query()
        for stream in streams:
            for photo in stream.photos:
                p = Photo.query_by_id(photo)
                PhotoDistances.append({"lat":p.Latitude, "lng": p.Longitude, "stream_id":p.stream_id,
                                       "photo_id": photo, "stream_name": stream.name})

        self.response.write(json.dumps({"Distances": PhotoDistances}))
