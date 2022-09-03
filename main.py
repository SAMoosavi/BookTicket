"""
import json
from AliBabaBookTicket import AliBabaBookTicket
from SafirBookTicket import SafirBookTicket
from MrBilitBookTicket import MrBilitBookTicket
from BookTicket import BookTicket

bookTicket: BookTicket = MrBilitBookTicket()

# data = {
#     'dataLogin': {
#         'username': "moosavi238@gmail.com",
#         'password': "Ali1#2#3#4#"
#
#     },
#     'data': {
#         'fromd': '1401/05/19',
#         'tod': '1401/06/06',
#         'from': "219",
#         'to': "1",
#         'sex': "3",
#         'wagon': "0",
#         'groupWay': 1,
#         'adult': "1",
#         'child': "0",
#         'infant': "0"
#     }
#     , 'listId': [[621, 821], [822, 720, 722, 620]],
#     'travelers': [
#         {
#             'id': "4421161772",
#             'birthday': {
#                 'day': "27",
#                 'month': '03',
#                 'year': "82"
#             },
#             'FName': "سید علی",
#             'LName': "موسوی",
#             'sex': "2",
#             'service': "جوجه"
#         }
#     ]
# }
fileJson = open("./Path.json", 'r')
data = json.loads(fileJson.read())
fileJson.close()
print(data)

bookTicket.login(data['dataLogin'])

searchSuper: bool = True
if searchSuper and type(bookTicket) == MrBilitBookTicket:
    bookTicket.searchS(data["data"], data["listId"])
else:
    bookTicket.search(data["data"])

bookTicket.setUsers(data["travelers"])
bookTicket.buy()
"""
import json
import time

from GetTicket import GetTicket
from Passenger import Passenger
from Path import Path
from Person import Person

personJson = open("./Person.json", 'r')
personData = json.loads(personJson.read())
personJson.close()
del personJson

passenger = Passenger()

for person in personData:
    per = Person()
    per.set_on_dict(person)
    passenger.add_person(per)

pathJson = open("./Path.json", 'r')
data = json.loads(pathJson.read())
pathJson.close()
del pathJson

path = Path()
pathData = data['path']
i: int = 0
while True:
    i += 1
    if path.is_free(pathData['beginning'], pathData['ending'], pathData['date'], pathData['sex'], data['listId']):
        getTicket = GetTicket()
        loginData = data['login']
        getTicket.login(loginData['username'], loginData['password'])
        tickets = getTicket.get_tickets(pathData['beginning'], pathData['ending'], pathData['date'], pathData['adult'],
                                        pathData['child'], pathData['sex'])
        getTicket.sel_ticket(path.find_ticket(tickets), data['Passengers'])
        break
    time.sleep(3)
    print(i)
