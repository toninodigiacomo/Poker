# This file manages the user interface and game flow in Ren'Py, by interacting with the game logic defined in poker_logic.py.

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Importing  Python classes
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
# init python:
    # classPoker.py must be in game/python/
    import classPoker as poker
    import random
# End init python






# The game starts here.

label start:

    call LB_TEXAS_HOLDEM("Player", "Computer", 5, 100)


    "... Fin du jeu ..."

    return
