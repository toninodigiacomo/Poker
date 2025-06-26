# ╭───────────────────────────────────────────────────────────────────────────
# │  This file manages the user interface and game flow in Ren'Py, by         ──
# │  interacting with the game logic defined in poker_logic.py.
# ╰───────────────────────────────────────────────────────────────────────────
#   ╰───────────────────────────────────────────────────────────────────────────

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Importing  Python classes
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
init python:
    # ► classPoker.py must be in game/python/
    import python/classPoker as poker
    import random
# End init python

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global game variables
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
# ► These variables are instances of the poker_logic.py classes.
default poker_game         = None                                                                                           # ═══► Instance of the PokerGame class
default player_name        = "You"                                                                                          # ═══► Human player name
default current_message_1  = ""   # Message d'information principal (ex: "Tour de mise: Flop")
default current_message_2  = ""   # Message d'information secondaire (ex: "Vos cartes: AH KS")
default game_debug_mode    = True   # Si True, les cartes des IA sont visibles pour le débogage





# The game starts here.

label start:

    call LB_TEXAS_HOLDEM("Player", "Computer", 5, 100)


    "... Fin du jeu ..."

    return
