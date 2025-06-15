# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global variables
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
define DEALER       = ""
define POKER_CHEAT  = False
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
            self.name = name                                                                            # ═══► Player's name
            self.chips = chips                                                                          # ═══► Player's available chips
            self.hand = []                                                                              # ═══► Player's hand (two cards)
            self.currentBet = 0                                                                         # ═══► Player's current bet in the round
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
    def BETTING_ROUND():                                                                                                    # ═══► Function for a betting round
        global pot
        player.resetBet()                                                                               # ═══► Reset players' current bets
        computer.resetBet()
        # Example: Player decides to bet 10 chips
        player.current_bet = 10
        player.chips -= 10
        pot += 10

        # AI decides to call the bet
        computer.current_bet = 10
        computer.chips -= 10
        pot += 10
    # End def
    def BLINDS(dealer_position):
        global pot                                                                                      # ═══► Define a function to handle the blinds
        small_blind = 10
        #big_blind = 20
        if dealer_position == "player":
            player.chips -= small_blind
            #ai.chips -= big_blind
            pot += small_blind #+ big_blind
        else:
            computer.chips -= small_blind
            #player.chips -= big_blind
            pot += small_blind #+ big_blind
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
    def CARDS_OPEN_REVEAL(count):                                                                                           # ═══► Function to reveal open cards
        cards_open.extend(deck.draw(count))
    # End def
    def CARDS_PLAYERS_RESET():                                                                                              # ═══► Function to reset players cards
        player.hand  = []
        computer.hand = []
    # End def
    def DEALER_RANDOM():                                                                                                    # ═══► Function to switch the dealer position
        dealer_position = renpy.random.choice(["player", "computer"])                                   # ═══► Randomly choose who starts as the dealer
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
        unique_ranks_values = sorted(list(set(RANK_TO_VALUE(card['rank']) for card in combined)), reverse=True)            # ═══► Check for Straight
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
                all_ranks = [RANK_TO_VALUE(card['rank']) for card in combined]                                             # ═══► Look for the best pair among all the cards to form a full house
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
    def DECIDE_ACTION(hand, cards_open, pot, opponent_bet):
        strength_tuple = HAND_EVALUATE(hand, cards_open)                                                                    # ═══► Evaluating the hand returns a tuple, so all we need is the hand type
        strength = HAND_RANKING[strength_tuple[0]]                                                                          # ═══► Retrieves the name of the hand
        strong_hands = ["Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
        if strength in strong_hands:
            return "Raise"
        elif strength == "One Pair" or strength == "Two Pair":
            return "Call" if opponent_bet <= pot * 0.5 else "Fold"
        else:
            return "Fold"
        # End if
    # End def
# End python

# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Texas Hold'Em
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
label LB_TEXAS_HOLDEM(str_Player="Player", str_Computer="Computer"):
    $ INITIALIZE_GAME(str_Player, str_Computer)                                                                             # ═══► Initialize the game
    $ DEALER = DEALER_RANDOM()
    show screen SC_HAND_PLAYER()
    show screen SC_HAND_COMPUTER()

    # Main game loop
    while True:
        $ DECK_RESET()
        $ POT_RESET(0)
        $ CARDS_OPEN_RESET()
        $ CARDS_PLAYERS_RESET()
        # Display the current dealer
        if DEALER == "player":
            "You are the dealer."
        else:
            "[str_Computer] is the dealer."
        $ winner = ["",""]

        # Post blinds and update pot
        $ BLINDS(DEALER)
        "Blinds have been posted. The pot is now [pot] chips."

        # Deal hole cards
        $ CARDS_DEAL()
        "You have been dealt: [player.hand[0]['rank']] of [player.hand[0]['suit']] and [player.hand[1]['rank']] of [player.hand[1]['suit']]."
        show screen SC_HAND_PLAYER()
        show screen SC_HAND_COMPUTER()

        # First betting round
        $ BETTING_ROUND()
        "The pot is now [pot] chips."

        # Reveal the Flop
        $ CARDS_OPEN_REVEAL(3)
        "The Flop is: [cards_open[0]['rank']] of [cards_open[0]['suit']], [cards_open[1]['rank']] of [cards_open[1]['suit']], and [cards_open[2]['rank']] of [cards_open[2]['suit']]."
        show screen SC_OPEN_CARDS()

        # Second betting round
        $ BETTING_ROUND()
        "The pot is now [pot] chips."

        # Reveal the Turn
        $ CARDS_OPEN_REVEAL(1)
        "The Turn is: [cards_open[3]['rank']] of [cards_open[3]['suit']]."

        # Third betting round
        $ BETTING_ROUND()
        "The pot is now [pot] chips."

        # Reveal the River
        $ CARDS_OPEN_REVEAL(1)
        "The River is: [cards_open[4]['rank']] of [cards_open[4]['suit']]."

        # Final betting round
        $ BETTING_ROUND()
        "The pot is now [pot] chips."

        # Evaluating hands to determine the winner
#        $ player_best_hand = HAND_EVALUATE(player.hand, cards_open)
#        $ computer_best_hand = HAND_EVALUATE(computer.hand, cards_open)
        $ winner = HANDS_COMPARE(player.hand, computer.hand, cards_open)
        if winner[0] == "player":
            "You have [winner[1]]. You win this round!"
            $ player.chips += pot
        elif winner[0] == "computer":
            "[str_Computer] has [winner[1]]. [str_Computer] wins this round!"
            $ computer.chips += pot
        else:
            "It's a tie! You both have [winner[1]]."
            $ player.chips += pot // 2
            $ computer.chips += pot // 2
        # End if

        # Reset the pot for the next round
        $ pot = 0

        # Ask if the player wants to play another round
        menu:
            "Do you want to play another round?"
            "Yes":
                hide screen SC_DEALER_CHIP
                $ DEALER = DEALER_SWITCH(DEALER)
                show screen SC_DEALER_CHIP(DEALER)
            "No":
                return
    # End While
# End label

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
                        if winner[0] == "" and POKER_CHEAT == False:
                            add "cards/back_of_card_1.png" size (188, 251)
                        elif winner[0] != "":
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
