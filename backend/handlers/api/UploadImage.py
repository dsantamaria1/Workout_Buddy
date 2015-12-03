import json

import webapp2
import urllib
import re
import time, datetime

from google.appengine.api import images, memcache
from google.appengine.ext import ndb
from domain.Stream import Stream
from domain.Photo import Photo
from threading import Lock

mutex = Lock()

MIN_FILE_SIZE = 1  # bytes
# Max file size is memcache limit (1MB) minus key size minus overhead:
MAX_FILE_SIZE = 999000  # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMB_MAX_WIDTH = 80
THUMB_MAX_HEIGHT = 80
THUMB_SUFFIX = '.'+str(THUMB_MAX_WIDTH)+'x'+str(THUMB_MAX_HEIGHT)+'.png'
EXPIRATION_TIME = 300  # seconds

class UploadImage(webapp2.RequestHandler):
    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'File is too small'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'Filetype not allowed'
        else:
            return True
        return False

    def get_file_size(self, file):
        file.seek(0, 2)  # Seek to the end of the file
        size = file.tell()  # Get the position of EOF
        file.seek(0)  # Reset the file position to the beginning
        return size

    def write_blob(self, data, info):
        key = urllib.quote(info['type'].encode('utf-8'), '') +\
            '/' + str(hash(data)) +\
            '/' + urllib.quote(info['name'].encode('utf-8'), '')
        try:
            memcache.set(key, data, time=EXPIRATION_TIME)
        except: #Failed to add to memcache
            return (None, None)
        thumbnail_key = None
        if IMAGE_TYPES.match(info['type']):
            try:
                img = images.Image(image_data=data)
                img.resize(
                    width=THUMB_MAX_WIDTH,
                    height=THUMB_MAX_HEIGHT
                )
                #thumbnail_data = img.execute_transforms()
                thumbnail_key = key + THUMB_SUFFIX
                memcache.set(
                    thumbnail_key,
                    thumbnail_data,
                    time=EXPIRATION_TIME
                )
            except: #Failed to resize Image or add to memcache
                thumbnail_key = None
        return (key, thumbnail_key)

    def handle_upload(self):
        results = []
        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = urllib.unquote(fieldStorage.filename)
            result['type'] = fieldStorage.type
            result['size'] = self.get_file_size(fieldStorage.file)
            if self.validate(result):
                key, thumbnail_key = self.write_blob(
                    fieldStorage.value,
                    result
                )
                if key is not None:
                    result['url'] = self.request.host_url + '/' + key
                    result['deleteUrl'] = result['url']
                    result['deleteType'] = 'DELETE'
                    if thumbnail_key is not None:
                        result['thumbnailUrl'] = self.request.host_url +\
                             '/' + thumbnail_key
                else:
                    result['error'] = 'Failed to store uploaded file.'
            results.append(result)
        return results


    @ndb.transactional(xg=True)
    def update_stream(self, image_):
        stream_id = self.request.get('stream_id')
        comment = self.request.get('comment')
        lat = self.request.get('Latitude')
        lng = self.request.get('Longitude')

        if (lat == '') or (lng == ''):
            lat = 0.0
            lng = 0.0
        photo = Photo(image=image_, stream_id=stream_id, comment=comment,
                      Latitude=lat, Longitude=lng)
        key = photo.put()

        stream = Stream.query_by_id(int(stream_id))
        if len(stream.cover) == 0:
            stream.cover = str(key.id())
        stream.photos.append(key.id())
        stream.put()


    def post(self):
        global mutex
        img = self.request.get_all('files[]')
        #img = self.request.POST.items()

        status_code = 0
        print "length of img %d" % len(img)
        if len(img):
            for image_ in img:
                print "found an image"
                mimetype = self.request.POST['files[]'].type  ###need to find how filter through all
                img_format = mimetype.split('/')[1]
                print img_format, '------------debug'
                mutex.acquire()
                try:
                    if (img_format in ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'tiff', 'ico', 'webp']):
                        self.update_stream(image_)
                    else:
                        status_code = 201
                finally:
                    mutex.release()


        else:
            status_code = 200

        if (self.request.get('_method') == 'DELETE'):
            return self.delete()
        result = {'files': self.handle_upload()}
        s = json.dumps(result, separators=(',', ':'))
        """
        redirect = self.request.get('redirect')
        if redirect:
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        """
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)



    def delete(self):
        print "Deleting... "
