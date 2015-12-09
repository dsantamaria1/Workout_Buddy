import webapp2, re
from jinja import JINJA_ENVIRONMENT
import requests
from handlers.api.GenPush import GenPush
from handlers.api.GetPath import GetPath


class GenWorkout(webapp2.RequestHandler):
    def get(self):
        category = self.request.get('WoSel')
        result = re.search("Upper Body Push", category, re.IGNORECASE)
        BASE = GetPath(self.request.url, self.request.path)

        if result:
            resp = requests.get(BASE+"/api/genPush", params={'category': 0})
        else:
            resp = requests.get(BASE+"/api/genPush", params={'category': 1})

        template_values = resp.json()

        template = JINJA_ENVIRONMENT.get_template('startWorkout.html')
        self.response.write(template.render(template_values))
        #self.response.write(template_values)
