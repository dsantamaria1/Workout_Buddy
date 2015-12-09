import webapp2
from api.ActivateSession import ActivateSession
import requests
from handlers.api.GetPath import GetPath
from domain.Session import Session
from jinja import JINJA_ENVIRONMENT

class DisplayWorkout(webapp2.RequestHandler):
    def get(self):
        print "hi DisplayWorkout get"
        session_id = self.request.get('session_id')
        BASE = GetPath(self.request.url, self.request.path)
        resp = requests.get(BASE+"/api/activateSession", params={"session_id": session_id})
        template_values = resp.json()
        template = JINJA_ENVIRONMENT.get_template('displayWorkout.html')
        self.response.write(template.render(template_values))

    def post(self):
        session_id = self.request.get('session_id')
        incStep = self.request.get('incStep')
        incWO = self.request.get('incWO')
        BASE = GetPath(self.request.url, self.request.path)
        resp = requests.post(BASE+"/api/activateSession", params={"session_id": session_id,
                                                                   "incStep": incStep,
                                                                   "incWO": incWO})
        self.redirect('/displayWorkout?session_id=' + session_id)
