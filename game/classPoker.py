import random

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Card Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class Card:
    # ► Represents a playing card with a value (rank) and a color (suit).
    def __init__(self, rank, suit):
        self.rank = rank                                                                                                    # ═══► Ex: "2", "3", ..., "T", "J", "Q", "K", "A"
        self.suit = suit                                                                                                    # ═══► Ex: "H" (Hearts), "D" (Diamonds), "C" (Clubs), "S" (Spades)
    # End def
    def __repr__(self):
        # ► Representation for debugging.
        return f"Card('{self.rank}', '{self.suit}')"
    # End def
    def __str__(self):
        # ► Textual representation of the card (e.g. “AH” for Ace of Hearts).
        return f"{self.rank}{self.suit}"
    # End def
    def get_value(self):
        # ► Returns the numerical value of the card for hand ranking.
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank == 'T':
            return 10
        elif self.rank == 'J':
            return 11
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'K':
            return 13
        elif self.rank == 'A':
            return 14                                                                                                       # ═══► Ace can be 1 or 14 depending on the hand
        return 0                                                                                                            # ═══► Default value if value is not recognized
    # End def
    def get_image_name(self):
        # ► Returns the image file name for Ren'Py.
        # ► Example: ‘AH.png’ for the Ace of Hearts.
        return f"{self.rank}{self.suit}.png"
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Card Deck Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class Deck:
    # ► Manages the 52-card deck (shuffle, deal).
    def __init__(self):
        self.cards = []
        self.reset()
    # End def
    def reset(self):
        # ► Resets the deck with 52 cards and shuffles them.
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'C', 'S']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()
    # End def
    def shuffle(self):
        # ► Shuffle the cards in the deck.
        random.shuffle(self.cards)
    # End def
    def deal_card(self):
        # ► Distributes a card from the top of the deck.
        if not self.cards:
            print("The package is empty. Reset.")
            self.reset()                                                                                                    # ═══► Optional: reinitialize if the package is empty, or raise an error
        # End if
        return self.cards.pop()
    # End def
    def __len__(self):
        return len(self.cards)
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Player Class Definition (base abstraite)
# ╰─────────────────────────────────────────────────────────────────────────────
class Player:
    # ► Basic class for all game participants.
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Player Class Definition (inherits from Player)
# ╰─────────────────────────────────────────────────────────────────────────────
class HumanPlayer(Player):
    # ► Represents a poker player with chips, hand and status.
    def __init__(self, name, initial_chips, is_human=True):
        super().__init__(name, is_human)
        self.chips          = initial_chips                                                                                 # ═══► Player's current chips
        self.hand           = []                                                                                            # ═══► Player's private cards
        self.current_bet    = 0                                                                                             # ═══► Amount bet by the player in the current betting round
        self.has_folded     = False                                                                                         # ═══► "True" if the player has folded the hand
        self.is_all_in      = False                                                                                         # ═══► "True" if the player has put in all his chips
        self.is_dealer      = False                                                                                         # ═══► "True" if the player has the dealer button
        self.is_small_blind = False                                                                                         # ═══► "True" if the player has the small blind
        self.is_big_blind   = False                                                                                         # ═══► "True" if the player has the big blind
        self.bet_in_hand = 0                                                                                                # ═══► Total bet by the player over the entire hand (for secondary pots)
    # End def
    def add_chips(self, amount):
        # ► Add chips to the player.
        self.chips      += amount
        print(f"{self.name} wins {amount} chips. Total: {self.chips}")
    # End def
    def remove_chips(self, amount):
        # ► Removes chips from the player. Handles the all-in case.
        # ► Returns the actual amount paid.
        if self.chips   >= amount:
            self.chips  -= amount
            return amount
        else:                                                                                                               # ═══► Can't pay in full, goes all-in
            all_in_amount   = self.chips
            self.chips      = 0
            self.is_all_in  = True
            return all_in_amount
        # End if
    # End def
    def reset_hand(self):
        # ► Resets player status for a new hand.
        self.hand           = []
        self.current_bet    = 0
        self.has_folded     = False
        self.is_all_in      = False
        #  ► Dealer/blind statuses are managed by the PokerGame class for each hand.
    # End def
    def can_check(self, current_bet_to_match):
        # ► Controls if the player can check (no bet to match).
        return current_bet_to_match == self.current_bet
    # End def
    def can_call(self, current_bet_to_match):
        # ► Checks if the player can call (must match a bet and has chips).
        return current_bet_to_match > self.current_bet and self.chips > 0
    # End def
    def get_call_amount(self, current_bet_to_match):
        # ► Calculates the amount needed for ‘call’.
        return current_bet_to_match - self.current_bet
    # End def
    def can_bet(self, min_bet=0):
        # ► Checks if the player can "bet" (nobody has bet and he has chips).
        return self.chips > 0 and self.current_bet == 0                                                                     # ═══► Can bet if no one has bet and has chips
    # End def
    def can_raise(self, current_bet_to_match, min_raise_amount):
        # ► Checks if the player can "raise" (someone has bet, he has chips and can raise).
        # ► The player must be able to match the current bet and add at least the minimum raise.
        amount_to_match = current_bet_to_match - self.current_bet
        return self.chips >= (amount_to_match + min_raise_amount) and (amount_to_match + min_raise_amount) > 0              # ═══► Must have chips to pay call and raise
    # End def
    def perform_action(self, action_type, amount_needed=0, raise_amount=0):
        # ► Performs the action chosen by the player.
        # ► Returns the total amount bet by the player in this action.
        print(f"{self.name} ({self.chips} chips) performs {action_type}.")
        bet_made_this_action = 0
        if action_type == "fold":
            self.has_folded = True
            print(f"{self.name} folds.")
        elif action_type == "check":
            if self.can_check(amount_needed):
                print(f"{self.name} checks.")
            else:
                print(f"WARNING: {self.name} tried to "check" but couldn't (bet to match={amount_needed}, current bet={self.current_bet}).
            # End if
        elif action_type == "call":
            call_amount = self.get_call_amount(amount_needed)
            actual_paid = self.remove_chips(call_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} calls {actual_paid} (total bet in the round: {self.current_bet}). Remaining chips: {self.chips}")
        elif action_type == "bet":
            bet_amount = amount_needed                                                                                     # ═══► For an initial bet, amount_needed is the bet amount
            actual_paid = self.remove_chips(bet_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} bets {actual_paid} (total bet in round: {self.current_bet}). Remaining chips: {self.chips}")
        elif action_type == "raise":
            amount_to_call = amount_needed - self.current_bet                                                               # ═══► Le montant total de la mise après le raise
            total_raise_amount_needed = amount_to_call + raise_amount
            actual_paid = self.remove_chips(total_raise_amount_needed)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} raises to {self.current_bet} (added {actual_paid}). Remaining chips: {self.chips}")
        elif action_type == "all_in":
            if self.is_all_in:                                                                                              # ═══► If the player is already all-in, he bets nothing more
                print(f"{self.name} is already ALL-IN.")
                return 0
            # End if
            actual_paid = self.remove_chips(self.chips)                                                                     # ═══► Bet all remaining chips
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            self.is_all_in = True
            print(f"{self.name} goes ALL-IN for {actual_paid} (total bet in round: {self.current_bet}).")
        else:
            print(f"Action not recognized: {action_type}")
        # End if
        return bet_made_this_action
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Robot Class Definition (inherits from Player)
# ╰─────────────────────────────────────────────────────────────────────────────
class RobotPlayer(HumanPlayer):
    # ► Represents an AI player with a decision logic.
    def __init__(self, name, initial_chips, aggression_level=3):
        super().__init__(name, initial_chips, is_human=False)
        self.aggression_level = aggression_level                                                                            # ═══► 1 (passive) à 5 (very aggressive)
    # End def
    def decide_action(self, current_bet_to_match, pot_size, num_active_players, community_cards, small_blind_val, big_blind_val):
        # ► Decides AI action (fold, check, call, bet, raise, all-in).
        # ► This is a VERY SIMPLIFIED AI LOGIC and a PLACEHOLDER.
        # ► A realistic poker AI is extremely complex and requires (todo list):
        #     - An accurate assessment of hand strength (your own hand + community cards).
        #     - Analysis of pot odds.
        #     - Reading opponents (betting patterns, history).
        #     - Table position.
        #     - Phase of play (pre-flop, flop, turn, river).
        #     - Stack size management.

        # ► Calculates hand strength (PLACEHOLDER: (todo) implement a real evaluator!)
        combined_cards = self.hand + community_cards
        hand_rank, hand_description = get_hand_rank_and_description(combined_cards)
        # ► hand_rank: a number for strength (e.g. 1=high card, 2=pair, ..., 9=straight flush)
        # ► description_de_la_main : "Paire d'As", "Couleur", etc.
        
        # ► Adapted to hand strength (hand_rank) and aggressiveness level.
        # ► hand_strength_score is a value between 0 and 1 (0 = weak, 1 = very strong)
        hand_strength_score = hand_rank / 9.0                                                                               # ═══► Max 9 main hand types

        print(f"Robot {self.name}: Hand Strength Score = {hand_strength_score:.2f} ({hand_description})")

        amount_to_call   = current_bet_to_match - self.current_bet                                                          # ═══► Calculate potential amounts
        min_bet_amount   = big_blind_val * 2                                                                                # ═══► Standard initial bet (2x BB)
        min_raise_amount = big_blind_val * 2                                                                                # ═══► Standard minimum raise amount

        # ► Decision logic
        if self.chips <= 0:
            return {"action": "check"}                                                                                      # ═══► If all-in or 0 chips, can do nothing else
        # End if
        if current_bet_to_match == self.current_bet:                                                                        # ═══► No bet to match (can Check or Bet)
            if hand_strength_score > 0.6 + (self.aggression_level * 0.05):                                                  # ═══► Strong hand or aggressive hand
                bet_amount = min(self.chips, big_blind_val)                                                                 # ═══► Try to bet higher if aggressive
                if bet_amount > 0:
                    return {"action": "bet", "amount": bet_amount}
                else:                                                                                                       # ═══► Not enough chips for a significant bet, so check
                    return {"action": "check"}
                # End if
            else:                                                                                                           # ═══► Weak hand or non-aggressive hand
                return {"action": "check"}
            # End if
        else:                                                                                                               # ═══► There's a bet to match (can Fold, Call or Raise)
            if self.chips < amount_to_call:                                                                                 # ═══► Not enough chips to call
                if self.chips > 0:                                                                                          # ═══► Can go all-in
                    return {"action": "all_in"}
                else:
                    return {"action": "fold"}                                                                               # ═══► No chips, must fold (or is already all-in)
                # End if
            # End if
            # ► Calculation of the probability of a restart/counter/counter as a function of strength and aggressiveness
            fold_threshold = 0.3 - (self.aggression_level * 0.05)                                                           # ═══► More aggressive = less likely to fold
            call_threshold = 0.5 + (self.aggression_level * 0.02)                                                           # ═══► More aggressive = more likely to call/raise
            if hand_strength_score < fold_threshold:
                return {"action": "fold"}
            elif hand_strength_score < call_threshold or not self.can_raise(current_bet_to_match, min_raise_amount):
                return {"action": "call", "amount_needed": current_bet_to_match}                                            # ═══► Strong enough to call, or can't raise
            else:                                                                                                           # ═══► Strong enough to raise and can raise
                raise_by_amount = min(self.chips - amount_to_call, big_blind_val)
                if raise_by_amount < big_blind_val and self.chips - amount_to_call > 0:                                     # ═══► If not enough for a real raise, goes all-in (and has chips)
                    return {"action": "all_in"}
                elif raise_by_amount < big_blind_val and self.chips - amount_to_call <= 0:                                  # ═══► If no chips to raise
                    return {"action": "call", "amount_needed": current_bet_to_match}                                        # ═══► So call
                else:                                                                                                       # ═══► Can raise from the Big Blind
                    return {"action": "raise", "amount_needed": current_bet_to_match, "raise_by": raise_by_amount}
            # End if
        # End if
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Game Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class PokerGame:
    # ► Manages the overall state of the poker game, players, rounds, pot and distribution.
    # ► Game constants (can be configured)
    SMALL_BLIND_VAL     = 5
    BIG_BLIND_VAL       = 10
    INITIAL_CHIPS       = 1000

    # ► Game states for logic flow and game display
    GAME_STATE_PREFLOP  = "preflop"
    GAME_STATE_FLOP     = "flop"
    GAME_STATE_TURN     = "turn"
    GAME_STATE_RIVER    = "river"
    GAME_STATE_SHOWDOWN = "showdown"
    GAME_STATE_END_HAND = "end_hand"

    def __init__(self, human_player_name="Player", num_ai_players=1):                                                       # ═══► 1 AI by default
        self.deck = Deck()
        self.players = []
        self.players.append(PokerPlayer(human_player_name, self.INITIAL_CHIPS, is_human=True))                              # ═══► Add the human player
        for i in range(num_ai_players):                                                                                     # ═══► Add the robot player
            self.players.append(AIPlayer(f"AI Player {i+1}", self.INITIAL_CHIPS, aggression_level=random.randint(1, 5)))
        # End for
        self.dealer_index = random.randint(0, len(self.players) - 1)                                                        # ═══► Initial Dealer position
        self.community_cards        = []
        self.pot                    = 0
        self.current_highest_bet    = 0
        self.current_player_index   = -1                                                                                    # ═══► Index of the player whose turn it is
        self.game_state             = None                                                                                  # ═══► Current state of game (preflop, flop, etc.)
        self.last_raiser_index      = -1                                                                                    # ═══► Index of the last player to make an aggressive action (bet/raise)
        self.num_hands_played       = 0                                                                                     # ═══► Hands played counter

        print("Poker game initialized.")
