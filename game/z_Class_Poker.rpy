# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global variables
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
define DEALER                   = ""
define POKER_CHEAT              = False
define PLAY                     = True
define WINNER_MESSAGE           = ""
define WINNER                   = ["", ""]
define SMALL_BLIND              = 5
define BIG_BLIND                = 10
define POKER_AI_AGGRESSION      = 3 # De 1 (passif) à 5 (très agressif)
define PREFLOP                  = True
define FLOP                     = True
define TURN                     = True
define RIVER                    = True

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
# ║║  Python code block for Texas Hold'Em Classes
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
init python:
    import random
    from collections import Counter                                                                                         # ═══► Import Counter pour compter les occurrences

    # ═══► Dictionary for converting card ranks into numerical values
    # ═══► Useful for comparing card and hand heights
    RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    # ═══► List of hand rankings, from weakest to strongest
    HAND_RANKING = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush"
    ]

    class CL_PLAYER:
        # ► This class represents a player in the game.
        def __init__(self, name, chips):
            self.name       = name                                                                                          # ═══► Player's name
            self.chips      = chips                                                                                         # ═══► Player's available chips
            self.hand       = []                                                                                            # ═══► Player's hand (two cards)
            self.currentBet = 0                                                                                             # ═══► Player's current bet in the round
            self.isFolded   = False                                                                                         # ═══► Find out if the player fold
        # End def
        def fold(self):
            self.isFolded   = True
        # End def
        def resetForNewHand(self):
            self.hand       = []
            self.currentBet = 0
            self.isFolded   = False
        # End def
        def resetBet(self):
            self.currentBet = 0
        # End def
    # End class
    class CL_DECK:
        # ► This class represents the deck of cards.
        def __init__(self):
            suits = ['C', 'D', 'H', 'S']
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
            self.cards = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
            random.shuffle(self.cards)                                                                  # ═══► Shuffle the deck
            # Validation des cartes
            rank_order = '23456789TJQKA'
            for card in self.cards:
                if card['rank'] not in rank_order:
                    raise ValueError(f"Invalid rank found in deck: {card['rank']}")
                # End if
            # End for
        # End def
        def draw(self, count):
            drawn_cards = self.cards[:count]                                                            # ═══► Draw 'count' number of cards from the deck
            self.cards = self.cards[count:]
            return drawn_cards
        # End def
    # End class
    def INITIALIZE_GAME(str_Player="Player", str_Computer="Computer", int_Chips=100):
        global player, computer
        player = CL_PLAYER(str_Player, int_Chips)                                                                           # ═══► Create players with 100 chips each
        computer = CL_PLAYER(str_Computer, int_Chips)
        deck = CL_DECK()                                                                                                    # ═══► Initialize a shuffled deck
    # End def
    def BETTING_ROUND(dealer, bet):                                                                                           # ═══► Function for a betting round
        global pot
        if turn == "player":
            player.resetBet()
            player.current_bet = bet
            player.chips -= 10
            pot += 10
        else:
            computer.resetBet()
            computer.current_bet = 10
            computer.chips -= 10
            pot += 10
        # End if
    # End def
    def BLINDS(dealer_position):
        global pot                                                                                                          # ═══► Define a function to handle the blinds
        small_blind = 5
        big_blind = 10
        if dealer_position == "player":
            player.chips    -= small_blind
            computer.chips  -= big_blind
            pot += small_blind + big_blind
        else:
            computer.chips  -= small_blind
            player.chips    -= big_blind
            pot += small_blind + big_blind
        # End if
    # End def
    def CARDS_DEAL():                                                                                                       # ═══► Function to distribute cards to players
        player.hand = deck.draw(2)                                                                      # ═══► Two cards for the player
        computer.hand = deck.draw(2)                                                                    # ═══► Two cards for the computer
    # End def
    def CARDS_IMAGE(card):
        return f"cards/{card['rank']}{card['suit']}.png"
    # End def
    def CARDS_OPEN_RESET():                                                                                                 # ═══► Function to reset open cards
        global cards_open
        cards_open = []
    # End def
    def CARDS_OPEN_REVEAL(state):                                                                                           # ═══► Function to reveal open cards
        count = 0
        if state == "FLOP":
            count = 3
        elif state == "TURN" or state == "RIVER":
            count = 1
        # End if
        cards_open.extend(deck.draw(count))
    # End def
    def CARDS_PLAYERS_RESET():                                                                                              # ═══► Function to reset players cards
        player.hand  = []
        computer.hand = []
    # End def
    def DEALER_RANDOM():                                                                                                    # ═══► Function to switch the dealer position
        dealer_position = renpy.random.choice(["player", "computer"])                                                       # ═══► Randomly choose who starts as the dealer
        return dealer_position
    # End def
    def DEALER_SWITCH(dealer_position):                                                                                     # ═══► Function to switch the dealer position
        print("Dealer before switch [dealer_position]")
        if dealer_position   == "player":
            dealer_position   = "computer"
        elif dealer_position == "computer":
            dealer_position   = "player"
        # End if
        print("Dealer after switch [dealer_position]")
        return dealer_position
    # End def
    def DECK_RESET():                                                                                                       # ═══► Function to switch the dealer position
        global deck
        deck = CL_DECK()                                                                                                    # ═══► Initialize a shuffled deck
    # End def
    def HANDS_COMPARE(player_hand, computer_hand, cards_open):
        player_evaluated = HAND_EVALUATE(player_hand, list(cards_open))
        computer_evaluated = HAND_EVALUATE(computer_hand, list(cards_open))
        print("Player hand assessment [player_evaluated]")
        print("Computer hand assessment [computer_evaluated]")
        # ═══► Compare hands using evaluation tuples
        # ═══► Tuples are compared element by element
        if player_evaluated > computer_evaluated:
            return ["player", HAND_RANKING[player_evaluated[0]]]
        elif player_evaluated < computer_evaluated:
            return ["computer", HAND_RANKING[computer_evaluated[0]]]
        else:
            return ["tie", HAND_RANKING[player_evaluated[0]]]
        # End if
    # End def
    def POT_RESET(int_Pot=0):                                                                                               # ═══► Function to initialize the pot
        global pot
        pot = int_Pot
    # End def
    def RANK_TO_VALUE(rank):                                                                                                # ═══► Converts a card rank into its numerical value
        print("Rank: [rank]")
        return RANK_VALUES.get(rank, 0)
    # End def
    def HAND_EVALUATE(hand, cards_open):
        combined = hand + list(cards_open)
        rank_counts = Counter(card['rank'] for card in combined)
        suit_counts = Counter(card['suit'] for card in combined)
        def find_ranks_by_count(count):                                                                                     # ═══► Helper to find ranks by number of occurrences
            return sorted([RANK_TO_VALUE(r) for r, c in rank_counts.items() if c == count], reverse=True)
        # End def
        def get_kickers(exclude_ranks):                                                                                     # ═══► Helper to obtain kickers (cards not used in the formation of the hand)
            all_ranks_values = sorted([RANK_TO_VALUE(card['rank']) for card in combined], reverse=True)
            kickers = [r for r in all_ranks_values if r not in exclude_ranks]
            return kickers[:5 - len(exclude_ranks)]                                                                         # ═══► Takes the kickers needed for a 5-card hand
        # End def
        flush_suit = None                                                                                                   # ═══► Check for Flush
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
            # End if
        # End for
        is_flush = (flush_suit is not None)
        unique_ranks_values = sorted(list(set(RANK_TO_VALUE(card['rank']) for card in combined)), reverse=True)             # ═══► Check for Straight
        if 14 in unique_ranks_values:                                                                                       # ═══► Add Ace as 1 for the bass fifth (A-2-3-4-5)
            unique_ranks_values.append(1)
        # End if
        unique_ranks_values.sort(reverse=True)
        straight_high_card = 0
        for i in range(len(unique_ranks_values) - 4):
            if unique_ranks_values[i] - unique_ranks_values[i+4] == 4:
                straight_high_card = unique_ranks_values[i]
                break
            # End if
        # End for
        is_straight = (straight_high_card > 0)
        four_of_a_kind_ranks = find_ranks_by_count(4)                                                                       # ═══► Evaluate hand strength and return with tie-breakers
        three_of_a_kind_ranks = find_ranks_by_count(3)                                                                      # ═══► Evaluate hand strength and return with tie-breakers
        pairs_ranks = find_ranks_by_count(2)                                                                                # ═══► Evaluate hand strength and return with tie-breakers
        if is_straight and is_flush:                                                                                        # ═══► For a straight flush, the highest card in the straight is the tiebreaker
            flush_straight_cards = sorted([RANK_TO_VALUE(card['rank']) for card in combined if card['suit'] == flush_suit], reverse=True)
            best_straight_flush_high_card = 0
            for i in range(len(flush_straight_cards) - 4):
                if flush_straight_cards[i] - flush_straight_cards[i+4] == 4:
                    best_straight_flush_high_card = flush_straight_cards[i]
                    break
                # End if
            # End for
            if best_straight_flush_high_card == 0 and 14 in flush_straight_cards and \
                all(r in flush_straight_cards for r in [2,3,4,5]):
                best_straight_flush_high_card = 5                                                                           # ═══► A-2-3-4-5 straight flush
            # End if
            return (HAND_RANKING.index("Straight Flush"), best_straight_flush_high_card)
        elif four_of_a_kind_ranks:
            quad_rank = four_of_a_kind_ranks[0]
            kicker = get_kickers([quad_rank])
            return (HAND_RANKING.index("Four of a Kind"), quad_rank, *kicker)
        elif three_of_a_kind_ranks and pairs_ranks:                                                                         # ═══► Full House (3 of the same rank + 2 of the same rank)
            full_house_3_rank = three_of_a_kind_ranks[0]                                                                    # ═══► The highest pair counts first, then the highest pair among the remaining pairs.
            remaining_pairs = [r for r in pairs_ranks if r != full_house_3_rank]
            if len(three_of_a_kind_ranks) > 1: # Si plusieurs brelans, le plus grand brelan
                full_house_3_rank = max(three_of_a_kind_ranks)
                remaining_pairs.append(min([r for r in three_of_a_kind_ranks if r != full_house_3_rank]))
            # End if
            if not remaining_pairs:                                                                                         # ═══► Case where there is no pair after the three of a kind (unlikely but for robustness)
                all_ranks = [RANK_TO_VALUE(card['rank']) for card in combined]                                              # ═══► Look for the best pair among all the cards to form a full house
                temp_counts = Counter(all_ranks)
                potential_pairs = sorted([r for r, c in temp_counts.items() if c >= 2 and r != full_house_3_rank], reverse=True)
                if potential_pairs:
                    full_house_2_rank = potential_pairs[0]
                else:
                    full_house_2_rank = 0                                                                                   # ═══► No valid pair
                # End if
            else:
                full_house_2_rank = max(remaining_pairs)
            # End if
            return (HAND_RANKING.index("Full House"), full_house_3_rank, full_house_2_rank)
        elif is_flush:                                                                                                      # ═══► For a suit, the 5 highest cards in the suit
            flush_cards_values = sorted([RANK_TO_VALUE(card['rank']) for card in combined if card['suit'] == flush_suit], reverse=True)
            return (HAND_RANKING.index("Flush"), *flush_cards_values[:5])
        elif is_straight:
            return (HAND_RANKING.index("Straight"), straight_high_card)
        elif three_of_a_kind_ranks:
            triple_rank = three_of_a_kind_ranks[0]
            kickers = get_kickers([triple_rank])
            return (HAND_RANKING.index("Three of a Kind"), triple_rank, *kickers)
        elif len(pairs_ranks) >= 2:                                                                                         # ═══► Two Pair: Sorted by highest pair, then second highest pair, then kicker
            pairs_ranks.sort(reverse=True)
            pair1_rank = pairs_ranks[0]
            pair2_rank = pairs_ranks[1]
            kickers = get_kickers([pair1_rank, pair2_rank])
            return (HAND_RANKING.index("Two Pair"), pair1_rank, pair2_rank, *kickers)
        elif len(pairs_ranks) == 1:                                                                                         # ═══► One Pair: Rank of the pair, then the three highest kickers
            pair_rank = pairs_ranks[0]
            kickers = get_kickers([pair_rank])
            return (HAND_RANKING.index("One Pair"), pair_rank, *kickers)
        else:                                                                                                               # ═══► High Card: The 5 highest cards
            high_cards = sorted([RANK_TO_VALUE(card['rank']) for card in combined], reverse=True)[:5]
            return (HAND_RANKING.index("High Card"), *high_cards)
        #End if
    # End def
    # ╭─────────────────────────────────────────────────────────────────────────
    # │  AI Decision Logic
    # ╰─────────────────────────────────────────────────────────────────────────
    def DECIDE_ACTION_AI(ai_hand, community_cards, current_bet_to_match, ai_chips, opponent_chips, aggression_level_param, num_community_cards_revealed):
        # ► Determines the action (Fold, Call, Raise, Check) of the AI according to its hand, community cards, current bet, chips and level of aggressiveness.
        # ►   Returns (action, bet_amount)
        # ►     action     ═══► "Fold", "Call", "Raise", "Check", "Bet"
        # ►     bet_amount ═══►The total amount to bet/raise (not just the difference).
        ai_hand_eval     = HAND_EVALUATE(ai_hand, community_cards)                                                           # ═══► Evaluate the current strength of the AI's hand
        hand_rank_index  = ai_hand_eval[0]                                                                                   # ═══► 0 for High Card, up to 8 for Straight Flush
        agg_factor       = aggression_level_param / 5.0                                                                      # ═══► Standardised aggressiveness factor (0.2 for passive, 1.0 for very aggressive)
        cost_to_call     = current_bet_to_match                                                                              # ═══► Cost of tracking current stake, if applicable
        # ► Determine the “tier” of hand strength for AI
        is_strong_hand   = False
        is_medium_hand   = False
        is_decent_hand   = False
        # ► Hand strength adjustments based on stage of play (pre-flop, flop, turn, river)
        # ► The strength of a hand is more "potential" pre-flop.
        if num_community_cards_revealed == 0: # Pré-Flop
            rank1        = _rank_to_value(ai_hand[0]['rank'])
            rank2        = _rank_to_value(ai_hand[1]['rank'])
            is_suited    = ai_hand[0]['suit'] == ai_hand[1]['suit']
            is_connected = abs(rank1 - rank2) == 1 and max(rank1, rank2) <= RANK_VALUES['Q']                                # ═══► Connected cards (not A-K, A-Q etc)
            if rank1 == rank2:                                                                                              # ═══► Pair served
                if rank1 >= RANK_VALUES['T']: is_strong_hand = True                                                         # ═══► TT+
                elif rank1 >= RANK_VALUES['7']: is_medium_hand = True                                                       # ═══► 77-99
                else: is_decent_hand = True                                                                                 # ═══► 22-66
            elif max(rank1, rank2) >= RANK_VALUES['A'] and min(rank1, rank2) >= RANK_VALUES['T']:                           # ═══► AK, AQ, AJ
                if is_suited: is_strong_hand = True
                else: is_medium_hand = True
            elif is_suited and max(rank1, rank2) >= RANK_VALUES['T']:                                                       # ═══► Suited high cards (KQ, KJ, QJ, etc.)
                is_medium_hand = True
            elif is_suited and is_connected and max(rank1, rank2) >= RANK_VALUES['7']:                                      # ═══► Suited connectors 78s+
                is_decent_hand = True
            elif (max(rank1, rank2) >= RANK_VALUES['Q'] and min(rank1, rank2) >= RANK_VALUES['9']):                         # ═══► Unsuited broadways QJ, KT etc
                is_decent_hand = True
            else:
                pass                                                                                                        # ═══► Remains weak
            #End if
        else:                                                                                                               # ═══► Post-flop: evaluate the hand and the draw potential
            if hand_rank_index >= HAND_RANKING.index("Straight"):
                is_strong_hand = True
            elif hand_rank_index >= HAND_RANKING.index("Two Pair"):
                is_medium_hand = True
            elif hand_rank_index >= HAND_RANKING.index("One Pair"):
                pair_rank = ai_hand_eval[1]                                                                                 # ═══► For a pair, consider the strength of the pair and the kickers
                if pair_rank >= RANK_VALUES['J']:                                                                           # ═══► High Pair (JJ+)
                    is_medium_hand = True
                else:                                                                                                       # ═══► Weak Pair
                    is_decent_hand = True
                # End if
            # End if
        # End if
        # ► Drawings (Flush draw, Straight draw)
        # ► This is a simplification. A more complex AI would calculate the outs.
        # ► For the moment, it's based on the curetn hand calculation
        action = "Fold"                                                                                                     # ═══► Action decision
        bet_amount = 0                                                                                                      # ═══► Total amount the AI will bet in the pot for its next action
        if current_bet_to_match == 0:                                                                                       # ═══► If the AI is the first to speak (current_bet_to_match is 0)
            if is_strong_hand:
                action = "Bet"
                bet_amount = BIG_BLIND * 2 if agg_factor >= 0.7 and ai_chips >= BIG_BLIND * 2 else BIG_BLIND
            elif is_medium_hand:
                action = "Bet"
                bet_amount = BIG_BLIND if agg_factor >= 0.5 and ai_chips >= BIG_BLIND else 0                                # ═══► If not aggressive enough or no chips, check
                if bet_amount == 0:
                    action = "Check"
                # End if
            elif is_decent_hand:
                if agg_factor > 0.7 and ai_chips >= BIG_BLIND:                                                              # ═══► Aggressive enough to make a small bet/bluff
                    action = "Bet"
                    bet_amount = BIG_BLIND
                else:
                    action = "Check"                                                                                        # ═══► Passive, check
                # End if
            else:                                                                                                           # ═══► Weak hand
                if agg_factor > 0.9 and ai_chips >= SMALL_BLIND:                                                            # ═══► Bluff very aggressive
                    action = "Bet"
                    bet_amount = SMALL_BLIND                                                                                # ═══► Very small bluff, to probe
                else:
                    action = "Check"
                # End if
            # End if
        else:
            # ► Ratio of call cost to AI tokens
            # ► Checks whether the AI can at least track the bet
            if ai_chips < cost_to_call:                                                                                     # ═══► Not enough chips to call, must have to fold or go all-in
                if ai_chips > 0 and ai_chips >= (cost_to_call * (0.5 - agg_factor * 0.1)):
                    action = "Call"                                                                                         # ═══► All-in for Call
                    bet_amount = ai_chips
                else:
                    action = "Fold"
                    bet_amount = 0
                # End if
                return action, int(bet_amount)                                                                              # ═══► Early exit if fold or partial all-in
            # End if
            if is_strong_hand:                                                                                              # ═══► If AI can keep up with the
                if agg_factor > 0.4:                                                                                        # ═══► Agressive
                    action = "Raise"
                    raise_increment = BIG_BLIND * 2 if agg_factor >= 0.7 and ai_chips >= current_bet_to_match + (BIG_BLIND * 2) else BIG_BLIND
                    bet_amount = current_bet_to_match + raise_increment
                else:                                                                                                       # ═══► Less aggressive, just Call
                    action = "Call"
                    bet_amount = current_bet_to_match
                # End if
            elif is_medium_hand:
                if agg_factor > 0.6:                                                                                        # ═══► Aggressive mid-range AI could Raise
                    action = "Raise"
                    raise_increment = BIG_BLIND if ai_chips >= current_bet_to_match + BIG_BLIND else 0
                    if raise_increment > 0:
                        bet_amount = current_bet_to_match + raise_increment
                    else:                                                                                                   # ═══► Cannot raise, must Call or Fold
                        action = "Call"
                        bet_amount = current_bet_to_match
                    # End if
                else:
                    action = "Call"
                    bet_amount = current_bet_to_match
                # End if
            elif is_decent_hand:
                if agg_factor > 0.4 and ai_chips >= current_bet_to_match:                                                   # ═══► IA not agressive
                    action = "Call"
                    bet_amount = current_bet_to_match
                else:
                    action = "Fold"
                    bet_amount = 0
                # End if
            else:                                                                                                           # ═══► Weak hand
                if agg_factor > 0.95 and ai_chips >= current_bet_to_match and random.random() < 0.2:                        # ═══► Occasional very aggressive Bluff
                    action = "Call"                                                                                         # ═══► Just Call to Bluff
                    bet_amount = current_bet_to_match
                else:
                    action = "Fold"
                    bet_amount = 0
                # End if
            # End if
        # End if
        # ► Final adjustments for chips (All-in if the desired stake exceeds the chips)
        if action != "Fold" and bet_amount > ai_chips:
            bet_amount = ai_chips
            if bet_amount < current_bet_to_match and current_bet_to_match > 0:                                              # ═══► If all-in amount is less than current bet, it's a fold
                action = "Fold"
                bet_amount = 0
            # End if
        # End if
        return action, int(bet_amount)                                                                                      # ═══► Ensure bet_amount is an integer
    # End def
# End python

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Texas Hold'Em
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
label LB_TEXAS_HOLDEM(str_Player="Player", str_Computer="Computer", int_Bet=10):
    $ INITIALIZE_GAME(str_Player, str_Computer)                                                                             # ═══► Initialize the game
    $ DEALER = DEALER_RANDOM()
    show screen SC_HAND_PLAYER()
    show screen SC_HAND_COMPUTER()

    # Main game loop
    while True:
        $ PREFLOP = True
        $ FLOP    = True
        $ TURN    = True
        $ RIVER   = True
        $ DECK_RESET()
        $ POT_RESET(0)
        $ CARDS_OPEN_RESET()
        $ CARDS_PLAYERS_RESET()
        $ DEALER = DEALER_SWITCH(DEALER)
        show screen SC_DEALER_CHIP(DEALER)
        $ BLINDS(DEALER)                                                                                                    # ═══► Post blinds and update pot
        $ CARDS_DEAL()                                                                                                      # ═══► Deal players cards
#        "You have been dealt: [player.hand[0]['rank']] of [player.hand[0]['suit']] and [player.hand[1]['rank']] of [player.hand[1]['suit']]."
        show screen SC_HAND_COMPUTER()
        show screen SC_HAND_PLAYER()
        if DEALER == "player":
            while PREFLOP == True:
                call screen SC_ACTION_PLAYER("PREFLOP", "")
                $ value = _return
                if value == "Call":
                    $ BETTING_ROUND("player", int_Bet)
                    $ PREFLOP = False
                elif value == "Raise":
                    $ BETTING_ROUND("player", int_Bet)
                    $ BETTING_ROUND("player", int_Bet)
                    $ PREFLOP = True
                elif value == "Fold":
                    $ game_status = _result
                    $ PREFLOP = False
                # End if
            # End while
        # End if
        $ CARDS_OPEN_REVEAL("FLOP")
        show screen SC_OPEN_CARDS()
        if DEALER == "player":
            while FLOP == True:
                call screen SC_ACTION_PLAYER("FLOP", "")
                $ value = _return
                if value == "Call":
                    $ BETTING_ROUND("player", int_Bet)
                    $ FLOP = False
                elif value == "Raise":
                    $ BETTING_ROUND("player", int_Bet)
                    $ BETTING_ROUND("player", int_Bet)
                    $ FLOP = True
                elif value == "Fold":
                    $ game_status = _result
                    $ FLOP = False
                # End if
            # End while
        # End if
        $ CARDS_OPEN_REVEAL("TURN")

        # Third betting round
#        $ BETTING_ROUND()
#        "The pot is now [pot] chips."

        # Reveal the River
        $ CARDS_OPEN_REVEAL("RIVER")
        "The River is: [cards_open[4]['rank']] of [cards_open[4]['suit']]."

        # Final betting round

#        $ BETTING_ROUND()
#        "The pot is now [pot] chips."

        $ WINNER = HANDS_COMPARE(player.hand, computer.hand, cards_open)                                                    # ═══► Evaluating hands to determine the winner
        if WINNER[0] == "player":
            $ WINNER_MESSAGE = "You win: " + str(WINNER[1])
            $ player.chips += pot
        elif WINNER[0] == "computer":
            $ WINNER_MESSAGE = str(str_Computer) + " wins: " + str(WINNER[1])
            $ computer.chips += pot
        else:
            "It's a tie (WINNER[1]])"
            $ player.chips += pot // 2
            $ computer.chips += pot // 2
        # End if
        $ pot = 0                                                                                                           # ═══► Reset the pot for the next round
        $ WINNER = ["",""]
        call screen SC_ACTION_PLAYER("CONTINUE", WINNER_MESSAGE)                                                            # ═══► Ask if the player wants to play another round
        if _return == False:
            return
        # End if
    # End While
# End label

screen SC_ACTION_PLAYER(action_player, message):
    if action_player == "PREFLOP" or action_player == "FLOP":
        frame:
            xalign 0.842
            yalign 0.96
            xsize 0.06
            ysize 0.05
            textbutton ("CALL") action Return (value="Call"):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_ORANGE"
        frame:
            xalign 0.914
            yalign 0.96
            xsize 0.06
            ysize 0.05
            textbutton ("RAISE") action Return (value="Raise"):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_ORANGE"
        frame:
            xalign 0.986
            yalign 0.96
            xsize 0.06
            ysize 0.05
            textbutton ("FOLD") action Return (value="Fold"):
                xanchor 0.5
                xpos 66
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_ORANGE"
    if action_player == "CONTINUE":
        frame:
            background "#404040"
            xalign 1.0
            yalign 1.0
            xsize 0.21
            ysize 0.13
            text "{b}[message]{/b}" size 26 color "#FFFFFF"
        frame:
            xalign 0.875
            yalign 0.96
            xsize 0.09
            ysize 0.05
            textbutton ("NEW GAME") action Return (value=True):
                xanchor 0.5
                xpos 108
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_LIME"
        frame:
            xalign 0.98
            yalign 0.96
            xsize 0.09
            ysize 0.05
            textbutton ("QUIT") action Return (value=False):
                xanchor 0.5
                xpos 108
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_RED"
# End screen
screen SC_HAND_PLAYER():
    frame:                                                                                                                  # ═══► Background frame for the screen
        background "#404040"
        xalign 1.0
        yalign 0.5
        xsize 0.22
        ysize 1.0
    # End frame
    frame:                                                                                                                  # ═══► Player hand display
        background "#404040"
        xalign 1.0
        yalign 0.8
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}Your Chips: [player.chips]{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for card in player.hand:
                        add CARDS_IMAGE(card) xsize 188 ysize 251
                    # End for
                # End hbox
            # End Grid
        # End vbox
    # End frame
    frame:                                                                                                                  # ═══► Pot display
        background "#404040"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: [pot]{/b}" size 26 color "#FFFFFF"
        # End hbox
    # End frame
# End screen
screen SC_HAND_COMPUTER():
    frame:                                                                                                                  # ═══► Computer hand display
        background "#404040"
        xalign 1.0
        yalign 0.1
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}[computer.name]: [computer.chips]{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for card in computer.hand:
                        if WINNER[0] == "" and POKER_CHEAT == False:
                            add "cards/back_of_card_1.png" size (188, 251)
                        elif WINNER[0] != "":
                            add CARDS_IMAGE(card) xsize 188 ysize 251
                        elif POKER_CHEAT == True:
                            add CARDS_IMAGE(card) size (188, 251)
                            add "cards/back_of_card_1.png" size (188, 251) alpha 0.5 xpos -30
                        # End if
                    # End for
                # End hbox
            # End Grid
        # End vbox
    # End frame
    frame:                                                                                                                  # ═══► Pot display
        background "#404040"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: [pot]{/b}" size 26 color "#FFFFFF"
        # End hbox
    # End frame
# End screen
screen SC_OPEN_CARDS():
    frame:                                                                                              # ═══► Community cards display
        background "#404040"
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
screen SC_DEALER_CHIP(DEALER):
    frame:                                                                                                                  # ═══► Player hand display
        if DEALER == "player":
            background "#404040"
            xalign 1.0
            yalign 0.85
            xsize 0.08
            ysize 0.2
            vbox:
                add "Dealer.png" size (100, 100)
            # End vbox
        # End if
        elif DEALER == "computer":
            background "#404040"
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
