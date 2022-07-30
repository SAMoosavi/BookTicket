from AliBabaBookTicket import AliBabaBookTicket
from SafirBookTicket import SafirBookTicket
from BookTicket import BookTicket

bookTicket: BookTicket = AliBabaBookTicket()

dataLogin: dict = {
    'username': "09101513198",
    'password': "1#2#3#4#"

}

bookTicket.login(dataLogin)
# sex : 1 = woman 2 = man 3 = other
data = {
    'fromd': '1401/05/20',
    'tod': '1401/05/30',
    'from': "1",
    'to': "191",
    'sex': "3",
    'wagon': "0",
    'groupWay': 1,
    'adult': "1",
    'child': "0",
    'infant': "0"
}
bookTicket.search(data)

travelers = [
    {
        'id': "4421161772",
        'birthday': {
            'day': "27",
            'month': '03',
            'year': "82"
        },
        'FName': "سید علی",
        'LName': "موسوی",
        'sex': "2"
    }
]

bookTicket.setUsers(travelers)
bookTicket.buy()
