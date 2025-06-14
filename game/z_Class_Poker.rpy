# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Global variables
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
define DEALER   = ""
# ╔═════════════════════════════════════════════════════════════════════════════
# ║╔════════════════════════════════════════════════════════════════════════════
# ║║  Python code block for Texas Hold'Em Classes
# ║╚════════════════════════════════════════════════════════════════════════════
# ╚═════════════════════════════════════════════════════════════════════════════
init python:
    import random
    from collections import Counter  # ═══► Import Counter pour compter les occurrences
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
        player = CL_PLAYER(str_Player, int_Chips)                                                       # ═══► Create players with 100 chips each
        computer = CL_PLAYER(str_Computer, int_Chips)
        deck = CL_DECK()                                                                                # ═══► Initialize a shuffled deck
    # End def
    def DECK_RESET():                                                                                   # ═══► Function to switch the dealer position
        global deck
        deck = CL_DECK()                                                                                # ═══► Initialize a shuffled deck
    # End def
    def DEALER_RANDOM():                                                                                # ═══► Function to switch the dealer position
        dealer_position = renpy.random.choice(["player", "computer"])                                   # ═══► Randomly choose who starts as the dealer
        return dealer_position
    # End def
    def DEALER_SWITCH(dealer_position):                                                                 # ═══► Function to switch the dealer position
        renpy.say(None, dealer_position)
        if dealer_position   == "player":
            dealer_position   = "computer"
        elif dealer_position == "computer":
            dealer_position   = "player"
        # End if
        renpy.say(None, dealer_position)
        return dealer_position
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
    def CARDS_DEAL():                                                                                   # ═══► Function to distribute cards to players
        player.hand = deck.draw(2)                                                                      # ═══► Two cards for the player
        computer.hand = deck.draw(2)                                                                    # ═══► Two cards for the computer
    # End def
    def CARDS_IMAGE(card):
        return f"cards/{card['rank']}{card['suit']}.png"
    # End def
    def CARDS_PLAYERS_RESET():                                                                          # ═══► Function to reset players cards
        player.hand  = []
        computer.hand = []
        # End def
    def CARDS_OPEN_RESET():                                                                             # ═══► Function to reset open cards
        global cards_open
        cards_open = []
        # End def
    def CARDS_OPEN_REVEAL(count):                                                                       # ═══► Function to reveal open cards
        cards_open.extend(deck.draw(count))
    # End def
    def POT_RESET(int_Pot=0):                                                                           # ═══► Function to initialize the pot
        global pot
        pot = int_Pot
    def BETTING_ROUND():                                                                                # ═══► Function for a betting round
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
    def HAND_EVALUATE(hand, cards_open):
        combined = hand + list(cards_open)                                                              # ═══► Combine player's hand and open cards
        rank_counts = Counter(card['rank'] for card in combined)                                        # ═══► Cunt occurrences of ranks and suits
        suit_counts = Counter(card['suit'] for card in combined)
        def is_flush():                                                                                 # ═══► Helper function: Check for flush
            return any(count >= 5 for count in suit_counts.values())
        # End def
        def is_straight():
            rank_order = '23456789TJQKA'
            valid_ranks = [r for r in rank_counts.keys() if r in rank_order]  # Filtre les rangs valides
            rank_str = ''.join(sorted(valid_ranks, key=lambda r: rank_order.index(r)))
            # Chercher une séquence de 5 cartes consécutives
            for i in range(len(rank_order) - 4):
                if rank_order[i:i+5] in rank_str:
                    return True
                # End if
            # End for
            return 'A' in valid_ranks and all(r in valid_ranks for r in '2345')                         # ═══► Managing the Ace-down for a fifth (A-2-3-4-5)
        # End def
        if is_flush() and is_straight():                                                                # ═══► Evaluate hand strength
            return "Straight Flush"
        elif 4 in rank_counts.values():
            return "Four of a Kind"
        elif 3 in rank_counts.values() and 2 in rank_counts.values():
            return "Full House"
        elif is_flush():
            return "Flush"
        elif is_straight():
            return "Straight"
        elif 3 in rank_counts.values():
            return "Three of a Kind"
        elif list(rank_counts.values()).count(2) == 2:
            return "Two Pair"
        elif 2 in rank_counts.values():
            return "One Pair"
        else:
            return "High Card"
        # End if
    # End def
    def HANDS_COMPARE(player_hand, computer_hand, cards_open):
        hand_ranking = [
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
        player_best = HAND_EVALUATE(player_hand, list(cards_open))
        computer_best = HAND_EVALUATE(computer_hand, list(cards_open))
        if hand_ranking.index(player_best) > hand_ranking.index(computer_best):
            return "player"
        elif hand_ranking.index(player_best) < hand_ranking.index(computer_best):
            return "computer"
        else:
            return "tie"
        # End if
    # End def
    def DECIDE_ACTION(hand, cards_open, pot, opponent_bet):
        strength = HAND_EVALUATE(hand, cards_open)                                                      # ═══► Evaluate the strength of the AI's hand
        strong_hands = ["Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]          # ═══► Simplistic decision-making logic
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
    $ INITIALIZE_GAME(str_Player, str_Computer)                                                         # ═══► Initialize the game
    $ DEALER = DEALER_RANDOM()
    show screen SC_SHOW_HANDS()

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

        # Post blinds and update pot
        $ BLINDS(DEALER)
        "Blinds have been posted. The pot is now [pot] chips."

        # Deal hole cards
        $ CARDS_DEAL()
        "You have been dealt: [player.hand[0]['rank']] of [player.hand[0]['suit']] and [player.hand[1]['rank']] of [player.hand[1]['suit']]."
        show screen SC_SHOW_HANDS()

        # First betting round
        $ BETTING_ROUND()
        "The pot is now [pot] chips."

        # Reveal the Flop
        $ CARDS_OPEN_REVEAL(3)
        "The Flop is: [cards_open[0]['rank']] of [cards_open[0]['suit']], [cards_open[1]['rank']] of [cards_open[1]['suit']], and [cards_open[2]['rank']] of [cards_open[2]['suit']]."
        show screen SC_CARDS_OPEN()
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
        $ player_best_hand = HAND_EVALUATE(player.hand, cards_open)
        $ computer_best_hand = HAND_EVALUATE(computer.hand, cards_open)
        $ winner = HANDS_COMPARE(player.hand, computer.hand, cards_open)
        if winner == "player":
            "You win this round!"
            $ player.chips += pot
        elif winner == "computer":
            "[str_Computer] wins this round!"
            $ computer.chips += pot
        else:
            "It's a tie!"
            $ player.chips += pot // 2
            $ computer.chips += pot // 2
        # End if

        # Reset the pot for the next round
        $ pot = 0

        # Ask if the player wants to play another round
        menu:
            "Do you want to play another round?"
            "Yes":
                $ DEALER = DEALER_SWITCH(DEALER)
            "No":
                return
    # End While
# End label


screen SC_SHOW_HANDS():
    # Background frame for the screen
    frame:
        background "#404040"
        xalign 1.0
        yalign 0.5
        xsize 0.22
        ysize 1.0
    # Player hand display
    frame:
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
                hbox:
                    if DEALER == "player":
                        add "Dealer.png" size (100, 100)
                    # End if
    # Opponent hand display
    frame:
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
                        add "cards/back_of_card_1.png" size (188, 251)
                    # End for
                hbox:
                    if DEALER == "computer":
                        add "Dealer.png" size (100, 100)
                    # End if
    # Pot
    frame:
        background "#404040"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: [pot]{/b}" size 26 color "#FFFFFF"

screen SC_CARDS_OPEN():
    # Community cards
    frame:
        background "#404040"
        xalign 0.997
        yalign 0.5
        xsize 0.21
        ysize 0.185
        hbox spacing -120:
            for card in cards_open:
                add CARDS_IMAGE(card) xsize 188 ysize 251
