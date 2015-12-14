import webapp2, json
from domain.Stream import Stream
from domain.Session import Session

class ActivateSession(webapp2.RequestHandler):
    def get(self):
        session_id = self.request.get('session_id')
        session = Session.query_by_id(int(session_id))
        stream = Stream.query_by_name(session.exercises[session.currWO])
        #use stream[0] for first element in list

        if session.step >= stream[0].totalSteps:
            lastStep = True
            step_ = stream[0].totalSteps
        else:
            lastStep = False
            step_ = session.step

        if session.currWO >= (session.totalWOs - 1): # subtract 1 because exerciseList starts at element 0
            lastWO = True
            print "This is the last workout. currWO = %d, totalWOs = %d" % (session.currWO, session.totalWOs)
        else:
            lastWO = False
            print "This is NOT the last workout. currWO = %d, totalWOs = %d" % (session.currWO, session.totalWOs)

        myDict = {"session_id": session_id,
                  "photo": stream[0].woPics[unicode(step_)], #get the first pic
                  "instructions": stream[0].woInstructions[unicode(step_)],
                  "name": stream[0].name,
                  "lastStep": lastStep,
                  "lastWO": lastWO}
        self.response.write(json.dumps(myDict))

    def post(self):
        session_id = self.request.get('session_id')
        incStep = self.request.get('incStep')
        incWO = self.request.get('incWO')
        session = Session.query_by_id(int(session_id))
        print "post ActivateSession"
        session.active = True

        if (int(incStep) == 1) and (int(incWO) == 0):
            session.step +=1
            print "incrementing steps"

        if(int(incStep) == -1 and (session.step > 1)):
            session.step -=1
            print "incrementing steps"
        elif(int(incStep) == -1 and (session.step == 1) and (session.currWO > 0)):
            session.currWO -= 1
            session.step = 3
            print "decrementing WO and setting steps to 3"

        if ((int(incWO) == 1)):
            if (session.currWO + 1) <= session.totalWOs:
                session.step = 1 #start at step 1 for next workout
                session.currWO +=1
                print "incrementing WORKOUT and resetting steps"

        if(int(incWO) == -1): #reset
                session.step = 1 #start at step 1 for next workout
                session.currWO = 0 #start at first WO
        session.put()
