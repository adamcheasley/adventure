"""
# each room has a Cartesian coordinate in three dimensions
{'room': {'title': str,
          'description': (long, short),
          'location': [x, y, z],
          'blocked': bool,
          'blocked_reason': str,
          'blocked_description': str,  # This is added to the description if
                                       # the room is blocked
          'unblocked': str  # This is printed when the room is unlocked},
 'items': [{'title': str,
           'description': str,
           'use_location' [x, y, z],  # Where this is item needed}],
}
"""

main_map = [
    {'room': {'title': 'Gate',
              'description': (("You are at the end of a long driveway.\nIn the"
                               " distance is a large building. \nTo either"
                               " side is grass and then a high concrete wall."
                               "\nThe drive leads"
                               " north."),
                              ''),
              'location': [0, 0, 0]},
     },
    {'room': {'title': 'Driveway',
              'description': (("You are half way up the driveway."
                               " At the end of the drive is a tall,"
                               "\nmodern office building."
                               "\nThe drive continues north."),
                              ''),
              'location': [0, 1, 0]},
     'items': [{'title': 'key',
                'description': 'A laser cut key. It looks very new.',
                'use_location': [0, 2, 0]}
               ],
     },
    {'room': {'title': 'Building door',
              'description': ("You are at the door to the building.",
                              ''),
              'location': [0, 2, 0],
              'blocked': True,
              'blocked_reason': 'The door is locked\n',
              'blocked_description': 'It appears to be locked.',
              'unblocked': ('You insert the key into the massive door.'
                            '\nThere is some clunking and a couple of '
                            'beeps and finally, the door opens\n')},
     },
    {'room': {'title': 'Lobby',
              'description': (('You are in the lobby. There is a huge'
                               ' sign on the wall which reads'
                               ' "BFC Laboratories". \nThere is also'
                               ' a large digital clock on the wall'
                               '\nwhich reads "09:32". To the east is'
                               ' a door.'),
                              'bar'),
              'location': [0, 3, 0]},
     },
    {'room': {'title': 'Office',
              'description': (('A regular looking office. There is'
                               ' a desk with a phone and computer.'
                               ' To the north is a door.'),
                              'bar'),
              'location': [1, 3, 0]},
     },
    {'room': {'title': 'Kitchen',
              'description': (('A very used kitchen. '
                               'The exit is behind you to the south.'),
                              'bar'),
              'location': [0, 4, 0]},
     'items': [{'title': 'watch',
                'use_location': [4, 5, 6]}],
     },
    {'room': {'title': 'Corridoor',
              'description': ('A blank corridoor. To the north is a door.',
                              'bar'),
              'location': [1, 4, 0]},
     },
    {'room': {'title': 'Stairwell',
              'description': (("You are in the stairwell of the building."
                               " Steps lead up to the next floor."),
                              ''),
              'location': [1, 5, 0]},
     },
    {'room': {'title': 'Stairwell',
              'description': (("You are in the stairwell of the building. "
                               "Steps lead up and down. "
                               "There is a door to the south."),
                              ''),
              'location': [1, 5, 1]},
     },
    {'room': {'title': 'Lab',
              'description': ("You are in a dark laboritory.",
                              ''),
              'location': [1, 4, 1]},
     'items': [{'title': 'time machine',
                'description': ('A small device which appears to allow'
                                ' one to travel through time!'),
                'use_location': None}],
     },
]
