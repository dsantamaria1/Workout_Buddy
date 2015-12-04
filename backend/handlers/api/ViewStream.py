import json
from random import randint

import webapp2
from domain.Stream import Stream

'''
which takes a stream id and a page range and returns a list of URLs to images, and a page range)
'''
class ViewStream(webapp2.RequestHandler):
    def get(self):
        #stream_id, st, ed
        stream_id = int(self.request.get('stream_id'))
        if self.request.get('st'):
            st = int(self.request.get('st'))
        else:
            st = 1
        stream = Stream.query_by_id(int(stream_id))
        stream.views = stream.views + 1
        stream.put()
        length = len(stream.photos)
        st = min(max(st, 1), length)
        ed = min(st + 3, length + 1)
        images = stream.photos[-st:-ed:-1]

        woPics=stream.woPics
        woInstructions=stream.woInstructions
        if self.request.get('all'):
            images = stream.photos[:]
        if ed == length + 1:
            ed = -1

        LatLngBounds = {
            'minLat': -85,
            'maxLat': 85,
            'minLng': -180,
            'maxLng': 180,
        }

        locations = [{
            'lat': randint(LatLngBounds['minLat'], LatLngBounds['maxLat']),
            'lng': randint(LatLngBounds['minLng'], LatLngBounds['maxLat']),
        } for i in range(len(images))]

        self.response.write(json.dumps({
            'images': images,
            'locations': locations,
            'st': st,
            'ed': ed,
            'size': length,
            'woPics': woPics,
            'woInstructions': woInstructions,
        }))
