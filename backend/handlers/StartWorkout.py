import webapp2
import requests, json
from jinja import JINJA_ENVIRONMENT

class StartWorkout(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('startWorkout.html')
        self.response.write(template.render())
