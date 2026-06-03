# Adventure — TODO

Framework tasks below, grouped roughly by priority. The original design
notes are preserved under [Design notes](#design-notes).

## Critical bugs

- [x] **Fix the failing test.** `tests.py::test_room` didn't pass the new
      `loop` argument to `Room()`. (Its assertion was also stale — see the
      room-title item under Engine.)
- [x] **`use()` destroys items used in the wrong place.** `Player.use` now
      only consumes an item once the action actually succeeds; using it in the
      wrong place returns "Nothing happens." and keeps the item. The time
      machine is reusable and no longer consumed.
- [x] **`eat()` never removes the eaten item.** `Player.eat` now removes the
      item from inventory/room when it's actually eaten.
- [ ] **Time travel crashes the game.** Using the time machine calls
      `world.toggle_date()` → `"past"`, but `parse_map` only ever populates
      the timezone(s) present in the map and `map.yaml` has no `past`/`future`
      rooms. `current_room()` then returns `None` and the main loop crashes on
      `room.death_if_entered`. Guard against a `None` room and/or seed the
      other timezones. (Currently unreachable in play — no time machine exists
      in `map.yaml` — but still a latent crash. See Engine: time-travel model.)
- [x] **`print()` inside curses.** The only `print(...)` (time-machine branch
      of `Player.use`) is gone; it now returns the message so the parser writes
      it via `stdscr`.
- [x] **Process always exits with code 1.** `adventure.py` now exits `0` on a
      clean quit/save.
- [x] **`take` with a specific item name doesn't verify it's present.** It now
      checks membership and returns a friendly "I cannot see a … here." message.

## Engine / framework

- [x] **Replace `getattr`-based command dispatch.** `tools.py` now dispatches
      through a `VERB_SYNONYMS` whitelist (take/get/grab, look/examine/x,
      drop/leave, inventory/inv/i, use, eat, on), so unknown or internal names
      get "I do not understand." instead of being invoked. Covered by tests.
- [ ] **Centralise the parser.** Movement is a long if/elif chain mixed with
      verb dispatch. Split into: normalise input → resolve verb/synonym →
      resolve direction → dispatch. Makes new commands and tests far easier.
- [ ] **Make `current_room()` total.** Returning `None` should never crash the
      loop; handle missing rooms explicitly (especially across timezones).
- [ ] **Finish the time-travel model.** `toggle_date` only flips
      present↔past and ignores `future`; `TimeMachine.set_time/travel/output`
      and the `Watch` class are empty stubs. Decide the model (see design
      notes) and implement it.
- [ ] **Player state init is inconsistent.** `Player.__init__` overrides
      `Human.__init__` without calling `super()`, so `told_back_story` is never
      set and `Human.back_story` is dead code. Reconcile the Human/Player
      hierarchy.
- [x] **Inventory limit constant.** Lifted to `Player.MAX_ITEMS` and covered
      by a test.
- [x] **Room title on entry.** `describe_location()` now prepends the title,
      so first entry shows title + description and re-entry shows the title
      only. Verified against `map.yaml` and covered by `test_room`.
- [ ] **Save/load.** Only a single implicit ZODB autosave-on-exit exists. Add
      explicit save/load (named slots or at least load-or-new on startup) and a
      `data/` reset path. Confirm `data.fs*` stays git-ignored (it is).
- [x] **Resource handling.** `init_world` now opens `map.yaml` with a `with`
      block.

## Content & data

- [ ] **Nothing in the map uses the engine's features.** `map.yaml` has no
      `blocked` rooms, no `room_items` with `sprite_id`, and no `time machine`
      item, so sprites (`ScientistOne`, `ComputerOne`), blocking/unblocking, and
      time travel are all unreachable. Build out a small playable slice that
      actually exercises them.
- [ ] **Add `past` (and maybe `future`) rooms** so the time machine has a
      destination.
- [ ] **Place the time machine** somewhere obtainable; wire the `Watch` item.
- [ ] **Document every map field.** README lists the schema but
      `short_description`, `loop`, `death_if_entered`, `when_eaten`,
      `death_if_eaten`, `hidden`, `sprite_id` are undocumented. (Carried over
      from the original TODO: "Document all mapping features".)
- [ ] **Make `title` optional per the original note** ("No need for title on
      every map feature") or default it sensibly.

## Tests

- [ ] **Grow the suite beyond 2 tests.** Now at 15, covering take (presence +
      limit), use (right vs wrong location), eat (death + non-death), a map
      smoke test, and command dispatch (synonyms, unknown/internal verbs,
      GameOver propagation, look-at-item). Still to cover: movement
      (directions, `loop` mazes, `blocked` rooms), drop, look with no args,
      looking at a sprite, room unblocking in context, and time travel.
- [ ] **Adopt pytest discovery conventions.** Rename `tests.py` → `test_*.py`
      (or a `tests/` package) so `pytest` finds it by default.
- [x] **Add a smoke test** that loads `map.yaml` and constructs the `World`,
      to catch schema/code drift (`test_real_map_loads`).

## Tooling / project hygiene

- [ ] **Add packaging.** No `pyproject.toml`/`setup.py` and no console entry
      point — `python adventure.py` is the only way in. Add packaging and an
      `adventure` entry point.
- [ ] **Split dev vs runtime deps.** `pytest` is a dev-only dependency mixed
      into `requirements.txt`.
- [ ] **Add formatting/lint config.** Git history shows `black` was run; pin it
      (plus a linter such as ruff/flake8) in config so it's reproducible.
- [ ] **Add CI** (GitHub Actions) to run the tests and formatter on push.
- [ ] **README cleanup.** Recommend creating the venv *outside* the repo (or in
      `.venv/`) instead of at the project root, which scatters `bin/ lib/
      include/` into the working tree.

## Web frontend

- [ ] **The `web/` frontend is a disconnected stub.** `index.html` + `main.js`
      just echo input; there's no bridge to the Python game. Either wire it to a
      backend (e.g. expose the engine over a small API/websocket) or drop it
      until the engine is ready.

---

## Design notes

- No need for title on every map feature.
- Document all mapping features

### General text Adventure research

https://www.amc.com/shows/halt-and-catch-fire/exclusives/colossal-cave-adventure

### Back story

Alien abduction.

### Time machine

Time machine should not allow the user to enter datetimes. The time travel should be triggered through the story and the user should work out to what time they have been transported.

Alternatively, the time machine only sends the player from the present day, to a specific point in the past. This adds to the puzzles, in that some rooms require the player to go use the time machine to go back and change something or take an object back to the present to go forward.

### Map updates

Player meets a scientist in the main building which explains more of the story.

Add a puzzle/cipher to solve.

The computer in the office building should be able to be turned on and then display something.

### Meeting other people

The player should meet other people in the world. These people will give the player information or just objects they need. They will be more complex than the other objects.
The player can speak to each actor. When they do, the prompt should change to describe the conversation, i.e. who is speaking when. The player could choose from a set of responses.

### NLP

https://spacy.io/
