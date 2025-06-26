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
default current_message_1  = ""                                                                                             # ═══► Main information message (e.g. “Betting round: Flop”)
default current_message_2  = ""                                                                                             # ═══► Secondary information message (e.g. “Your cards: AH KS”)
default game_debug_mode    = True                                                                                           # ═══► If True, AI maps are visible for debugging purposes

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Ren'Py styles definition
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
style default:
    font  "Futura.ttc"
    size  28
    color "#FFFFFF"
# End syle
style STYLE_CHOICE_BUTTON_LIME:
    font "Futura.ttc"
    size 32
    idle_color "#FFFFFF"
    hover_color "#FFFF00"
    selected_idle_color "#00FF00"
    selected_hover_color "#AAFF00"
    background "#404040CC"                                                                                                  # ═══► Slightly transparent background
    hover_background "#606060CC"
    xmaximum 200                                                                                                            # ═══► Largeur max des boutons
    ymaximum 60                                                                                                             # ═══► Hauteur max des boutons
    box_wrap True
    text_align 0.5
    text_vertical_align 0.5
    padding (10, 10)
    xradius 10                                                                                                              # ═══► Add rounded corners for enhanced aesthetics
    yradius 10
# End syle
style POKER_TEXT:
    font "Futura.ttc"
    size 28
    color "#FFFFFF"
    outlines [ (1, "#000000", 0, 0) ]                                                                                       # ═══► Black outline for easy viewing
# End syle
style POKER_CHIP_TEXT:
    font "Futura.ttc"
    size 22
    color "#FFFF00"                                                                                                         # ═══► Yellow for chips
    outlines [ (1, "#000000", 0, 0) ]
# End syle
style POKER_PLAYER_NAME:
    font "Futura.ttc"
    size 26
    color "#ADD8E6"                                                                                                         # ═══► Light blue for player names
    outlines [ (1, "#000000", 0, 0) ]
# End syle

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Ren'Py images definition
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
# ► Make sure images are in the ‘images/’ folder.
# ►    Ex: AH.png, 2C.png, card_back.png, poker_table_bg.jpg
image card_back = "images/cards/card_back.png"                                                                         # ═══► Image for the back of the hidden cards
#image poker_table_bg = "poker_table_bg.jpg"                                                                            # ═══► Poker table background image

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Ren'Py poker screens definition
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
screen poker_game_screen():
    tag menu                                                                                                           # ═══► Hide this screen with commands such as ‘hide screen menu’.
   
#    add "poker_table_bg"                                                                                               # ═══► Poker table background

    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Displaying common cards
    # ╰─────────────────────────────────────────────────────────────────────────
    frame:
        xalign 0.5
        yalign 0.3
        background "#00000088"                                                                                         # ═══► Semi-transparent black background
        padding (10, 10)
        xradius 10
        yradius 10
        hbox:
            spacing 10
            for card in poker_game.community_cards:
                add card.get_image_name() size (80, 112)                                                               # ═══► Size of card images
            # End for
        # End hbox
    # End frame
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Pot display
    # ╰─────────────────────────────────────────────────────────────────────────
    text "Pot: [poker_game.pot]" style POKER_TEXT:
        xalign 0.5
        yalign 0.45
        outlines [ (2, "#000000", 0, 0) ]                                                                              # ═══► More pronounced pot shape
    # End text
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Displaying player information
    # ╰─────────────────────────────────────────────────────────────────────────
    # ► Use a "fixed" to position players around the table more flexibly.
    fixed:
        $ human_player = poker_game.players[0]                                                                         # ═══► The human player is always first
        vbox:
            xalign 0.5
            yalign 0.9
            spacing 5
            text "[human_player.name]":
                style POKER_PLAYER_NAME
                if human_player.is_dealer: text_color "#FFD700"                                                        # ═══► Gold for the dealer
                if human_player.is_small_blind: text_color "#FFA07A"                                                   # ═══► Salmon for Small Blind
                if human_player.is_big_blind: text_color "#FF8C00"                                                     # ═══► Dark orange for Big Blind
            text "Chips: [human_player.chips]" style POKER_CHIP_TEXT
            text "Bet: [human_player.current_bet]" style POKER_CHIP_TEXT
            hbox:
                spacing 5
                for card in human_player.hand:
                    add card.get_image_name() size (70, 98)                                                            # ═══► Slightly larger size for player cards
                # End for
            # End hbox
            if human_player.has_folded: text "(FOLDED)" style POKER_TEXT color "#FF0000"
            if human_player.is_all_in: text "(ALL-IN)" style POKER_TEXT color "#00FF00"
        # End vbox
        if len(poker_game.players) > 1:
            $ robot_player = poker_game.players[1]                                                                      # ═══► Robot player (second player)
            vbox:
                xalign 0.5
                yalign 0.1
                spacing 5
                text "[robot_player.name]":
                    style POKER_PLAYER_NAME
                    if robot_player.is_dealer: text_color "#FFD700"
                    if robot_player.is_small_blind: text_color "#FFA07A"
                    if robot_player.is_big_blind: text_color "#FF8C00"
                # End text
                text "Jetons: [robot_player.chips]" style POKER_CHIP_TEXT
                text "Mise: [robot_player.current_bet]" style POKER_CHIP_TEXT
                hbox:
                    spacing 5
                    for card in robot_player.hand:
                        if game_debug_mode: add card.get_image_name() size (60, 84)
                        else: add "card_back" size (60, 84)
                    # End for
                # End hbox
                if robot_player.has_folded: text "(FOLDED)" style POKER_TEXT color "#FF0000"
                if robot_player.is_all_in: text "(ALL-IN)" style POKER_TEXT color "#00FF00"
            # End vbox
        # End if
    # End fixed
   if poker_game is not None and poker_game.get_current_player() is not None:                                           # ═══► Player action section (only if it's his turn and he's human)
        $ current_acting_player = poker_game.get_current_player()
        if current_acting_player.is_human:
            frame:
                xalign 0.5
                yalign 0.98                                                                                             # ═══► Positioning at the bottom of the screen
                background "#000000CC"                                                                                  # ═══► Semi-transparent dark background
                padding (20, 10)
                xradius 15                                                                                              # ═══► More rounded corners
                yradius 15
                hbox:
                    spacing 15                                                                                          # ═══► Button spacing
                    # ► Bouton FOLD
                    textbutton "FOLD" action Return({"action": "fold"}):
                        style STYLE_CHOICE_BUTTON_LIME
                        tooltip "Abandon current hand."
                    # End textbutton
                    # ► Bouton CHECK / CALL
                    $ amount_to_match_for_call = poker_game.current_highest_bet - current_acting_player.current_bet     # ═══► Calculates the amount the player must match to "call"
                    if current_acting_player.can_check(poker_game.current_highest_bet):
                        textbutton "CHECK" action Return({"action": "check"}):
                            style STYLE_CHOICE_BUTTON_LIME
                            tooltip "Pass the round without betting (if no one has bet)."
                        # End textbutton
                    elif current_acting_player.can_call(poker_game.current_highest_bet):
                        $ display_call_amount = min(amount_to_match_for_call, current_acting_player.chips)              # ═══► Display actual amount
                        textbutton "CALL ([display_call_amount])" action Return({"action": "call", "amount_needed": poker_game.current_highest_bet}):
                            style STYLE_CHOICE_BUTTON_LIME
                            # ► Disable if not enough chips for a full call, unless ALL-IN button is available.
                            sensitive current_acting_player.chips >= amount_to_match_for_call or current_acting_player.is_all_in
                            tooltip "Match the current bet."
                        # End textbutton
                    else:
                        textbutton "CHECK/CALL" action NullAction() sensitive False:                                    # ═══► If neither check nor call is possible, deactivate the
                            style STYLE_CHOICE_BUTTON_LIME
                        # End textbutton
                    # End if
                    # ► Bouton BET / RAISE
                    $ min_bet_val = poker_game.BIG_BLIND_VAL                                                            # ═══► Minimum bet for a new bet
                    $ min_raise_val = poker_game.BIG_BLIND_VAL * 2                                                      # ═══► Minimum for a raise (2x BB, common convention)
                    if poker_game.current_highest_bet == 0:                                                             # ═══► If no one has bet (can BET)
                        $ suggested_bet_amount = min(current_acting_player.chips, min_bet_val * 2)                      # ═══► Suggests 2xBB
                        textbutton "BET ([suggested_bet_amount])" action Return({"action": "bet", "amount_needed": suggested_bet_amount}):
                            style STYLE_CHOICE_BUTTON_LIME
                            sensitive current_acting_player.chips >= suggested_bet_amount                               # ═══► Activate if the player has enough tokens
                            tooltip "Making an initial bet."
                        # End textbutton
                    elif current_acting_player.can_raise(poker_game.current_highest_bet, min_raise_val):                # ═══► Can RAISE
                        $ amount_to_add_for_raise = (poker_game.current_highest_bet - current_acting_player.current_bet) + min_raise_val
                        $ display_raise_to = poker_game.current_highest_bet + min_raise_val                             # ═══► Total amount after raise: current stake + raise amount
                        textbutton "RAISE ([display_raise_to])" action Return({"action": "raise", "amount_needed": poker_game.current_highest_bet, "raise_by": min_raise_val}):
                            style STYLE_CHOICE_BUTTON_LIME
                            sensitive current_acting_player.chips >= amount_to_add_for_raise                            # ═══► Activate if the player can afford the raise
                            tooltip "Increase current bet."
                        # End textbutton
                    else:                                                                                               # ═══► When neither bet nor raise is possible
                        textbutton "BET/RAISE" action NullAction() sensitive False:
                            style STYLE_CHOICE_BUTTON_LIME
                        # End textbutton
                    # End if
                    if current_acting_player.chips > 0 and not current_acting_player.is_all_in:                         # ═══► ALL-IN button (always available if the player has chips and is not already all-in)
                        textbutton "ALL-IN ([current_acting_player.chips])" action Return({"action": "all_in"}):
                            style STYLE_CHOICE_BUTTON_LIME
                            tooltip "Bet all your chips."
                        # End textbutton
                    else:
                        textbutton "ALL-IN" action NullAction() sensitive False:
                            style STYLE_CHOICE_BUTTON_LIME
                        # End textbutton
                    # End if
                # End hbox
            # End frame
        # End if
    # End if
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Floating information screen (SC_POKER_INFORMATION)
    # ╰─────────────────────────────────────────────────────────────────────────
    screen SC_POKER_INFORMATION(sMessage1, sMessage2):
        frame:
            background "#404040AA"                                                                                      # ═══► Semi-transparent grey background
            xalign 1.0
            yalign 0.01
            xsize 0.30
            ysize 0.12
            padding (10, 5)
            xradius 10
            yradius 10
            vbox:
                text sMessage1 style POKER_TEXT size 22
                text sMessage2 style POKER_TEXT size 20
            # End vbox
        # End frame
    # End screen
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Using the information screen
    # ╰─────────────────────────────────────────────────────────────────────────
    use SC_POKER_INFORMATION(current_message_1, current_message_2)
# End screen

# The game starts here.

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Ren'Py labels
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
label start:
    "Welcome to Texas Hold'em!"
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Initializing the poker game
    # ╰─────────────────────────────────────────────────────────────────────────
    # ► num_ai_players=1 for a game with two players (one human, one robot)
    $ poker_game = poker.PokerGame(human_player_name=player_name, num_ai_players=1)
    "Get ready for a new game with [len(poker_game.players) - 1] AI opponent!"
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Call the main game loop
    # ╰─────────────────────────────────────────────────────────────────────────
    call LB_TEXAS_HOLDEM()
    "Thanks for playing Texas Hold'em!"
    return
# End label
label LB_TEXAS_HOLDEM():
    # Boucle qui représente la succession des mains de poker
    while PokerLoop:
        # Afficher la main actuelle (pour le joueur humain, les cartes des IA sont cachées)
        $ current_message_1 = f"Main #{poker_game.num_hands_played + 1}"
        $ current_message_2 = "Nouvelle main en préparation..."
        show screen poker_game_screen
        pause 1.0 # Petite pause visuelle

        # Vérifier si la partie doit se terminer (ex: un seul joueur restant avec des jetons)
        $ active_players_in_game = [p for p in poker_game.players if p.chips > 0]
        if len(active_players_in_game) <= 1:
            $ final_winner = active_players_in_game[0] if active_players_in_game else None
            if final_winner:
                "Félicitations, [final_winner.name], vous avez remporté la partie !"
            else:
                "La partie est terminée, mais aucun vainqueur n'a pu être désigné."
            # End screen
            PokerLoop = False # Sortir de la boucle de jeu
        # End if

        # 1. Réinitialiser la main et assigner le bouton du dealer
        $ poker_game.reset_hand()
        $ current_message_2 = f"Dealer: {poker_game.players[poker_game.dealer_index].name}"
        show screen poker_game_screen
        pause 1.0

        # 2. Assigner et collecter les blinds
        $ poker_game.assign_blinds()
        $ current_message_2 = f"Petite Blinde: {pl.PokerGame.SMALL_BLIND_VAL}, Grosse Blinde: {pl.PokerGame.BIG_BLIND_VAL}"
        show screen poker_game_screen
        pause 1.5

        # 3. Distribuer les cartes privées (hole cards)
        $ poker_game.deal_hole_cards()
        $ current_message_1 = "Cartes distribuées."
        # Afficher les cartes du joueur humain dans le message d'info
        $ human_player_hand_str = " ".join(str(c) for c in poker_game.players[0].hand)
        $ current_message_2 = f"Vos cartes: [human_player_hand_str]"
        show screen poker_game_screen
        pause 2.0

        # 4. Tour de mise (Pre-flop)
        $ poker_game.game_state = pl.PokerGame.GAME_STATE_PREFLOP
        $ current_message_1 = "Tour de mise: Pre-flop"
        $ current_message_2 = f"Pot: {poker_game.pot}. Mise la plus haute: {poker_game.current_highest_bet}"
        show screen poker_game_screen
        call betting_round_logic # Appel de la logique du tour de mise

        # Vérifier si la main est terminée après le tour de mise (si un seul joueur actif)
        $ active_players_count = len(poker_game.get_active_players_in_hand())
        if active_players_count <= 1:
            jump hand_end # Aller à la fin de la main si un seul joueur restant

        # 5. Distribuer le Flop et nouveau tour de mise
        $ current_message_1 = "Tour de mise: Flop"
        $ current_message_2 = "Distribution du Flop..."
        show screen poker_game_screen
        pause 1.0
        $ poker_game.deal_community_cards(3) # Distribue 3 cartes pour le Flop
        show screen poker_game_screen
        pause 1.5
        $ poker_game.game_state = pl.PokerGame.GAME_STATE_FLOP
        call betting_round_logic

        if active_players_count <= 1:
            jump hand_end

        # 6. Distribuer le Turn et nouveau tour de mise
        $ current_message_1 = "Tour de mise: Turn"
        $ current_message_2 = "Distribution du Turn..."
        show screen poker_game_screen
        pause 1.0
        $ poker_game.deal_community_cards(1) # Distribue 1 carte pour le Turn
        show screen poker_game_screen
        pause 1.5
        $ poker_game.game_state = pl.PokerGame.GAME_STATE_TURN
        call betting_round_logic

        if active_players_count <= 1:
            jump hand_end

        # 7. Distribuer la River et nouveau tour de mise
        $ current_message_1 = "Tour de mise: River"
        $ current_message_2 = "Distribution de la River..."
        show screen poker_game_screen
        pause 1.0
        $ poker_game.deal_community_cards(1) # Distribue 1 carte pour la River
        show screen poker_game_screen
        pause 1.5
        $ poker_game.game_state = pl.PokerGame.GAME_STATE_RIVER
        call betting_round_logic

        if active_players_count <= 1:
            jump hand_end

        # 8. Showdown (dévoilement des mains et détermination du gagnant)
        label showdown:
            $ poker_game.game_state = pl.PokerGame.GAME_STATE_SHOWDOWN
            $ current_message_1 = "Showdown !"
            $ current_message_2 = "Dévoilement des mains des joueurs restants..."
            show screen poker_game_screen
            pause 2.0

            # Déterminer le(s) gagnant(s)
            $ winners, winning_desc = poker_game.determine_winner()
            $ current_message_1 = "Résultats de la main :"
            $ current_message_2 = winning_desc
            show screen poker_game_screen
            pause 3.0

            # Distribuer le pot
            $ poker_game.distribute_pot(winners)
            show screen poker_game_screen
            pause 2.0

        # Fin de la main (pour les cas de fold anticipé ou de showdown)
        label hand_end:
            $ poker_game.game_state = pl.PokerGame.GAME_STATE_END_HAND
            $ current_message_1 = "Fin de la main."
            $ current_message_2 = "Préparation de la prochaine main..."
            show screen poker_game_screen
            pause 2.0

            # Vérifier si des joueurs sont éliminés
            $ players_eliminated_this_hand = [p for p in poker_game.players if p.chips <= 0]
            if players_eliminated_this_hand:
                $ current_message_1 = "Joueurs éliminés :"
                $ current_message_2 = ", ".join([p.name for p in players_eliminated_this_hand]) + " n'ont plus de jetons !"
                show screen poker_game_screen
                pause 2.0

    return # Fin de la boucle de jeu principale



    return
# End label
