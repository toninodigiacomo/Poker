## Import required libraries
init python:
    import random
    import renpy.store as store
    import renpy.exports as renpy

    ## Define the Player class
    class Player:
        def __init__(self, name, is_human=True):
            self.name = name
            self.is_human = is_human
            self.chips = 100
            self.is_dealer = False
            self.hand = []  # Personal cards
            self.has_requested_extension = 0

        def bet(self, amount):
            if amount > self.chips:
                raise ValueError(f"{self.name} does not have enough chips!")
            self.chips -= amount
            return amount

        def add_chips(self, amount):
            self.chips += amount

        def reset_hand(self):
            self.hand = []

    ## Define the GameState class
    class GameState:
        def __init__(self):
            self.deck = []
            self.pot = 0
            self.community_cards = []  # Flop, Turn, River
            self.players = []  # List of Player instances
            self.dealer_index = 0

        def create_deck(self):
            suits = ['C', 'D', 'H', 'S']
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            self.deck = [{'suit': suit, 'rank': rank, 'image': f"cards/{rank}{suit}.png"} for suit in suits for rank in ranks]
            random.shuffle(self.deck)

        def deal_card(self):
            if len(self.deck) == 0:
                raise ValueError("The deck is empty!")
            return self.deck.pop()

        def deal_hands(self):
            for player in self.players:
                player.hand = [self.deal_card(), self.deal_card()]

        def deal_community_cards(self, count):
            if len(self.deck) < count:
                raise ValueError("Not enough cards in the deck!")
            for _ in range(count):
                self.community_cards.append(self.deal_card())

        def rotate_dealer(self):
            # Reset dealer roles
            for player in self.players:
                player.is_dealer = False

            # Assign the dealer role to the next player
            self.dealer_index = (self.dealer_index + 1) % len(self.players)
            self.players[self.dealer_index].is_dealer = True
            print(f"Dealer updated. {self.players[self.dealer_index].name} is now the Dealer.")

    ## Initialize game state and players
    game = GameState()
    game.create_deck()
    game.players.append(Player(name="Player", is_human=True))
    game.players.append(Player(name="AI Opponent", is_human=False))
    game.players[0].is_dealer = True  # Set the first player as the Dealer

    ## Function to start a new round
    def start_new_round():
        print("Starting a new round...")
        game.rotate_dealer()

        # Reset the pot and community cards
        game.pot = 0
        game.community_cards = []

        # Small blind by the dealer
        dealer = game.players[game.dealer_index]
        if dealer.chips >= 10:
            game.pot += dealer.bet(10)
        else:
            print(f"{dealer.name} cannot pay the small blind and is out of the game!")

        # Deal cards to players
        game.deal_hands()
        print("Cards dealt.")

define opponent_image = "opponent_character.png"  # Replace with your opponent image

screen poker_game():
    zorder 200
    modal True

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
            text "{b}Your Chips: [game.players[0].chips]{/b}" size 26 color "#FFFFFF"
            hbox spacing -100:
                for card in game.players[0].hand:
                    if "image" in card:
                        add card['image'] size (188, 251)
                    else:
                        add "cards/back_of_card_1.png" size (188, 251)

    # Opponent hand display
    frame:
        background "#404040"
        xalign 1.0
        yalign 0.1
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}Your Chips: [game.players[1].chips]{/b}" size 26 color "#FFFFFF"
            hbox spacing -100:
                for card in game.players[1].hand:
                    if "image" in card:
                        add card['image'] size (188, 251)
                    else:
                        add "cards/back_of_card_1.png" size (188, 251)

    # Community cards
    frame:
        xalign 0.99
        yalign 0.5
        xsize 0.21
        ysize 0.1
        hbox spacing 10:
            for card in game.community_cards:
                if "image" in card:
                    add card['image'] size (188, 251)
                else:
                    add "cards/back_of_card_1.png" size (188, 251)

    # Buttons for player actions
    frame:
        align (0.5, 0.8)
        xsize 400
        ysize 200
        vbox spacing 20:
            textbutton "Bet" action Return("bet") style "poker_button"
            textbutton "Call" action Return("call") style "poker_button"
            textbutton "Fold" action Return("fold") style "poker_button"
            textbutton "Next Round" action Return("next_round") style "poker_button"

style poker_button:
    font "Arial"
    size 18
    background "#202020"
    foreground "#FFFFFF"
    padding (10, 10)
    xsize 200
    yalign 0.5
