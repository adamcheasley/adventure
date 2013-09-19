from textwrap import dedent
# each room has a Cartesian coordinate in three dimensions

world = [
    {'room': {'title': 'Driveway',
              'description': (dedent("""You are at the end of a long driveway.
              In the distance is a large building. To either side is lush green grass.
              The drive leads north.
              """),
                              ''),
              'location': [0, 0, 0]},
     },
    {'room': {'title': 'Driveway',
              'description': (dedent("""\
              You are half way up the driveway. At the end of the drive is a
              tall, moderen office building. The drive continues north.
              """),
                              ''),
              'location': [0, 1, 0]},
     'items': [{'title': 'key',
                'description': 'A laser cut key. It looks very new.',
                'use_location': [0, 2, 0]}
               ],
     },
    {'room': {'title': 'Building door',
              'description': (dedent("""\
              You are at the door to the building.
              """),
                              ''),
              'location': [0, 2, 0]},
     },
    {'room': {'title': 'lobby',
              'description': ('You are in the lobby. There is a large digital clock on the wall which reads "09:32". To the east is a door.',
                              'bar'),
              'location': [0, 3, 0]},
     },
    {'room': {'title': 'room 2',
              'description': ('You enter a corridoor. To the north is a door.',
                              'bar'),
              'location': [1, 3, 0]},
     },
    {'room': {'title': 'Kitchen',
              'description': ('A very used kitchen. The exit is behind you to the south.',
                              'bar'),
              'location': [1, 4, 0]},
     'items': [{'title': 'watch',
                'use_location': [4, 5, 6]}],
     },
]
