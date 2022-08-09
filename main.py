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
fileJson = open("./data.json", 'r')
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
