import webapp2
import json
from google.appengine.ext import blobstore

class GetUploadURL(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/uploadwithurl')
        upload_url = str(upload_url)
        response = {'upload_url' : upload_url}
        jsonObj = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
        self.response.write(jsonObj)
