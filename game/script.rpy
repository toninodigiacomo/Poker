# game/script.rpy
# Ce fichier gère l'interface utilisateur et le flux du jeu dans Ren'Py,
# en interagissant avec la logique du jeu définie dans classPoker.py.

# Importation de vos classes Python
init python:
    # La ligne d'importation correcte pour un fichier dans game/python/
    import python.classPoker as poker
    import random # Gardons random pour les IA, etc.
    # sys n'est plus nécessaire si le bloc de débogage sys.path est supprimé.

# Variables globales du jeu (maintenues par Ren'Py, donc sauvegardées)
default POKER_GAME              = None
default player_name             = "Vous"
default Current_Message_1       = ""
default Current_Message_2       = ""
default game_debug_mode         = True

# --- Définitions des styles Ren'Py ---
# CORRECTION: Déplacé les définitions de style ici pour qu'elles soient reconnues avant l'écran.
style default:
    font "Futura.ttc"
    size 28
    color "#FFFFFF"

style STYLE_CHOICE_BUTTON_LIME:
    font "Futura.ttc"
    size 32
    idle_color "#FFFFFF"
    hover_color "#FFFF00"
    selected_idle_color "#00FF00"
    selected_hover_color "#AAFF00"
    background "#404040CC" # Fond légèrement transparent
    hover_background "#606060CC"
    xmaximum 200 # Largeur max des boutons
    ymaximum 60  # Hauteur max des boutons
    box_wrap True
    text_align 0.5
    # CORRECTION: Supprimé vertical_align, car non directement supporté ici.
    # CORRECTION: Supprimé xradius et yradius d'ici pour la compatibilité
    # xradius 10
    # yradius 10

style POKER_TEXT:
    font "Futura.ttc"
    size 28
    color "#FFFFFF"
    outlines [ (1, "#000000", 0, 0) ] # Contour noir pour la lisibilité

style POKER_CHIP_TEXT:
    font "Futura.ttc"
    size 22
    color "#FFFF00" # Jaune pour les jetons
    outlines [ (1, "#000000", 0, 0) ]

style POKER_PLAYER_NAME:
    font "Futura.ttc"
    size 26
    color "#ADD8E6" # Bleu clair pour les noms de joueurs
    outlines [ (1, "#000000", 0, 0) ]

# --- Définition des images Ren'Py ---
image card_back = "images/cards/card_back.png"
image poker_table_bg = "poker_table_bg.jpg"

# --- Écran principal du jeu de poker (screen SC_POKER) ---
screen SC_POKER(sMessage1, sMessage2):
    tag menu

    add "poker_table_bg"

    frame:
        xalign 0.5
        yalign 0.3
        background "#00000088"
        padding (10, 10)
        # CORRECTION: Supprimé xradius et yradius d'ici, car non supporté directement sur frame.
        hbox:
            spacing 10
            for card in POKER_GAME.community_cards:
                add card.get_image_name() size (80, 112)

    text "Pot: [POKER_GAME.pot]" style "POKER_TEXT": # CORRECTION: Style entre guillemets
        xalign 0.5
        yalign 0.45
        outlines [ (2, "#000000", 0, 0) ]

    fixed:
        $ human_player = POKER_GAME.players[0]
        vbox:
            xalign 0.5
            yalign 0.9
            spacing 5
            text "[human_player.name]":
                style "POKER_PLAYER_NAME" # CORRECTION: Style entre guillemets
                # CORRECTION: Utiliser 'color' au lieu de 'text_color'
                if human_player.is_dealer:
                    color "#FFD700"
                if human_player.is_small_blind:
                    color "#FFA07A"
                if human_player.is_big_blind:
                    color "#FF8C00"
            text "Jetons: [human_player.chips]" style "POKER_CHIP_TEXT" # CORRECTION: Style entre guillemets
            text "Mise: [human_player.current_bet]" style "POKER_CHIP_TEXT" # CORRECTION: Style entre guillemets
            hbox:
                spacing 5
                for card in human_player.hand:
                    add card.get_image_name() size (70, 98)

            # CORRECTION: Conditionnement du displayable text entier
            if human_player.has_folded:
                text "(FOLDED)" style "POKER_TEXT" color "#FF0000" # CORRECTION: Style entre guillemets
            if human_player.is_all_in:
                text "(ALL-IN)" style "POKER_TEXT" color "#00FF00" # CORRECTION: Style entre guillemets

        if len(POKER_GAME.players) > 1:
            $ ai_player_1 = POKER_GAME.players[1]
            vbox:
                xalign 0.5
                yalign 0.1
                spacing 5
                text "[ai_player_1.name]":
                    style "POKER_PLAYER_NAME" # CORRECTION: Style entre guillemets
                    # CORRECTION: Utiliser 'color' au lieu de 'text_color'
                    if ai_player_1.is_dealer:
                        color "#FFD700"
                    if ai_player_1.is_small_blind:
                        color "#FFA07A"
                    if ai_player_1.is_big_blind:
                        color "#FF8C00"
                text "Jetons: [ai_player_1.chips]" style "POKER_CHIP_TEXT" # CORRECTION: Style entre guillemets
                text "Mise: [ai_player_1.current_bet]" style "POKER_CHIP_TEXT" # CORRECTION: Style entre guillemets
                hbox:
                    spacing 5
                    for card in ai_player_1.hand:
                        # CORRECTION: Indenter les displayables sous les conditions
                        if game_debug_mode:
                            add card.get_image_name() size (60, 84)
                        else:
                            add "card_back" size (60, 84)
                # CORRECTION: Conditionnement du displayable text entier
                if ai_player_1.has_folded:
                    text "(FOLDED)" style "POKER_TEXT" color "#FF0000" # CORRECTION: Style entre guillemets
                if ai_player_1.is_all_in:
                    text "(ALL-IN)" style "POKER_TEXT" color "#00FF00" # CORRECTION: Style entre guillemets


    if POKER_GAME is not None and POKER_GAME.get_current_player() is not None:
        $ current_acting_player = POKER_GAME.get_current_player()
        if current_acting_player.is_human:
            frame:
                xalign 0.5
                yalign 0.98
                background "#000000CC"
                padding (20, 10)
                hbox:
                    spacing 15

                    textbutton "FOLD" action Return({"action": "fold"}):
                        style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                        tooltip "Abandonner la main actuelle."

                    $ amount_to_match_for_call = POKER_GAME.current_highest_bet - current_acting_player.current_bet
                    if current_acting_player.can_check(POKER_GAME.current_highest_bet):
                        textbutton "CHECK" action Return({"action": "check"}):
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                            tooltip "Passer le tour sans miser (si personne n'a misé)."
                    elif current_acting_player.can_call(POKER_GAME.current_highest_bet):
                        $ display_call_amount = min(amount_to_match_for_call, current_acting_player.chips)
                        textbutton "CALL ([display_call_amount])" action Return({"action": "call", "amount_needed": POKER_GAME.current_highest_bet}):
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                            sensitive current_acting_player.chips >= amount_to_match_for_call or current_acting_player.is_all_in
                            tooltip "Égaler la mise actuelle."
                    else:
                        textbutton "CHECK/CALL" action NullAction() sensitive False:
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets

                    $ min_bet_val = POKER_GAME.big_blind_val # Utilise la grosse blinde comme base pour la mise
                    $ min_raise_val = POKER_GAME.big_blind_val # Utilise la grosse blinde comme base pour la relance

                    if POKER_GAME.current_highest_bet == 0:
                        $ suggested_bet_amount = min(current_acting_player.chips, min_bet_val * 2)
                        textbutton "BET ([suggested_bet_amount])" action Return({"action": "bet", "amount_needed": suggested_bet_amount}):
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                            sensitive current_acting_player.chips >= suggested_bet_amount
                            tooltip "Faire une mise initiale."
                    elif current_acting_player.can_raise(POKER_GAME.current_highest_bet, min_raise_val):
                        $ amount_to_add_for_raise = (POKER_GAME.current_highest_bet - current_acting_player.current_bet) + min_raise_val
                        $ display_raise_to = POKER_GAME.current_highest_bet + min_raise_val
                        textbutton "RAISE ([display_raise_to])" action Return({"action": "raise", "amount_needed": POKER_GAME.current_highest_bet, "raise_by": min_raise_val}):
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                            sensitive current_acting_player.chips >= amount_to_add_for_raise
                            tooltip "Augmenter la mise actuelle."
                    else:
                        textbutton "BET/RAISE" action NullAction() sensitive False:
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets

                    if current_acting_player.chips > 0 and not current_acting_player.is_all_in:
                        textbutton "ALL-IN ([current_acting_player.chips])" action Return({"action": "all_in"}):
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets
                            tooltip "Miser tous vos jetons."
                    else:
                        textbutton "ALL-IN" action NullAction() sensitive False:
                            style "STYLE_CHOICE_BUTTON_LIME" # CORRECTION: Style entre guillemets

    use SC_POKER_INFORMATION(sMessage1, sMessage2)

screen SC_POKER_INFORMATION(sMessage1, sMessage2):
    frame:
        background "#404040AA"
        xalign 1.0
        yalign 0.01
        xsize 0.30
        ysize 0.12
        padding (10, 5)
        # CORRECTION: Supprimé xradius et yradius d'ici, car non supporté directement sur frame.
        hbox: # Un hbox ou vbox ici, si on veut mettre du contenu.
            vbox:
                text sMessage1 style "POKER_TEXT" size 22 # CORRECTION: Style entre guillemets
                text sMessage2 style "POKER_TEXT" size 20 # CORRECTION: Style entre guillemets

label start:
    "Bienvenue au Texas Hold'em!"

    $ POKER_GAME = poker.PokerGame(human_player_name=player_name, num_ai_players=1, card_image_base_path="images/cards/", small_blind_val=10, big_blind_val=20, initial_chips_val=200)
    "Préparez-vous pour une nouvelle partie avec [len(POKER_GAME.players) - 1] adversaire IA !"

    $ _rollback = False
    call LB_TEXAS_HOLDEM()
    $ _rollback = True

    "Merci d'avoir joué au Texas Hold'em !"
    return

label LB_TEXAS_HOLDEM():
    $ PokerHandsLoop = True
    while PokerHandsLoop:
        $ Current_Message_1 = f"Main #{POKER_GAME.num_hands_played + 1}"
        $ Current_Message_2 = "Nouvelle main en préparation..."
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.0

        $ players_remaining_in_game = POKER_GAME.get_players_remaining_in_game()
        if len(players_remaining_in_game) <= 1:
            $ final_winner = players_remaining_in_game[0] if players_remaining_in_game else None
            if final_winner:
                "Félicitations, [final_winner.name], vous avez remporté la partie !"
            else:
                "La partie est terminée, mais aucun vainqueur n'a pu être désigné."
            $ PokerHandsLoop = False
            jump LB_END_GAME # Sauter à la fin du jeu complet

        $ POKER_GAME.reset_hand()
        $ Current_Message_2 = f"Dealer: {POKER_GAME.players[POKER_GAME.dealer_index].name}"
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.0

        $ POKER_GAME.assign_blinds()
        $ Current_Message_2 = f"Petite Blinde: {POKER_GAME.small_blind_val}, Grosse Blinde: {POKER_GAME.big_blind_val}"
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.5

        $ POKER_GAME.deal_hole_cards()
        $ Current_Message_1 = "Cartes distribuées."
        $ human_player_hand_str = " ".join(str(c) for c in POKER_GAME.players[0].hand)
        $ Current_Message_2 = f"Vos cartes: [human_player_hand_str]"
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 2.0

        $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_PREFLOP
        $ Current_Message_1 = "Tour de mise: Pre-flop"
        $ Current_Message_2 = f"Pot: {POKER_GAME.pot}. Mise la plus haute: {POKER_GAME.current_highest_bet}"
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        call LB_BETTING_ROUND_LOGIC()

        # Débogage : Vérifier les joueurs actifs après le tour de mise
        $ current_players_in_hand_count = len(POKER_GAME.get_players_in_hand_for_showdown()) # Use new function
        $ print(f"DEBUG LB_TEXAS_HOLDEM: Players in hand after betting round ({POKER_GAME.game_state}): {current_players_in_hand_count}")
        if current_players_in_hand_count <= 1:
            $ print(f"DEBUG LB_TEXAS_HOLDEM: Only one player in hand or less. Jumps to hand_end.")
            jump LB_HAND_END

        $ Current_Message_1 = "Tour de mise: Flop"
        $ Current_Message_2 = "Distribution du Flop..."
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.0
        $ POKER_GAME.deal_community_cards(3)
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.5
        $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_FLOP
        call LB_BETTING_ROUND_LOGIC()

        $ current_players_in_hand_count = len(POKER_GAME.get_players_in_hand_for_showdown()) # Use new function
        $ print(f"DEBUG LB_TEXAS_HOLDEM: Players in hand after betting round ({POKER_GAME.game_state}): {current_players_in_hand_count}")
        if current_players_in_hand_count <= 1:
            $ print(f"DEBUG LB_TEXAS_HOLDEM: Only one player in hand or less. Jumps to hand_end.")
            jump LB_HAND_END

        $ Current_Message_1 = "Tour de mise: Turn"
        $ Current_Message_2 = "Distribution du Turn..."
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.0
        $ POKER_GAME.deal_community_cards(1)
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.5
        $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_TURN
        call LB_BETTING_ROUND_LOGIC()

        $ current_players_in_hand_count = len(POKER_GAME.get_players_in_hand_for_showdown()) # Use new function
        $ print(f"DEBUG LB_TEXAS_HOLDEM: Players in hand after betting round ({POKER_GAME.game_state}): {current_players_in_hand_count}")
        if current_players_in_hand_count <= 1:
            $ print(f"DEBUG LB_TEXAS_HOLDEM: Only one player in hand or less. Jumps to hand_end.")
            jump LB_HAND_END

        $ Current_Message_1 = "Tour de mise: River"
        $ Current_Message_2 = "Distribution de la River..."
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.0
        $ POKER_GAME.deal_community_cards(1)
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 1.5
        $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_RIVER
        call LB_BETTING_ROUND_LOGIC()

        $ current_players_in_hand_count = len(POKER_GAME.get_players_in_hand_for_showdown()) # Use new function
        $ print(f"DEBUG LB_TEXAS_HOLDEM: Players in hand after betting round ({POKER_GAME.game_state}): {current_players_in_hand_count}")
        if current_players_in_hand_count <= 1:
            $ print(f"DEBUG LB_TEXAS_HOLDEM: Only one player in hand or less. Jumps to hand_end.")
            jump LB_HAND_END


        label LB_SHOWDOWN():
             $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_SHOWDOWN
             $ Current_Message_1 = "Showdown !"
             $ Current_Message_2 = "Dévoilement des mains des joueurs restants..."
             show screen SC_POKER(Current_Message_1, Current_Message_2)
             pause 2.0

             $ winners, winning_desc = POKER_GAME.determine_winner()
             $ Current_Message_1 = "Résultats de la main :"
             $ Current_Message_2 = winning_desc
             show screen SC_POKER(Current_Message_1, Current_Message_2)
             pause 3.0

             $ POKER_GAME.distribute_pot(winners)
             # NOUVEAU: Message de confirmation après distribution du pot
             $ Current_Message_1 = "Pot distribué !"
             $ Current_Message_2 = f"Le pot est maintenant de {POKER_GAME.pot} et vos jetons: {POKER_GAME.players[0].chips}."
             show screen SC_POKER(Current_Message_1, Current_Message_2)
             " ... PAUSE ..." # Ceci met le jeu en pause et attend un clic du joueur

        label LB_HAND_END():
             $ print(f"DEBUG LB_TEXAS_HOLDEM: Entering hand_end. Pot before cleanup: {POKER_GAME.pot}")
             # If the hand ends by a fold (before showdown), the pot must still be distributed
             $ players_for_win = POKER_GAME.get_players_in_hand_for_showdown() # Use new function
             if len(players_for_win) == 1:
                 $ winner_by_fold = players_for_win[0]
                 $ print(f"DEBUG LB_TEXAS_HOLDEM: {winner_by_fold.name} is the only player in hand. S/he should win the pot.")
                 # Assurez-vous que le pot est collecté avant de déterminer le gagnant ici.
                 # Cela devrait déjà être fait à la fin de betting_round_logic, mais double-vérification.
                 $ POKER_GAME.collect_bets_to_pot() # Repeated to ensure if the jump bypassed the final collection
                 $ POKER_GAME.distribute_pot([winner_by_fold])
                 $ current_message_1 = f"End of hand. {winner_by_fold.name} wins by default!"
                 $ current_message_2 = f"Chips of {winner_by_fold.name}: {winner_by_fold.chips}"
                 show screen SC_POKER(Current_Message_1, Current_Message_2)
                 " ... PAUSE ..." # Ceci met le jeu en pause et attend un clic du joueur
             else:
                 $ print(f"DEBUG LB_TEXAS_HOLDEM: End of hand without single winner by fold (number of players in hand: {len(players_for_win)}).")

             $ POKER_GAME.game_state = poker.PokerGame.GAME_STATE_END_HAND
             $ Current_Message_1 = "Fin de la main."
             $ Current_Message_2 = "Préparation de la prochaine main..."
             show screen SC_POKER(Current_Message_1, Current_Message_2)
             pause 2.0

             $ players_eliminated_this_hand = [p for p in POKER_GAME.players if p.chips <= 0]
             if players_eliminated_this_hand:
                $ Current_Message_1 = "Joueurs éliminés :"
                $ Current_Message_2 = ", ".join([p.name for p in players_eliminated_this_hand]) + " n'ont plus de jetons !"
                show screen SC_POKER(Current_Message_1, Current_Message_2)
                pause 2.0

    label LB_END_GAME():
        return

label LB_BETTING_ROUND_LOGIC():
    $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Début du tour de mise. État: {POKER_GAME.game_state}. Pot: {POKER_GAME.pot}. Mise la plus haute: {POKER_GAME.current_highest_bet}")
    $ POKER_GAME.start_betting_round()
    $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Après start_betting_round. Pot: {POKER_GAME.pot}. Mise la plus haute: {POKER_GAME.current_highest_bet}")

    # La boucle while continuera tant que le tour de mise n'est pas terminé
    while not POKER_GAME.is_betting_round_over():
        $ current_player = POKER_GAME.get_next_player_to_act()

        if current_player is None:
            $ print("DEBUG LB_BETTING_ROUND_LOGIC(): current_player est None. Tour de mise terminé (ou aucun joueur ne doit agir).")
            jump betting_round_loop_end

        $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Au tour de {current_player.name} (humain: {current_player.is_human}). Jetons: {current_player.chips}. Mise actuelle: {current_player.current_bet}")
        $ Current_Message_1 = f"Au tour de [current_player.name]."
        $ Current_Message_2 = f"Mise à égaler: {POKER_GAME.current_highest_bet}. Jetons: {current_player.chips}"
        show screen SC_POKER(Current_Message_1, Current_Message_2)
        if current_player.is_human:
            "C'est votre tour."
            $ player_action_result = ui.interact()
            $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Action du joueur humain: {player_action_result['action']}")
            $ chosen_action = player_action_result["action"]
            $ amount_needed_for_action = player_action_result.get("amount_needed", POKER_GAME.current_highest_bet)
            $ raise_by_amount = player_action_result.get("raise_by", 0)

            $ bet_amount_paid = current_player.perform_action(chosen_action, amount_needed=amount_needed_for_action, raise_amount=raise_by_amount)
            # LIGNE SUPPRIMÉE: $ POKER_GAME.pot += bet_amount_paid
            $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Humain a misé {bet_amount_paid}. Pot total: {POKER_GAME.pot}. Mise la plus haute: {POKER_GAME.current_highest_bet}")

            if chosen_action in ["bet", "raise"]:
                $ POKER_GAME.current_highest_bet = current_player.current_bet
                $ POKER_GAME.last_raiser_index = POKER_GAME.players.index(current_player)

        else:
            "C'est au tour de [current_player.name] (IA)."
            $ ai_decision = current_player.decide_action(
                POKER_GAME.current_highest_bet,
                POKER_GAME.pot,
                len(POKER_GAME.get_players_in_hand_for_showdown()), # Use players in hand for AI decision context
                POKER_GAME.community_cards,
                POKER_GAME.small_blind_val,
                POKER_GAME.big_blind_val
            )
            $ chosen_action = ai_decision["action"]
            $ amount_needed_for_action = ai_decision.get("amount_needed", POKER_GAME.current_highest_bet)
            $ raise_by_amount = ai_decision.get("raise_by", 0)

            $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): IA {current_player.name} action: {chosen_action}")
            $ bet_amount_paid = current_player.perform_action(chosen_action, amount_needed=amount_needed_for_action, raise_amount=raise_by_amount)
            # LIGNE SUPPRIMÉE: $ POKER_GAME.pot += bet_amount_paid
            $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): IA a misé {bet_amount_paid}. Pot total: {POKER_GAME.pot}. Mise la plus haute: {POKER_GAME.current_highest_bet}")

            if chosen_action in ["bet", "raise"]:
                $ POKER_GAME.current_highest_bet = current_player.current_bet
                $ POKER_GAME.last_raiser_index = POKER_GAME.players.index(current_player)

            show screen SC_POKER(Current_Message_1, Current_Message_2)
            pause 1.5

        show screen SC_POKER(Current_Message_1, Current_Message_2)
        pause 0.5

    # Le code après la boucle while (collect_bets_to_pot, messages de fin de tour)

    # Le label pour la sortie anticipée de la boucle
    label betting_round_loop_end:

    $ print(f"DEBUG LB_BETTING_ROUND_LOGIC(): Boucle du tour de mise terminée. Appel de collect_bets_to_pot().")
    $ POKER_GAME.collect_bets_to_pot()
    $ Current_Message_1 = "Tour de mise terminé."
    $ Current_Message_2 = f"Pot total: {POKER_GAME.pot}"
    show screen SC_POKER(Current_Message_1, Current_Message_2)
    pause 1.0

    return
