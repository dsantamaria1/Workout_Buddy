import webapp2, random, json
from domain.Stream import Stream
from domain.Session import Session

class GenPush(webapp2.RequestHandler):
    def get(self):
        PushList = []
        PullList = []

        parameter = self.request.get('category')
        if int(parameter) == 0:
            category = 'Upper Body Push/Lower Body Pull'
            PushQuery = Stream.query(Stream.woType == '0') #upper push
            PullQuery = Stream.query(Stream.woType == '3') #lower pull
        else:
            category = 'Upper Body Pull/Lower Body Push'
            PullQuery = Stream.query(Stream.woType == '1') #upper pull
            PushQuery = Stream.query(Stream.woType == '2') # lower push

        for x in PushQuery:
            PushList.append(x.name)

        for x in PullQuery:
            PullList.append(x.name)

        exerciseList = []
        exerciseList.append(random.choice(PushList))
        exerciseList.append(random.choice(PullList))
        reps = random.choice(['5 sets of 5','4 sets of 10','4 sets of 15'])
        totalWOs = len(exerciseList)

        session = Session(category=category, exercises=exerciseList,reps=reps,currWO=0,
                          step=1,active=False,totalWOs=totalWOs,completed=False)

        key = session.put()
        session_id=key.id()
        workouts = {'reps': reps,
                    'exercises': exerciseList,
                    'category': category,
                    'totalWOs': totalWOs,
                    'session_id': session_id
                    }
        print json.dumps(workouts)
        self.response.write(json.dumps(workouts))
