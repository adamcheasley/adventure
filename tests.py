from content import Item, Room, World


def test_parse_map():
    """parse map expects a python data structure
    """
    world_data = {
        "present": {
            "0-0-0": {
                "description": "You are at the end of a long "
                "driveway.\n"
                "In the  distance is a large "
                "building. \n"
                "To either side is grass and then a "
                "high concrete wall.\n"
                "The drive leads north.",
                "title": "Gate",
            },
            "0-1-0": {
                "description": "You are half way up the driveway. "
                "At the end of the drive is a tall,\n"
                "modern office building.\n"
                "The drive continues north.",
                "room_items": [
                    {
                        "description": "A laser cut key. It " "looks very new.",
                        "title": "key",
                        "use_location": [0, 2, 0],
                    }
                ],
                "title": "Driveway",
            },
        }
    }
    world = World(world_data)
    assert isinstance(world.adventure_map, dict)
    assert "present" in world.adventure_map
    assert len(world.adventure_map["present"]) == 2


def test_room():
    room = Room(
        title="test room",
        description="this is just a test",
        short_description="just a test",
        blocked=False,
        blocked_reason="",
        unblocked="",
        blocked_description="",
        death_if_entered=False,
    )
    full_description = room.describe_location()
    expected = "{}\n{}".format(room.title, room.long_description)
    assert full_description == expected

    item = Item(
        title="test object",
        description="just a test",
        use_location=[0, 0, 0],
        hidden=False,
        when_eaten="nothing",
    )
    room.items[item.title] = item
    assert "There is a test object here" in room.describe_location()
