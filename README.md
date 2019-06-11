# Adventure

A text adventure game featuring time travel.

This project is not really in a playable state. I am still working on
the framework, so the actual story needs a lot of work.


## Installation

This game was written for python 3.

Get yourself a virtualenv:
`python3 -m venv .`
`. bin/activate`  
Then install the requirements:  
`pip install -r requirements.txt `

To play, simply run `python adventure.py`


## Map Layout

we create a world for each timezone past/present
each room has a set of coordinates indicating its place in three dimensions

present:
  x-y-z:
    title: str
    description: [long, short]
    blocked: bool
    blocked_reason: str
    blocked_description: str
    unblocked: str
    room_items:
      title: str
      description: str
      use_location: [x, y, z]


----------------------------------------
Further info:

 - blocked_description:    This is added to the description if
                           the room is blocked.

 - unblocked:              This is printed when the room is unlocked.

 - use_location            Where this is item needed.
