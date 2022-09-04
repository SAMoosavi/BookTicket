import json
import time

from v2.GetTicket import GetTicket
from v2.Passenger import Passenger
from v2.Path import Path
from v2.Person import Person

personJson = open("v2/data/Person.json", 'r')
personData = json.loads(personJson.read())
personJson.close()
del personJson

passenger = Passenger()

for person in personData:
    per = Person()
    per.set_on_dict(person)
    passenger.add_person(per)

pathJson = open("v2/data/Path.json", 'r')
data = json.loads(pathJson.read())
pathJson.close()
del pathJson

path = Path()
pathData = data['path']

while True:
    if path.is_free(pathData['beginning'], pathData['ending'], pathData['date'], pathData['sex'], data['listId']):
        getTicket = GetTicket()
        loginData = data['login']
        getTicket.login(loginData['username'], loginData['password'])
        tickets = getTicket.get_tickets(pathData['beginning'], pathData['ending'], pathData['date'], pathData['adult'],
                                        pathData['child'], pathData['sex'])
        getTicket.sel_ticket(path.find_ticket(tickets), data['Passengers'])
        break
    time.sleep(3)
