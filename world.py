# each room has a Cartesian coordinate in three dimensions

world = [
    {'room': {'title': 'lobby',
              'description': ('You are in the lobby. There is a large digital clock on the wall which reads "09:32". To the east is a door.', 'bar'),
              'location': [0, 0, 0]},
     'items': [],
     },
    {'room': {'title': 'room 2',
              'description': ('You enter a corridoor. To the north is a door.',
                              'bar'),
              'location': [1, 0, 0]},
     'items': [{'title': 'key',
                'description': 'A laser cut key. It looks very new.'}
               ],
     },
    {'room': {'title': 'Kitchen',
              'description': ('A very used kitchen. The exit is behind you to the south.',
                              'bar'),
              'location': [1, 1, 0]},
     'items': [{'title': 'watch'}],
     },
]
