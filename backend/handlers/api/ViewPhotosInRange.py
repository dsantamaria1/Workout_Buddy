import json
import datetime
import time
from random import randint

import webapp2
from domain.Stream import Stream
from domain.Photo import Photo

'''
which takes a stream id and a time range and returns a list of images that are added in that time range
'''
class ViewPhotosInRange(webapp2.RequestHandler):
    def get(self):
        #stream_id, start_time, end_time
        stream_id = int(self.request.get('stream_id'))
        start_time = self.request.get('start_time')
        end_time = self.request.get('end_time')
        stream = Stream.query_by_id(int(stream_id))
        stream.views = stream.views + 1
        stream.put()

        images = []
        LatLngBounds = {
            'minLat': -85,
            'maxLat': 85,
            'minLng': -180,
            'maxLng': 180,
        }

        start_time = datetime.datetime.strptime(start_time, "%b %d %Y")
        end_time = datetime.datetime.strptime(end_time, "%b %d %Y") + datetime.timedelta(days=1, hours=12)
        print start_time, end_time
        for photo_id in stream.photos:
            photo = Photo.get_by_id(photo_id)
            if photo.updated_time >= start_time and photo.updated_time <= end_time:
                images.append({
                    'image': photo_id,
                    'updated_time': photo.updated_time.isoformat(),
                    'lat': randint(LatLngBounds['minLat'], LatLngBounds['maxLat']),
                    'lng': randint(LatLngBounds['minLng'], LatLngBounds['maxLat']),
                })
        self.response.write(json.dumps({
            'images': images,
            'status': 0,
        }))
