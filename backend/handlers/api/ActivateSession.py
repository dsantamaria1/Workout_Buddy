import webapp2, json
from domain.Stream import Stream
from domain.Session import Session

class ActivateSession(webapp2.RequestHandler):
    def get(self):
        session_id = self.request.get('session_id')
        session = Session.query_by_id(int(session_id))
        stream = Stream.query_by_name(session.exercises[session.currWO])
        #use stream[0] for first element in list

        myDict = {"session_id": session_id,
                  "photo": stream[0].woPics[unicode(session.step)], #get the first pic
                  "instructions": stream[0].woInstructions[unicode(session.step)],
                  "name": stream[0].name}
        self.response.write(json.dumps(myDict))

    def post(self):
        session_id = self.request.get('session_id')
        session = Session.query_by_id(int(session_id))
        print "post ActivateSession"
        session.active = True
        session.put()
