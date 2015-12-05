from google.appengine.api import users
from google.appengine.api import mail

import time
import webapp2
import requests, json, re
from jinja import JINJA_ENVIRONMENT
from handlers.api.CreateStream import CreateStream
from handlers.api.GetPath import GetPath

class Create(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_values = {
            'login_logout_url' : url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render(template_values))

    def post(self):
        #TODO: unique name
        BASE = GetPath(self.request.url, self.request.path)
        user = users.get_current_user()
        if user is None:
            self.redirect('/')
            return

        subscribers = self.request.get('subscribers')
        optional_mes = self.request.get('optional_msg')
        res = requests.post(BASE+"/api/create", params={"name": self.request.get('stream_name'),
                                                        "author": user.user_id(),
                                                        "tags": self.request.get('tags'),
                                                        "cover_url": self.request.get('cover_url'),
                                                        "email": user.email(),
                                                        "woType": self.request.get('woType')
                                                        })

        status_code = 1
        if res:
            result = res.json()
            status_code = result['status_code']

            #send emails
            if len(subscribers) > 0 and status_code == 0:
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', subscribers)
                for m in emails:
                    mes = mail.EmailMessage(sender="Connexus Invitation <xiaorong.fd@gmail.com>",
                                            subject="You had been invited to subscribe to your friend's photo stream!")
                    mes.to = m
                    mes.body = """
                        Dear %s,
                            You friend has invited you to subscribe to a photo stream:
                            %s
                            %s
                        """ %(m, BASE+'/view?stream_id='+str(result['key']), optional_mes)
                    mes.send()

        if status_code:
            self.redirect('/social?status_code='+str(status_code))
        else:
            self.redirect('/manage')
