# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global variables
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
define DEALER               = ""
define SMALL_BLIND          = 5                                                                                             # ═══► Small Blind
define BIG_BLIND            = 10                                                                                            # ═══► Big Blind
define POKER_AI_AGGRESSION  = 3                                                                                             # ═══► IA agressivity level (1=passive - 5=very agressive)
define PLAYER_FOLD          = False

define POKER_CHEAT          = False

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global Text Style
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
style STYLE_CHOICE_BUTTON_LIME:
    font "Futura.ttc"
    size 32
    idle_color "#FFFFFF"
    hover_color "#00FF00"
    insensitive_color "#808080"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]
# End style
style STYLE_CHOICE_BUTTON_ORANGE:
    font "Futura.ttc"
    size 32
    idle_color "#FFFFFF"
    hover_color "#FF6600"
    insensitive_color "#808080"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]
# End style
style STYLE_CHOICE_BUTTON_RED:
    font "Futura.ttc"
    size 32
    idle_color "#FFFFFF"
    hover_color "#FF0000"
    insensitive_color "#808080"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]
# End style

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Python code block for Texas Hold'Em Classes
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
init python:
    import random
    from collections import Counter

    RANK_VALUES = {'2': 2,
                   '3': 3,
                   '4': 4,
                   '5': 5,
                   '6': 6,
                   '7': 7,
                   '8': 8,
                   '9': 9,
                   'T': 10,
                   'J': 11,
                   'Q': 12,
                   'K': 13,
                   'A': 14}
    HAND_VALUES = ["High Card",
                   "One Pair",
                   "Two Pair",
                   "Three of a Kind",
                   "Straight",
                   "Flush",
                   "Full House",
                   "Four of a Kind",
                   "Straight Flush"]

    class CL_PLAYER:
        # ► Description:
        # ►     Represents a player in the game, storing their attributes and managing their state during gameplay.
        # ► Attributes:
        # ►     name (str): The player's name.
        # ►     chips (int): The player's current chip balance.
        # ►     hand (list): The player's current hand (two cards).
        # ►     currentBet (int): The amount the player has bet in the current round.
        # ►     isFolded (bool): Indicates whether the player has folded in the current round.
        # ► Methods:
        # ►     resetBet(): Resets the player's bet to zero for the next round.
        # ►     fold(): Marks the player as having folded.
        # ►     resetForNewHand(): Prepares the player's state for a new hand.
        def __init__(self, name, chips):
            self.name       = name                                                                                          # ═══► The player's name
            self.chips      = chips                                                                                         # ═══► The player's chip balance
            self.hand       = []                                                                                            # ═══► The player's hand (two cards)
            self.currentBet = 0                                                                                             # ═══► The player's current bet
            self.isFolded   = False                                                                                         # ═══► Tracks if the player has folded
        # End def
        def resetBet(self):
            self.currentBet = 0
        # End def
        def fold(self):
            self.isFolded   = True
        # End def
        def resetForNewHand(self):
            self.hand       = []                                                                                            # ═══► Clears the player's hand
            self.currentBet = 0                                                                                             # ═══► Resets the current bet
            self.isFolded   = False                                                                                         # ═══► Resets the fold status
        # End def
    # End class
    class CL_DECK:
        # ► Description:
        # ►      Represents a deck of playing cards with functionality for shuffling and drawing cards.
        # ►      The deck contains 52 cards, one for each combination of ranks ('2'-'A') and suits ('C', 'D', 'H', 'S').
        # ►      Raises a ValueError if an invalid rank is detected during initialization.
        # ► Methods:
        # ►     draw(count): Draws a specified number of cards from the top of the deck and returns them.
        # ► Attributes:
        # ►     count (int): The number of cards to draw.
        # ► Returns:
        # ►      list: A list of dictionaries representing the drawn cards, each with 'suit' and 'rank'.
        # ► Notes:
        # ►      The drawn cards are removed from the deck.
        def __init__(self):
            suits = ['C', 'D', 'H', 'S']
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
            self.cards = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
            random.shuffle(self.cards)
            rank_order = '23456789TJQKA'
            for card in self.cards:
                if card['rank'] not in rank_order:
                    raise ValueError(f"Invalid rank found in deck: {card['rank']}")
                # End if
            # End for
        # End def
        def draw(self, count):
            drawn_cards = self.cards[:count]
            self.cards = self.cards[count:]
            return drawn_cards
        # End def
    # End class
    def INITIALIZE_GAME(sHuman, sRobot, iChips): # Augmenté les jetons pour plus de parties
        global human, robot, pot, cards_open, active_players
        human           = CL_PLAYER(sHuman, iChips)
        robot           = CL_PLAYER(sRobot, iChips)
        pot             = 0
        cards_open      = []
        active_players  = [human, robot]                                                                                    # ═══► List of players still in the game for the round
        DECK_RESET()
    # End def
    def APPLY_BET(player_obj, total_bet_amount_desired):
        # ► Adjusts the player's bet to meet the desired total bet amount and updates the game state.
        # ► Args:
        # ►     player_obj: An object representing the player. Must have attributes `chips` (int) and `currentBet` (int).
        # ►     total_bet_amount_desired (int): The desired total bet amount for the player in the current round.
        # ► Returns:
        # ►     int: The actual amount added to the pot during this action.
        global pot
        amount_to_add = total_bet_amount_desired - player_obj.currentBet                                                    # ═══► Calculate the amount to add to the bet. It's the difference between the desired bet and the current bet.
        if amount_to_add < 0: amount_to_add = 0 # Shouldn't happen with correct logic
        # End if
        if amount_to_add > player_obj.chips:
            amount_to_add = player_obj.chips                                                                                # ═══► Go all-in
        # End if
        player_obj.chips -= amount_to_add
        player_obj.currentBet += amount_to_add
        pot += amount_to_add
        return amount_to_add                                                                                                # ═══► Return actual amount put into the pot in this action
    # End def
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Function used for every betting rounds
    # ╰─────────────────────────────────────────────────────────────────────────
    def BETTING_ROUND_LOGIC(first_player_obj, initial_bet, street_name, num_community_cards_revealed):
        # ► Handles the betting logic for a round of Texas Hold'em.
        # ► Args:
        # ►     first_player_obj: The player object (human or robot) who acts first in the round.
        # ►     initial_bet (int): The starting bet amount for the round.
        # ►     street_name (str): The stage of the game (e.g., "Pre-Flop", "Flop", "Turn", "River").
        # ►     num_community_cards_revealed (int): Number of community cards currently revealed on the table.
        # ► Global Variables:
        # ►     pot (int): The current total pot size.
        # ►     human (Player): The human player object.
        # ►     robot (Player): The AI-controlled player object.
        # ►     active_players (list): A list of players who have not folded and still have chips.
        # ► Behavior:
        # ►     - Resets player bets if not in "Pre-Flop".
        # ►     - Determines the order of play based on the first player.
        # ►     - Manages player actions (fold, check, call, bet, raise) and updates game state accordingly.
        # ►     - Ends the round when betting conditions are satisfied (e.g., all players have matched bets or only one player remains).
        global pot, human, robot, active_players

        current_highest_bet         = initial_bet
        last_raiser                 = None
        players_who_acted_in_round  = set()

        print(f"[DEBUG] ► Street name: {street_name}")
        if street_name != "Pre-Flop":
            human.resetBet()
            robot.resetBet()
            active_players = [p for p in [human, robot] if not p.isFolded and p.chips > 0]
        else:                                                                                                               # ═══► Pre-Flop, blinds already set currentBet, so add them to players_who_acted_in_round
            if human.currentBet > 0:
                players_who_acted_in_round.add(human)
            # End if
            if robot.currentBet > 0:
                players_who_acted_in_round.add(robot)
            # End if
        # End if
        order_of_play = []
        if first_player_obj == human:
            order_of_play = [human, robot]
        else:
            order_of_play = [robot, human]
        # End if
        print(f"[DEBUG] ► First player: {first_player_obj.name}")
        round_completed = False
        while not round_completed:
            # CHECK FOR EARLY ROUND END DUE TO FOLD
            print(f"[DEBUG] ► Active players (1): {len(active_players)}")
            if len(active_players) <= 1:
                # ► If only one player is left, the round ends.
                # ► The remaining player wins the pot.
                print(f"[DEBUG] ► Round ended early by fold. Active players: {len(active_players)}")
                round_completed = True                                                                                      # ═══► Indicate that the round ended by a fold
            # End if
            for p_turn in order_of_play:
                print(f"[DEBUG] ► Player turn: {p_turn.name}")
                if not p_turn.isFolded and p_turn.chips > 0 and not len(active_players) <= 1:
                    # ► GET_AMOUNT_TO_MATCH returns what the player has to ADD.
                    # ► current_highest_bet is the TOTAL AMOUNT to reach.
                    amount_to_match = GET_AMOUNT_TO_MATCH(p_turn, current_highest_bet)
                    print(f"[DEBUG] ► Amount to match: {amount_to_match}")
                    needs_to_act = True
                    if (p_turn.currentBet == current_highest_bet and p_turn in players_who_acted_in_round):
                        needs_to_act = False
                    elif p_turn.chips == 0:
                        needs_to_act = False
                    # End if
                    print(f"[DEBUG] ► Needs to act: {needs_to_act}")
                    if needs_to_act:
                        print(f"[DEBUG] ► Turn: {p_turn.name} --► Active players: {len(active_players)}")
                        if p_turn == human:
                            player_action_data = renpy.call_screen("SC_HUMAN_CHOICES", street_name, pot, current_highest_bet, human.chips, human.currentBet, amount_to_match, BIG_BLIND)
                            action_type = player_action_data["action"]
                            chosen_amount = player_action_data.get("amount", 0)
                            print(f"[DEBUG] ► Player Action Data: {player_action_data}")
                            if action_type == "fold":
                                human.fold()
                                active_players.remove(human)
                                print(f"[DEBUG] ► Current action: {action_type} --► Active players: {len(active_players)}")
                                renpy.say(None, "\n\nYou decided to fold.")
                            elif action_type == "check":
                                players_who_acted_in_round.add(human)
                                print(f"[DEBUG] ► Current action: {action_type}")
                                renpy.say(None, "\n\nYou checked.")
                            elif action_type == "call":
                                actual_bet = APPLY_BET(human, chosen_amount)                                                # ═══► Here, chosen_amount is already current_highest_bet_val (the total amount)
                                print(f"[DEBUG] ► Current action: {action_type} --► Actual bet: {actual_bet}")
                                if human.currentBet < current_highest_bet:                                                  # ═══► Check if the player is all-in
                                    renpy.say(None, f"\n\nYou don't have enough chips. You call all-in for {actual_bet} chips.")
                                    action_type = "all-in"
                                else:
                                    renpy.say(None, f"\n\nYou follow for {actual_bet} chips.")
                                # End if
                                players_who_acted_in_round.add(human)
                            elif action_type == "bet":
                                actual_bet = APPLY_BET(human, chosen_amount)
                                current_highest_bet = human.currentBet
                                last_raiser = human
                                print(f"[DEBUG] ► Current action: {action_type} --► Last Raiser: {last_raiser.name}")
                                renpy.say(None, f"\n\nYou bet {actual_bet} chips. Highest bet is {current_highest_bet} chips.")
                                players_who_acted_in_round = set([human])
                            elif action_type == "raise":
                                actual_bet = APPLY_BET(human, chosen_amount)
                                raised_by = actual_bet - (current_highest_bet - amount_to_match)                            # ═══► Amount of the raise (what has been added above the call)
                                # ► amount_to_match is the difference. The previous bet was current_highest_bet - amount_to_match.
                                # ► raised_by is actual_bet minus (current_highest_bet_val - (current_highest_bet_val - human.currentBet_before_action))
                                raised_by = actual_bet - (current_highest_bet - amount_to_match)                            # ◀═══ Correction of raised_by calculation
                                current_highest_bet = human.currentBet
                                last_raiser = human
                                print(f"[DEBUG] ► Current action: {action_type} --► Last Raiser: {last_raiser.name} ----► Current bet: {human.currentBet}")
                                renpy.say(None, f"\n\nYou raise by {raised_by} chips (total: {current_highest_bet} chips).")
                                players_who_acted_in_round = set([human])
                            # End if
                        elif p_turn == robot:
                            ai_action, ai_total_bet_amount = DECIDE_ACTION_AI(
                                robot.hand, cards_open, current_highest_bet,                                                # ◀═══ Here, pass current_highest_bet as `current_bet_to_match`
                                robot.chips, human.chips, POKER_AI_AGGRESSION, num_community_cards_revealed
                            )
                            print(f"[DEBUG] ► Robot action: {ai_action} --► Robot total bet amount: {ai_total_bet_amount}")
                            if ai_action == "fold":
                                robot.fold()
                                active_players.remove(robot)
                                print(f"[DEBUG] ► Current action: {ai_action} --► Active players: {len(active_players)}")
                                renpy.say(None, f"\n\n{robot.name} decided to fold.")
                            elif ai_action == "check":
                                players_who_acted_in_round.add(robot)
                                print(f"[DEBUG] ► Current action: {ai_action}")
                                renpy.say(None, f"\n\n{robot.name} checked.")
                            elif ai_action == "call":
                                actual_bet = APPLY_BET(robot, ai_total_bet_amount)                                          # ═══► ai_total_bet_amount is already the total amount that the AI wants to have bet
                                print(f"[DEBUG] ► Current action: {ai_action} --► Actual bet: {actual_bet}")
                                if robot.currentBet < current_highest_bet:                                                  # ═══► If all-in
                                    renpy.say(None, f"{robot.name} is all-in for {actual_bet} chips.")
                                    ai_action = "all-in"
                                else:
                                    renpy.say(None, f"{robot.name} follows for {actual_bet} chips.")
                                # End if
                                players_who_acted_in_round.add(robot)
                            elif ai_action == "bet":
                                actual_bet = APPLY_BET(robot, ai_total_bet_amount)
                                current_highest_bet = robot.currentBet
                                last_raiser = robot
                                print(f"[DEBUG] ► Current action: {ai_action} --► Last Raiser: {last_raiser.name}")
                                renpy.say(None, f"{robot.name} bet {actual_bet} chips. Highest bet is {current_highest_bet} chips.")
                                players_who_acted_in_round = set([robot])
                            elif ai_action == "raise":
                                actual_bet = APPLY_BET(robot, ai_total_bet_amount)
                                raised_by = actual_bet - amount_to_match # Montant de la relance (ce qui a été rajouté au-dessus du call)
                                current_highest_bet = robot.currentBet
                                last_raiser = robot
                                print(f"[DEBUG] ► Current action: {ai_action} --► Last Raiser: {last_raiser.name} ----► Current bet: {robot.currentBet}")
                                renpy.say(None, f"{robot.name} relance de {raised_by} jetons (total : {current_highest_bet} jetons).")
                                players_who_acted_in_round = set([robot])
                            # End if
                        # End if
                        renpy.show_screen("SC_HAND_HUMAN")
                        renpy.show_screen("SC_HAND_ROBOT", reveal=False)
                        renpy.show_screen("SC_OPEN_CARDS")
                        renpy.pause(0.5)
                    # End if
                # End if
            # End for
            all_matched = True                                                                                              # ═══► End-of-turn condition for normal bets (not by a premature fold)
            for p_check in active_players:
                if p_check.currentBet < current_highest_bet and p_check.chips > 0:
                    all_matched = False
                    break
                # End if
            # End for
            # ► This condition must check that all the active players have bet the same amount, and that all those who had to act after the last raise (or since the start of the round) have done so.
            # ► For two players, if `all_matched` is True, then both have either checked or called, or one has raised and the other has called.
            # ► The complexity arises if one player raises, the other calls, but the first must still act if there has been an over-raise.
            # ► Since `players_who_acted_in_round` resets each time it is relaunched, `len(players_who_acted_in_round) == len(active_players)` should be sufficient for most cases, if `active_players` has been correctly updated with the folds.
            if all_matched and len(players_who_acted_in_round) == len(active_players):
                round_completed = True
            # End if
            print(f"[DEBUG] ► End of loop conditions: all_matched = {all_matched}, len(players_who_acted_in_round) = {len(players_who_acted_in_round)}, len(active_players) = {len(active_players)}")
        # End while

        # ► Gérer le pot et le retour après la boucle while.
        # ► Cette section ne sera atteinte que si `round_completed` devient True sans qu'un `return True` prématuré ne soit appelé pour un fold.
        print(f"[DEBUG] ► Active players (2): {len(active_players)}")
        if len(active_players) <= 1:
            winner_of_round = active_players[0] if active_players else None
            print(f"[DEBUG] ► Winner: {winner_of_round.name}")
            if winner_of_round == human:
                renpy.say(None, f"\n\n{robot.name} have folded. You win the pot of {pot} chips!")
                human.chips += pot
                pot = 0
                return True
            elif winner_of_round == robot:
                renpy.say(None, f"\n\n{winner_of_round.name} has won the pot of {pot} chips because you have folded!")
                robot.chips += pot
                pot = 0
                return True
            else:
                renpy.say(None, f"\n\nThere are no more active players in the hand. Split pot or error!!")
                return True                                                                                                 # ═══► Should not happen in 2-player game if active_players is empty
            # End if
        else:
            renpy.say(None, f"\n\nThe {street_name} betting round is over.")
            return False                                                                                                    # ═══► Round completed normally (all calls/checks), not by fold
        # End if
    # End def
    def BLINDS(dealer_position):
        global pot
        small_blind_player  = None
        big_blind_player    = None
        if dealer_position == "human":                                                                                      # ═══► Human is dealer, Robot is small blind, Human is big blind (for 2 players)
            small_blind_player  = robot
            big_blind_player    = human
        else:                                                                                                               # ═══► Robot is dealer, Human is small blind, Robot is big blind
            small_blind_player  = human
            big_blind_player    = robot
        # End if
        amount_sb = min(small_blind_player.chips, SMALL_BLIND)                                                              # ═══► Pay Small Blind
        small_blind_player.chips -= amount_sb
        small_blind_player.currentBet += amount_sb
        pot += amount_sb
        print(f"[DEBUG] ► " + small_blind_player.name + " puts in the small blind of " + str(amount_sb) + " chips ")
        amount_bb = min(big_blind_player.chips, BIG_BLIND)                                                                  # ═══► Pay Big Blind
        big_blind_player.chips -= amount_bb
        big_blind_player.currentBet += amount_bb
        pot += amount_bb
        print(f"[DEBUG] ► " + big_blind_player.name + " puts the big blind of " + str(amount_bb) + " chips ")
        renpy.show_screen("SC_POKER_INFORMATION", small_blind_player.name + " pays the small blind of [SMALL_BLIND] chips.", big_blind_player.name + " pays the big blind of [BIG_BLIND] chips.")
        return big_blind_player                                                                                             # ═══► The big blind player is usually the last to act pre-flop, starting the action post-flop
    # End def
    def CARDS_DEAL():
        human.hand = deck.draw(2)
        robot.hand = deck.draw(2)
    # End def
    def CARDS_IMAGE(card):
        return f"cards/{card['rank']}{card['suit']}.png"
    # End def
    def CARDS_PLAYERS_RESET():
        human.resetForNewHand()
        robot.resetForNewHand()
        global active_players
        active_players = [p for p in [human, robot] if p.chips > 0]                                                         # ═══► Reset active players
        print(f"[DEBUG] ► Reset active players' cards")
    # End def
    def CARDS_OPEN_RESET():
        global cards_open
        cards_open = []
        print(f"[DEBUG] ► Reset open cards")
    # End def
    def CARDS_OPEN_REVEAL(count):
        cards_open.extend(deck.draw(count))
    # End def
    def DECK_RESET():
        global deck
        deck = CL_DECK()
    # End def
    def DEALER_RANDOM():
        dealer_position = renpy.random.choice(["human", "robot"])
        print(f"[DEBUG] ► Dealer defined for this round: " + dealer_position)
        return dealer_position
    # End def
    def DEALER_SWITCH(current_dealer):
        print(f"[DEBUG] ► Current dealer before change: " + current_dealer)
        next_dealer = "robot" if current_dealer == "human" else "human"
        print(f"[DEBUG] ► Current dealer after change: " + next_dealer)
        return next_dealer
    # End def
    def GET_AMOUNT_TO_MATCH(player_obj, highest_bet_in_round):                                                              # ═══► Helper to calculate the amount you need to track.
        return highest_bet_in_round - player_obj.currentBet
    # End def
    def POT_RESET(int_Pot=0):
        global pot
        pot = int_Pot
    # End def
    def RANK_TO_VALUE(rank):
        return RANK_VALUES.get(rank, 0)
    # End def
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Evaluates hand and determines its strength
    # ╰─────────────────────────────────────────────────────────────────────────
    def HAND_EVALUATE(hand, cards_open):
        # ► Combines the player's hand and the open cards to evaluate the strongest poker hand.
        # ► Args:
        # ►     hand (list): A list of dictionaries representing the player's cards. Each card has 'rank' and 'suit'.
        # ►     cards_open (list): A list of dictionaries representing the open community cards on the table.
        # ► Returns:
        # ►     tuple: A tuple indicating the strength of the hand. The first element is the hand rank (based on HAND_VALUES),
        # ►            followed by tie-breaker values like high card, pair rank, or kickers, depending on the hand type.
        combined = hand + list(cards_open)
        rank_counts = Counter(card['rank'] for card in combined)
        suit_counts = Counter(card['suit'] for card in combined)
        def find_ranks_by_count(count):
            # ► Finds ranks that occur exactly 'count' times and sorts them in descending order of value.
            # ► Args:
            # ►     count (int): The number of occurrences to match.
            # ► Returns:
            # ►     list: A sorted list of ranks matching the count.
            return sorted([RANK_TO_VALUE(r) for r, c in rank_counts.items() if c == count], reverse=True)
        # End def
        def get_kickers(exclude_ranks_list):                                                                                # ═══► Pay Changed parameter name to avoid confusion
            # ► Calculates the kickers by removing specified ranks from the combined cards.
            # ► Args:
            # ►     exclude_ranks_list (list): A list of rank values to exclude from consideration.
            # ► Returns:
            # ►     list: A sorted list of remaining ranks in descending order.
            all_ranks_values = sorted([RANK_TO_VALUE(card['rank']) for card in combined], reverse=True)
            temp_all_ranks = list(all_ranks_values)#                                                                        # ═══► Create a temporary list to remove excluded ranks
            for r in exclude_ranks_list:
                if r in temp_all_ranks:
                    temp_all_ranks.remove(r)
                # End if
            # End for
            return sorted(temp_all_ranks, reverse=True)
        # End def
        flush_suit = None                                                                                                   # ═══► Check for Flush
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
            # End if
        # End for
        is_flush = (flush_suit is not None)
        unique_ranks_values = sorted(list(set(RANK_TO_VALUE(card['rank']) for card in combined)), reverse=True)             # ═══► Check for Straight
        if 14 in unique_ranks_values:                                                                                       # ═══► Add Ace as 1 for A-2-3-4-5 straight
            unique_ranks_values.append(1)
        # End if
        unique_ranks_values.sort(reverse=True)
        straight_high_card = 0
        for i in range(len(unique_ranks_values) - 4):
            if unique_ranks_values[i] - unique_ranks_values[i+4] == 4 and \
                all(r in unique_ranks_values for r in range(unique_ranks_values[i+4], unique_ranks_values[i]+1)):           # ═══► Ensure all intermediate cards exist
                straight_high_card = unique_ranks_values[i]
                break
            # End if
        # End for
        is_straight = (straight_high_card > 0)
        four_of_a_kind_ranks = find_ranks_by_count(4)                                                                       # ═══► Evaluate hand strength and return with tie-breakers
        three_of_a_kind_ranks = find_ranks_by_count(3)
        pairs_ranks = find_ranks_by_count(2)
        if is_straight and is_flush:                                                                                        # ═══► Get the straight-flush high card
            flush_ranks_in_order = sorted([RANK_TO_VALUE(card['rank']) for card in combined if card['suit'] == flush_suit], reverse=True)
            if 14 in flush_ranks_in_order: # Add Ace as 1 for A-2-3-4-5 straight flush
                flush_ranks_in_order.append(1)
            # End if
            flush_ranks_in_order.sort(reverse=True)
            sf_high_card = 0
            for i in range(len(flush_ranks_in_order) - 4):
                if flush_ranks_in_order[i] - flush_ranks_in_order[i+4] == 4 and \
                    all(r in flush_ranks_in_order for r in range(flush_ranks_in_order[i+4], flush_ranks_in_order[i]+1)):
                    sf_high_card = flush_ranks_in_order[i]
                    break
                # End if
            # End for
            if sf_high_card == 0 and 14 in flush_ranks_in_order and all(r in flush_ranks_in_order for r in [2,3,4,5]):
                sf_high_card = 5 # A-2-3-4-5 straight flush
            # End if
            return (HAND_VALUES.index("Straight Flush"), sf_high_card)
        elif four_of_a_kind_ranks:
            quad_rank = four_of_a_kind_ranks[0]
            kicker = get_kickers([quad_rank] * 4)                                                                           # ═══► Exclude all 4 for kicker calculation
            return (HAND_VALUES.index("Four of a Kind"), quad_rank, *(kicker[:1]))                                          # ═══► Need only 1 kicker
        elif three_of_a_kind_ranks and pairs_ranks:
            three_of_a_kind_ranks.sort(reverse=True)                                                                        # ═══► Sort triples and pairs to pick the best full house
            pairs_ranks.sort(reverse=True)
            full_house_3_rank = three_of_a_kind_ranks[0]
            full_house_2_rank = 0
            for p_rank in pairs_ranks:                                                                                      # ═══► Prioritize pairs
                if p_rank != full_house_3_rank:
                    full_house_2_rank = p_rank
                    break
                # End if
            # End for
            if full_house_2_rank == 0 and len(three_of_a_kind_ranks) > 1:                                                   # ═══► If no separate pair, try to use a second triple for the pair part (e.g., KKKQQQ -> KKKQQ)
                full_house_2_rank = three_of_a_kind_ranks[1]
            # End if
            return (HAND_VALUES.index("Full House"), full_house_3_rank, full_house_2_rank)
        elif is_flush:
            flush_cards_values = sorted([RANK_TO_VALUE(card['rank']) for card in combined if card['suit'] == flush_suit], reverse=True)
            return (HAND_VALUES.index("Flush"), *flush_cards_values[:5])
        elif is_straight:
            return (HAND_VALUES.index("Straight"), straight_high_card)
        elif three_of_a_kind_ranks:
            triple_rank = three_of_a_kind_ranks[0]
            kickers = get_kickers([triple_rank] * 3)
            return (HAND_VALUES.index("Three of a Kind"), triple_rank, *(kickers[:2]))
        elif len(pairs_ranks) >= 2:
            pairs_ranks.sort(reverse=True)
            pair1_rank = pairs_ranks[0]
            pair2_rank = pairs_ranks[1]
            kickers = get_kickers([pair1_rank] * 2 + [pair2_rank] * 2)
            return (HAND_VALUES.index("Two Pair"), pair1_rank, pair2_rank, *(kickers[:1]))
        elif len(pairs_ranks) == 1:
            pair_rank = pairs_ranks[0]
            kickers = get_kickers([pair_rank] * 2)
            return (HAND_VALUES.index("One Pair"), pair_rank, *(kickers[:3]))
        else:
            high_cards = sorted([RANK_TO_VALUE(card['rank']) for card in combined], reverse=True)[:5]
            return (HAND_VALUES.index("High Card"), *high_cards)
        # End if
    # End def
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Compares the evaluated poker human and robot hands
    # ╰─────────────────────────────────────────────────────────────────────────
    def HANDS_COMPARE(human_hand, robot_hand, cards_open):
        # ► Compares the evaluated poker hands of the human and the robot to determine the winner.
        # ► Args:
        # ►     human_hand (list): A list of dictionaries representing the human player's cards.
        # ►     robot_hand (list): A list of dictionaries representing the robot player's cards.
        # ►     cards_open (list): A list of dictionaries representing the open community cards on the table.
        # ► Returns:
        # ►     list: A list containing two elements. The first element is a string indicating the winner
        # ►           ("human", "robot", or "tie"), and the second is the name of the winning hand type.
        human_evaluated = HAND_EVALUATE(human_hand, list(cards_open))
        robot_evaluated = HAND_EVALUATE(robot_hand, list(cards_open))
        print(f"[DEBUG] ► Human evaluation hand: " + str(human_evaluated) + " " + str(HAND_VALUES[human_evaluated[0]]))
        print(f"[DEBUG] ► Robot evaluation hand: " + str(robot_evaluated) + " " + str(HAND_VALUES[robot_evaluated[0]]))
        if human_evaluated > robot_evaluated:
            return ["human", HAND_VALUES[human_evaluated[0]]]
        elif human_evaluated < robot_evaluated:
            return ["robot", HAND_VALUES[robot_evaluated[0]]]
        else:
            return ["tie", HAND_VALUES[human_evaluated[0]]]
        # End if
    # End def
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  Computer (AI) Decision Logic
    # ╰─────────────────────────────────────────────────────────────────────────
    def DECIDE_ACTION_AI(ai_hand, community_cards, current_bet_to_match, ai_chips, opponent_chips, aggression_level_param, num_community_cards_revealed):
        # ► Determines the action an AI player should take based on its hand strength, game state, and aggression level.
        # ► Args:
        # ►     ai_hand (list): AI player's two-card hand.
        # ►     community_cards (list): Cards revealed on the table.
        # ►     current_bet_to_match (int): Total bet amount required to stay in the game.
        # ►     ai_chips (int): Number of chips the AI has.
        # ►     opponent_chips (int): Number of chips the opponent has.
        # ►     aggression_level_param (float): AI's aggression level (0.2 = passive, 1.0 = very aggressive).
        # ►     num_community_cards_revealed (int): Number of cards currently visible on the table.
        # ► Returns:
        # ►     tuple: The action ("fold", "call", "bet", "raise") and the bet amount (int).
        ai_hand_eval = HAND_EVALUATE(ai_hand, community_cards)                                                              # ═══► Evaluate the AI's hand strength and categorize it
        hand_rank_index = ai_hand_eval[0]                                                                                   # ═══► 0 for High Card, up to 8 for Straight Flush
        agg_factor = aggression_level_param / 5.0                                                                           # ═══► Normalize the aggression factor to a 0.2–1.0 range
        cost_to_call = current_bet_to_match                                                                                 # ═══► Define the cost to call the current bet.

        # ► Initialize hand strength tiers.
        is_strong_hand = False
        is_medium_hand = False
        is_decent_hand = False

        # ► Adjust hand strength based on the game stage (Pre-Flop vs Post-Flop).
        if num_community_cards_revealed == 0:                                                                               # ═══► Pre-Flop logic
            rank1 = RANK_TO_VALUE(ai_hand[0]['rank'])
            rank2 = RANK_TO_VALUE(ai_hand[1]['rank'])
            is_suited = ai_hand[0]['suit'] == ai_hand[1]['suit']                                                            # ═══► Check if both cards are of the same suit
            is_connected = abs(rank1 - rank2) == 1 and max(rank1, rank2) <= RANK_VALUES['Q']                                # ═══► Connected cards (not A-K, A-Q etc)
            # ► Evaluate specific pre-flop conditions (e.g., pairs, suited high cards).
            if rank1 == rank2:                                                                                              # ═══► Pair conditions
                if rank1 >= RANK_VALUES['T']: is_strong_hand = True                                                         # ═══► High pair (TT+)
                elif rank1 >= RANK_VALUES['7']: is_medium_hand = True                                                       # ═══► Mid pair (77–99)
                else: is_decent_hand = True                                                                                 # ═══► 22-66
                # End if
            elif max(rank1, rank2) >= RANK_VALUES['A'] and min(rank1, rank2) >= RANK_VALUES['T']:                           # ═══► AK, AQ, AJ
                if is_suited: is_strong_hand = True
                else: is_medium_hand = True
                # End if
            elif is_suited and max(rank1, rank2) >= RANK_VALUES['T']:                                                       # ═══► Suited high cards (KQ, KJ, QJ, etc.)
                is_medium_hand = True
            elif is_suited and is_connected and max(rank1, rank2) >= RANK_VALUES['7']:                                      # ═══► Suited connectors 78s+
                is_decent_hand = True
            elif (max(rank1, rank2) >= RANK_VALUES['Q'] and min(rank1, rank2) >= RANK_VALUES['9']):                         # ═══► Unsuited broadways QJ, KT etc
                is_decent_hand = True
            else:
                pass                                                                                                        # ═══► Weak
            # End if
        else:                                                                                                               # ═══► Post-flop: Categorize the strength of the made hand
            if hand_rank_index >= HAND_VALUES.index("Straight"):
                is_strong_hand = True
            elif hand_rank_index >= HAND_VALUES.index("Two Pair"):
                is_medium_hand = True
            elif hand_rank_index >= HAND_VALUES.index("One Pair"):
                pair_rank = ai_hand_eval[1]                                                                                 # ═══► Evaluate the strength of the pair.
                if pair_rank >= RANK_VALUES['J']:
                    is_medium_hand = True
                else: # Paire moyenne à basse
                    is_decent_hand = True
                # End if
            # End if
        # End if
        # ► Decide the AI's action based on its hand strength and aggression level.
        action = "fold"                                                                                                     # ═══► Default action is to fold
        bet_amount = 0                                                                                                      # ═══► Default bet amount
        if current_bet_to_match == 0:                                                                                       # ═══► If the AI is the first to act (no current bet to match).
            if is_strong_hand:
                action = "bet"
                bet_amount = BIG_BLIND * 2 if agg_factor >= 0.7 and ai_chips >= BIG_BLIND * 2 else BIG_BLIND
            elif is_medium_hand:
                action = "bet"
                bet_amount = BIG_BLIND if agg_factor >= 0.5 and ai_chips >= BIG_BLIND else 0
                if bet_amount == 0: action = "check"
                # End if
            elif is_decent_hand:
                if agg_factor > 0.7 and ai_chips >= BIG_BLIND:
                    action = "bet"
                    bet_amount = BIG_BLIND
                else:
                    action = "check"
                # End if
            else:                                                                                                           # ═══► Weak hand
                if agg_factor > 0.9 and ai_chips >= SMALL_BLIND:
                    action = "Bet"
                    bet_amount = SMALL_BLIND
                else:
                    action = "check"
                # End if
            # End if
        else:                                                                                                               # ═══► If the opponent has bet (current_bet_to_match > 0)
            # ► Checks if the AI can at least follow the bet amount_to_match is the total amount the player must have bet.
            # ► The difference between what the AI has already bet and current_bet_to_match is the "real" cost of calling.
            required_to_call = current_bet_to_match - robot.currentBet                                                      # ◀═══ IMPORTANT: Calculate the *actual* amount to be added
            if ai_chips < required_to_call:                                                                                 # ═══► If the AI does not have enough chips to cover the call
                if ai_chips > 0 and ai_chips >= (required_to_call * (0.5 - agg_factor * 0.1)):
                    action = "call"                                                                                         # ═══► All-in for call
                    bet_amount = ai_chips + robot.currentBet                                                                # ═══► Total bet will be all chips
                else:
                    action = "fold"
                    bet_amount = 0
                # End if
                return action, int(bet_amount)                                                                              # ═══►Premature end if fold or partial all-in
            # End if
            if is_strong_hand:
                if agg_factor > 0.4:
                    action = "raise"
                    # ► The raise must be at least the BIG_BLIND above the current bet
                    # ► Raise by BIG_BLIND * 2 ABOVE the current_bet_to_match
                    raise_increment = BIG_BLIND * 2 if agg_factor >= 0.7 and ai_chips >= current_bet_to_match + (BIG_BLIND * 2) else BIG_BLIND
                    bet_amount = current_bet_to_match + raise_increment
                else:
                    action = "call"
                    bet_amount = current_bet_to_match
                # End if
            elif is_medium_hand:
                if agg_factor > 0.6:
                    action = "raise"
                    raise_increment = BIG_BLIND if ai_chips >= current_bet_to_match + BIG_BLIND else 0
                    if raise_increment > 0:
                        bet_amount = current_bet_to_match + raise_increment
                    else:                                                                                                   # ═══► Cannot raise, must call or fold
                        action = "call"
                        bet_amount = current_bet_to_match
                    # End if
                else:
                    action = "call"
                    bet_amount = current_bet_to_match
                # End if
            elif is_decent_hand:
                if agg_factor > 0.4 and ai_chips >= required_to_call:
                    action = "call"
                    bet_amount = current_bet_to_match
                else:
                    action = "fold"
                    bet_amount = 0
                # End if
            else:                                                                                                           # ═══► Weak hand
                if agg_factor > 0.95 and ai_chips >= required_to_call and random.random() < 0.2:
                    action = "call"                                                                                         # ═══► Just call to bluff
                    bet_amount = current_bet_to_match
                else:
                    action = "fold"
                    bet_amount = 0
                # End if
            # End if
        # End if

        # ► Final adjustments for chip management and all-in scenarios.
        amount_to_add_to_pot = bet_amount - robot.currentBet
        if action != "fold" and amount_to_add_to_pot > ai_chips:
            bet_amount = ai_chips + robot.currentBet
            if bet_amount < current_bet_to_match and current_bet_to_match > 0:
                action = "fold"
                bet_amount = 0
            elif bet_amount == current_bet_to_match:
                action = "call"
            elif bet_amount > current_bet_to_match:
                action = "raise"
            # End if
        # End if

        return action, int(bet_amount)                                                                                      # ═══► Ensure bet_amount is an integer
    # End def

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Texas Hold'Em Game Flow
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
label LB_TEXAS_HOLDEM(sHuman="Human", sRobot="Robot", iAI=3, iChip=100):
    $ INITIALIZE_GAME(sHuman, sRobot, iChip)
    $ DEALER = DEALER_RANDOM() # Détermine le premier croupier
    $ print(f"[DEBUG] ► Label LB_TEXAS_HOLDEM({sHuman},{sRobot},{iAI},{iChip})")
    show screen SC_HAND_HUMAN()
    show screen SC_HAND_ROBOT()
    show screen SC_DEALER_CHIP(DEALER)
    $ POKER_AI_AGGRESSION = iAI
    call LB_START_NEW_HAND()
# End label
label LB_START_NEW_HAND():
    # Main game loop
    $ print(f"[DEBUG] ► Label LB_START_NEW_HAND()")
    while True:
        $ print(f"[DEBUG] ► While loop starting point")
        # ╭─────────────────────────────────────────────────────────────────────
        # │  Ensure that players still have chips
        # ╰─────────────────────────────────────────────────────────────────────
        if human.chips <= 0:
            "\n\nYou have no more chips. [sRobot] has won the game!"
            jump LB_END_GAME
        # End if
        if robot.chips <= 0:
            "\n\n[sRobot] has no more chips. You've won the game!"
            jump LB_END_GAME
        # End if
        $ DECK_RESET()
        $ POT_RESET(0)
        $ CARDS_OPEN_RESET()
        $ CARDS_PLAYERS_RESET()                                                                                             # ═══► Reset hands and folded status
        $ PLAYER_FOLD = False
        $ print(f"[DEBUG] ► Reset hands and folded status {PLAYER_FOLD}")

        $ highest_bet_this_round = BIG_BLIND                                                                                # ═══► At the start of the round, the big blind is the bet to call
        $ small_blind_player_obj = robot if DEALER == "human" else human
        $ big_blind_player_obj = human if DEALER == "human" else robot
        $ print(f"[DEBUG] ► Big bling = {BIG_BLIND} --► Small Blind is {small_blind_player_obj.name} and Big Blind is {big_blind_player_obj.name}")
        $ big_blind_player_who_posted = BLINDS(DEALER)                                                                      # ═══► Place the blinds and get the player who must speak first post-blinds (the one after the big blind)
        $ first_to_act_preflop = small_blind_player_obj if big_blind_player_obj == human else human
        $ print(f"[DEBUG] ► First post-blinds player = {first_to_act_preflop.name}")
        $ print(f"[DEBUG] ► The blinds have been bet. The pot is now " + str(pot) + " chips")
        show screen SC_HAND_HUMAN()
        show screen SC_HAND_ROBOT(reveal=False)                                                                             # ═══► Ensures that the AI's hand is hidden
        $ CARDS_DEAL()                                                                                                      # ═══► Deal the hidden cards
        $ print(f"[DEBUG] ► Your cards " + str(human.hand[0]['rank']) + str(human.hand[0]['suit']) + " and " + str(human.hand[1]['rank']) + str(human.hand[1]['suit']))
        show screen SC_HAND_HUMAN()
        show screen SC_HAND_ROBOT(reveal=False)                                                                             # ═══► Ensures that the AI's hand is hidden

        # ╔═════════════════════════════════════════════════════════════════════
        # ║ Tours de mise (Pre-Flop, Flop, Turn, River)
        # ╚═════════════════════════════════════════════════════════════════════
        # ► The BETTING_ROUND_LOGIC function manages the betting flow. It returns True if the round ends in a Fold.
        # ► It takes into account: the first player to act, the current bet and the name of the stage.

        # ╭─────────────────────────────────────────────────────────────────────
        # │  Pre-Flop
        # ╰─────────────────────────────────────────────────────────────────────
        $ print(f"[DEBUG] ► Pre-Flop start --► First to act: {first_to_act_preflop.name} ----► Big Blind: {BIG_BLIND}")
        $ print(f"[DEBUG] ► Human Chips {human.chips} --► Robot Chips: {robot.chips} ----► All-In : {if human.chips > 0 and robot.chips > 0}")
        if human.chips > 0 and robot.chips > 0:                                                                             # ═══► Not all-in
            $ round_ended_by_fold = BETTING_ROUND_LOGIC(first_to_act_preflop, BIG_BLIND, "Pre-Flop", 0)
            if round_ended_by_fold:
                $ PLAYER_FOLD = True
            # End if
        else
            show screen SC_HAND_ROBOT(reveal=True)                                                                          # ═══► All-in - Reveals the computer hand
        # End if
        $ print(f"[DEBUG] ► Pre-Flop end --► Round ended by fold: {round_ended_by_fold}")
        " PAUSE 1 "
        # ╭─────────────────────────────────────────────────────────────────────
        # │  Flop
        # ╰─────────────────────────────────────────────────────────────────────
        if PLAYER_FOLD == False:
            $ CARDS_OPEN_REVEAL(3)
            $ print(f"[DEBUG] ► Flop : " + str(cards_open[0]['rank']) + str(cards_open[0]['suit']) + ", " + str(cards_open[1]['rank']) + str(cards_open[1]['suit']) + ", " + str(cards_open[2]['rank']) + str(cards_open[2]['suit']))
            show screen SC_OPEN_CARDS()
            $ print(f"[DEBUG] ► Flop start --► First to act: {small_blind_player_obj.name}")
            $ print(f"[DEBUG] ► Human Chips {human.chips} --► Robot Chips: {robot.chips} ----► All-In : {if human.chips > 0 and robot.chips > 0}")
            if human.chips > 0 and robot.chips > 0:                                                                         # ═══► Not all-in
                $ first_to_act_postflop = small_blind_player_obj                                                            # ═══► Post-flop, the small blind goes first
                $ round_ended_by_fold = BETTING_ROUND_LOGIC(first_to_act_postflop, 0, "Flop", 3)
                if round_ended_by_fold:
                    $ PLAYER_FOLD = True
                # End if
            else
                show screen SC_HAND_ROBOT(reveal=True)                                                                      # ═══► All-in - Reveals the computer hand
            # End if
            $ print(f"[DEBUG] ► Pre-Flop end --► Round ended by fold: {round_ended_by_fold}")
        # End if
        " PAUSE 2 "
        # ╭─────────────────────────────────────────────────────────────────────
        # │  Turn
        # ╰─────────────────────────────────────────────────────────────────────
        if PLAYER_FOLD == False:
            $ CARDS_OPEN_REVEAL(1)
            $ print(f"[DEBUG] ► Turn : " + str(cards_open[3]['rank']][cards_open[3]['suit']))
            show screen SC_OPEN_CARDS()
            $ print(f"[DEBUG] ► Human Chips {human.chips} --► Robot Chips: {robot.chips} ----► All-In : {if human.chips > 0 and robot.chips > 0}")
            if human.chips > 0 and robot.chips > 0:                                                                         # ═══► Not all-in
                $ round_ended_by_fold = BETTING_ROUND_LOGIC(first_to_act_postflop, 0, "Turn", 4)
                if round_ended_by_fold:
                    $ PLAYER_FOLD = True
                # End if
            else
                show screen SC_HAND_ROBOT(reveal=True)                                                                      # ═══► All-in - Reveals the computer hand
            # End if
        # End if
        " PAUSE 3 "
        # ╭─────────────────────────────────────────────────────────────────────
        # │  River
        # ╰─────────────────────────────────────────────────────────────────────
        if PLAYER_FOLD == False:
            $ CARDS_OPEN_REVEAL(1)
            $ print(f"[DEBUG] ► River : " + str(cards_open[4]['rank']][cards_open[4]['suit']))
            show screen SC_OPEN_CARDS()
            $ print(f"[DEBUG] ► Human Chips {human.chips} --► Robot Chips: {robot.chips} ----► All-In : {if human.chips > 0 and robot.chips > 0}")
            if human.chips > 0 and robot.chips > 0:                                                                         # ═══► Not all-in
                $ round_ended_by_fold = BETTING_ROUND_LOGIC(first_to_act_postflop, 0, "River", 5)
                if round_ended_by_fold:
                    $ PLAYER_FOLD = True
                # End if
            else
                show screen SC_HAND_ROBOT(reveal=True)                                                                      # ═══► All-in - Reveals the computer hand
            # End if
        # End if
        " PAUSE 4 "
        # ╭─────────────────────────────────────────────────────────────────────
        # │  Showdown
        # ╰─────────────────────────────────────────────────────────────────────
        if PLAYER_FOLD == False:
            "\n\nAll bets are in. Showdown!"
            show screen SC_HAND_ROBOT(reveal=True)                                                                          # ═══► Révèle la main de l'ordinateur
            $ winner_info = HANDS_COMPARE(human.hand, robot.hand, cards_open)
            $ winner = winner_info[0]
            $ winning_hand_type = winner_info[1]

            if winner == "human":
                "Vous avez [winning_hand_type]. Vous gagnez le pot de [pot] jetons !"
                $ human.chips += pot
            elif winner == "robot":
                "[sRobot] a [winning_hand_type]. [sRobot] gagne le pot de [pot] jetons !"
                $ robot.chips += pot
            else: # tie
                "C'est une égalité ! Vous avez tous les deux [winning_hand_type]."
                $ human.chips += pot // 2
                $ robot.chips += pot // 2
            $ pot = 0 # Le pot est distribué

            "Vos jetons: [human.chips], Jetons de [sRobot]: [robot.chips]."

        $ DEALER = DEALER_SWITCH(DEALER) # Changer de croupier pour la prochaine main
        hide screen SC_DEALER_CHIP
        show screen SC_DEALER_CHIP(DEALER)

        # Option de rejouer
        # Remplacer le menu par des boutons
        $ choice = renpy.call_screen("SC_PLAY_AGAIN_CHOICES")
        if choice == "continue":
            jump LB_START_NEW_HAND
        elif choice == "quit":
            jump LB_END_GAME

label LB_END_GAME:
    "Merci d'avoir joué !"
    return

screen SC_PLAY_AGAIN_CHOICES():
    modal True
    zorder 100
    frame:
        xalign  0.872
        yalign  0.960
        xsize   0.088
        ysize   0.050
        textbutton ("NEW GAME") action Return("continue"):
            xanchor  0.5
            xpos   108
            ypos    -5
            text_style "STYLE_CHOICE_BUTTON_LIME"
        # End textbutton
    # End frame
    frame:
        xalign  0.978
        yalign  0.960
        xsize   0.088
        ysize   0.050
        textbutton ("QUIT") action Return("quit"):
            xanchor 0.5
            xpos  100
            ypos -5
            text_style "STYLE_CHOICE_BUTTON_RED"
        # End textbutton
    # End frame
# End screen
screen SC_DEALER_CHIP(current_dealer_param):
    frame:
        if current_dealer_param == "human":
            background "#40404000"
            xalign 1.0
            yalign 0.85
            xsize 0.08
            ysize 0.2
            vbox:
                add "Dealer.png" size (100, 100)
        elif current_dealer_param == "robot":
            background "#40404000"
            xalign 1.0
            yalign 0.15
            xsize 0.08
            ysize 0.2
            vbox:
                add "Dealer.png" size (100, 100)
            # End vbox
        # End if
    # End frame
# End screen
screen SC_HAND_HUMAN():
    frame:
        background "#40404060"
        xalign 1.0
        yalign 0.5
        xsize 0.22
        ysize 1.0
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.8
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}Your chips: [human.chips]{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for card in human.hand:
                        add CARDS_IMAGE(card) xsize 188 ysize 251
            # End Grid
        # End vbox
    # End frame
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: [pot]{/b}" size 26 color "#FFFFFF"
        # End hbox
    # End frame
# End screen
screen SC_HAND_ROBOT(reveal=False): # Ajout du paramètre reveal
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.1
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}[robot.name]: [robot.chips]{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for card in robot.hand:
                        if reveal:
                            add CARDS_IMAGE(card) size (188, 251)
                        elif POKER_CHEAT:
                            add CARDS_IMAGE(card) size (188, 251)
                            add "cards/back_of_card_1.png" size (188, 251) alpha 0.5 xpos -30
                        else:
                            add "cards/back_of_card_1.png" size (188, 251)
                    # End for
                # End hbox
            # End Grid
        # End vbox
    # End frame
# End screen
screen SC_HUMAN_CHOICES(street_name, current_pot, current_highest_bet_val, player_chips_val, player_current_bet_val, amount_to_match_val, big_blind_val):
    # Fond semi-transparent pour l'écran d'action
    modal True
    zorder 100

    frame:
        xalign  0.842
        yalign  0.960
        xsize   0.060
        ysize   0.050
        textbutton ("FOLD") action Return({"action": "fold"}):
            xanchor  0.5
            xpos    66
            ypos    -5
            text_style "STYLE_CHOICE_BUTTON_RED"
        # End textbutton
    # End frame
    frame:
        xalign  0.914
        yalign  0.960
        xsize   0.060
        ysize   0.050
        if amount_to_match_val == 0:
            textbutton ("CHECK") action Return({"action": "check"}):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_ORANGE"
            # End textbutton
        else:
            # Call amount is the difference between current_highest_bet and player_current_bet
            $ actual_call_cost = current_highest_bet_val - player_current_bet_val
            if player_chips_val >= actual_call_cost:
                textbutton ("CALL") action Return({"action": "call", "amount": current_highest_bet_val}):
                    xanchor 0.5
                    xpos 66
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            else: # All-in Call
                textbutton ("ALL-IN") action Return({"action": "call", "amount": player_chips_val + player_current_bet_val}):
                    xanchor 0.5
                    xpos 66
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            # End if
        # End if
    # End frame
    $ can_bet_2bb = player_chips_val >= (big_blind_val * 2) + amount_to_match_val
    frame:
        xalign 0.986
        yalign 0.96
        xsize 0.06
        ysize 0.05
        if amount_to_match_val == 0: # If no one has bet yet (player can Bet)
            textbutton ("BET") action Return({"action": "bet", "amount": big_blind_val * 2}):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_LIME"
        else: # If someone has already bet (player can Raise)
            textbutton ("RAISE") action Return({"action": "raise", "amount": current_highest_bet_val + (big_blind_val * 2)}):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_LIME"
        # End if
    # End frame
# End screen
screen SC_POKER_INFORMATION(sMessage1, sMessage2):
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.01
        xsize 0.21
        ysize 0.075
        vbox:
            grid 1 2:
                hbox:
                    text "{i}" + sMessage1 + "{/i}" size 24 color "#FFFFFF"
                hbox:
                    text "{i}" + sMessage2 + "{/i}" size 24 color "#FFFFFF"

# End screen
screen SC_OPEN_CARDS():
    frame:
        background "#40404000"
        xalign 0.997
        yalign 0.5
        xsize 0.21
        ysize 0.185
        hbox spacing -120:
            for card in cards_open:
                add CARDS_IMAGE(card) xsize 188 ysize 251
            # End Grid
        # End vbox
    # End frame
# End screen
