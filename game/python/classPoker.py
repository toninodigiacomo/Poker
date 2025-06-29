import random
import math                                                                                                                 # ═══► Importation for math.ceil

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global module variable
# ╰─────────────────────────────────────────────────────────────────────────────
_CARD_IMAGE_BASE_PATH = "images/cards/"                                                                                     # ═══► Default path (with a “/” at the end)

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
    def get_image_name(self):
        # ► Returns the image file name for Ren'Py.
        # ► Example: ‘AH.png’ for the Ace of Hearts.
        return f"{_CARD_IMAGE_BASE_PATH}{self.rank}{self.suit}.png"
    # End def
    def get_value(self, aces_high=True):
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
            return 14 if aces_high else 1                                                                                   # ═══► Ace can be 1 or 14 depending on the hand
        return 0                                                                                                            # ═══► Default value if value is not recognized
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
    def __len__(self):
        return len(self.cards)
    # End def
    def deal_card(self):
        # ► Distributes a card from the top of the deck.
        if not self.cards:
            print("The package is empty. Reset.")
            self.reset()                                                                                                    # ═══► Optional: reinitialize if the package is empty, or raise an error
        # End if
        return self.cards.pop()
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
    def can_bet(self, min_bet=0):
        # ► Checks if the player can "bet" (nobody has bet and he has chips).
        return self.chips > 0 and self.current_bet == 0                                                                     # ═══► Can bet if no one has bet and has chips
    # End def
    def can_call(self, current_bet_to_match):
        # ► Checks if the player can call (must match a bet and has chips).
        return current_bet_to_match > self.current_bet and self.chips > 0
    # End def
    def can_check(self, current_bet_to_match):
        # ► Controls if the player can check (no bet to match).
        return current_bet_to_match == self.current_bet
    # End def
    def can_raise(self, current_bet_to_match, min_raise_amount):
        # ► Checks if the player can "raise" (someone has bet, he has chips and can raise).
        # ► The player must be able to match the current bet and add at least the minimum raise.
        amount_to_match = current_bet_to_match - self.current_bet
        return self.chips >= (amount_to_match + min_raise_amount) and (amount_to_match + min_raise_amount) > 0              # ═══► Must have chips to pay call and raise
    # End def
    def get_call_amount(self, current_bet_to_match):
        # ► Calculates the amount needed for ‘call’.
        return current_bet_to_match - self.current_bet
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
                print(f"WARNING: {self.name} tried to Check but couldn't (bet to match={amount_needed}, current bet={self.current_bet}).")
            # End if
        elif action_type == "call":
            call_amount = self.get_call_amount(amount_needed)
            actual_paid = self.remove_chips(call_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} calls {actual_paid} (total bet in the round: {self.current_bet}). Remaining chips: {self.chips}")
        elif action_type == "bet":
            bet_amount = int(math.ceil(amount_needed / 10.0))                                                               # ═══► Ensure bet amount is a multiple of 10
            actual_paid = self.remove_chips(bet_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} bets {actual_paid} (total bet in round: {self.current_bet}). Remaining chips: {self.chips}")
        elif action_type == "raise":
            amount_to_call = amount_needed - self.current_bet                                                               # ═══► Le montant total de la mise après le raise
            raise_amount = int(math.ceil(raise_amount / 10.0)) * 10 if raise_amount % 10 != 0 else raise_amount             # ═══► Ensure raise amount is a multiple of 10
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
            self.has_acted_in_round = True
            print(f"{self.name} goes ALL-IN for {actual_paid} (total bet in round: {self.current_bet}).")
        else:
            print(f"Action not recognized: {action_type}")
        # End if
        return bet_made_this_action
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
    def reset_for_new_hand(self):
        # ► Resets player status for a new hand.
        self.hand               = []
        self.current_bet        = 0
        self.has_folded         = False
        self.is_all_in          = False
        self.has_acted_in_round = False                                                                                     # ═══► Reset this flag for the new hand
        #  ► Dealer/blind statuses are managed by the PokerGame class for each hand.
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
        # ► description_de_la_main : "Pair of Aces", "Flush", etc.

        # ► Adapted to hand strength (hand_rank) and aggressiveness level.
        # ► hand_strength_score is a value between 0 and 1 (0 = weak, 1 = very strong)
        hand_strength_score = hand_rank / 9.0                                                                               # ═══► Max 9 main hand types

        print(f"Robot {self.name}: Hand Strength Score = {hand_strength_score:.2f} ({hand_description})")

        amount_to_call   = current_bet_to_match - self.current_bet                                                          # ═══► Calculate potential amounts
        min_bet_amount   = big_blind_val                                                                                    # ═══► Standard initial bet (was 2x BB, now just BB for cleaner multiples)
        min_raise_amount = big_blind_val                                                                                    # ═══► Standard minimum raise amount

        min_bet_amount = int(math.ceil(min_bet_amount / 10.0)) * 10                                                         # ═══► Rounding for multiples of 10 for AI decisions
        min_raise_amount = int(math.ceil(min_raise_amount / 10.0)) * 10

        # ► Decision logic
        if self.chips <= 0:
            return {"action": "check"}                                                                                      # ═══► If all-in or 0 chips, can do nothing else
        # End if
        if current_bet_to_match == self.current_bet:                                                                        # ═══► No bet to match (can Check or Bet)
            if hand_strength_score > 0.6 + (self.aggression_level * 0.05):                                                  # ═══► Strong hand or aggressive hand
                bet_amount = min(self.chips, min_bet_amount)                                                                # ═══► Try to bet higher if aggressive
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
                raise_by_amount = min(self.chips - amount_to_call, min_raise_amount)
                if raise_by_amount % 10 != 0:                                                                               # ═══► Ensure raise_by_amount is a multiple of 10
                    raise_by_amount = int(math.ceil(raise_by_amount / 10.0)) * 10

                if raise_by_amount < min_raise_amount and self.chips - amount_to_call > 0:                                  # ═══► If not enough for a real raise, goes all-in (and has chips)
                    return {"action": "all_in"}
                elif raise_by_amount < min_raise_amount and self.chips - amount_to_call <= 0:                               # ═══► If no chips to raise
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
    DEFAULT_SMALL_BLIND_VAL         = 10
    DEFAULT_BIG_BLIND_VAL           = 20
    DEFAULT_INITIAL_CHIPS           = 200
    # ► Game states for logic flow and game display
    GAME_STATE_PREFLOP              = "preflop"
    GAME_STATE_FLOP                 = "flop"
    GAME_STATE_TURN                 = "turn"
    GAME_STATE_RIVER                = "river"
    GAME_STATE_SHOWDOWN             = "showdown"
    GAME_STATE_END_HAND             = "end_hand"

    def __init__(self, human_player_name="Player", num_ai_players=1, card_image_base_path=None, small_blind_val=None, big_blind_val=None, initial_chips_val=None):
        if card_image_base_path is not None:                                                                                # ═══► Update the module's global variable if a path is provided
            global _CARD_IMAGE_BASE_PATH                                                                                    # ═══► Indicates that we are modifying the global variable
            _CARD_IMAGE_BASE_PATH = card_image_base_path
            if not _CARD_IMAGE_BASE_PATH.endswith('/'):                                                                     # ═══► Make sure the path ends with a “/” for easy concatenation
                _CARD_IMAGE_BASE_PATH += '/'
            # End if
            print(f"Base path for map images set to: {_CARD_IMAGE_BASE_PATH}")
        # End if
        self.small_blind_val            = small_blind_val if small_blind_val is not None else self.DEFAULT_SMALL_BLIND_VAL  # ═══► Define the blind values for this instance
        self.big_blind_val              = big_blind_val if big_blind_val is not None else self.DEFAULT_BIG_BLIND_VAL
        self.initial_chips_per_player   = initial_chips_val if initial_chips_val is not None else self.DEFAULT_INITIAL_CHIPS
        self.small_blind_val            = int(math.ceil(self.small_blind_val / 10.0)) * 10                                  # ═══► Ensure that blinds are multiples of 10
        self.big_blind_val              = int(math.ceil(self.big_blind_val / 10.0)) * 10
        if self.big_blind_val           < 2 * self.small_blind_val:                                                         # ═══► Ensure that the big blind is at least double the small blind
            self.big_blind_val          = 2 * self.small_blind_val
        # End if
        self.deck                       = Deck()                                                                            # ═══► Initialisation without cards_to_use
        self.players                    = []
        self.players.append(HumanPlayer(human_player_name, self.initial_chips_per_player, is_human=True))                   # ═══► Add the human player
        for i in range(num_ai_players):                                                                                     # ═══► Add the robot player
            self.players.append(RobotPlayer(f"AI Player {i+1}", self.initial_chips_per_player, aggression_level=random.randint(1, 5)))
        # End for
        self.dealer_index = random.randint(0, len(self.players) - 1)                                                        # ═══► Initial Dealer position
        self.community_cards            = []
        self.pot                        = 0
        self.current_highest_bet        = 0
        self.current_player_index       = -1                                                                                # ═══► Index of the player whose turn it is
        self.game_state                 = None                                                                              # ═══► Current state of game (preflop, flop, etc.)
        self.last_raiser_index          = -1                                                                                # ═══► Index of the last player to make an aggressive action (bet/raise)
        self.num_hands_played           = 0                                                                                 # ═══► Hands played counter
        print("Poker game initialized.")
    # End def
    def assign_blinds(self):
        # ► Assign small and large blinds and collect initial bets.
        players_in_hand = self.get_players_in_hand_for_showdown()
        if len(players_in_hand) < 2:
            print("Not enough players in hand to assign blinds.")
            return
        # End if
        sb_player = None                                                                                                    # ═══► Logic to determine sb_player and bb_player for heads-up and 3+ players
        bb_player = None
        if len(players_in_hand) == 2:                                                                                       # ═══► Heads-up: Dealer is SB, other is BB
            dealer_player = self.players[self.dealer_index]
            other_player_in_hand = [p for p in players_in_hand if p != dealer_player]                                       # ═══► Ensure we find the *other* player in `players_in_hand`, not just `self.players`
            if other_player_in_hand:
                sb_player = dealer_player
                bb_player = other_player_in_hand[0]
            else:                                                                                                           # ═══► Should not happen if len(players_in_hand) == 2
                print("Error: Could not find distinct players for blinds in heads-up.")
                return
            # End if
        # else:                                                                                                               # ═══► 3+ players: normal blind assignment
        #     current_idx = self.dealer_index                                                                                 # ═══► Find SB and BB correctly based on dealer_index and active players
        #     # Find Small Blind
        #     for _ in range(len(self.players)):                                                                              # ═══► Loop through all players
        #         current_idx = (current_idx + 1) % len(self.players)
        #         if self.players[current_idx] in players_in_hand:                                                            # ═══► Must be an active player in the hand
        #             sb_player = self.players[current_idx]
        #             break
        #         # End if
        #     # End for
        #     # Find Big Blind
        #     for _ in range(len(self.players)):                                                                              # ═══► Loop through all players starting after SB
        #         current_idx = (current_idx + 1) % len(self.players)
        #         if self.players[current_idx] in players_in_hand:                                                            # ═══► Must be an active player in the hand
        #             bb_player = self.players[current_idx]
        #             break
        #         # End if
        #     # End for
        # End if
        if sb_player and sb_player.chips > 0:
            sb_paid = sb_player.remove_chips(self.small_blind_val)                                                          # ═══► Use instance attribute
            sb_player.current_bet += sb_paid
            sb_player.bet_in_hand += sb_paid
            self.pot += sb_paid                                                                                             # ═══► Add to pot here, this is the only direct pot addition for blinds
            sb_player.is_small_blind = True
            print(f"{sb_player.name} pays the Small Blind: {sb_paid}")
        # End if
        if bb_player and bb_player.chips > 0:
            bb_paid = bb_player.remove_chips(self.big_blind_val)                                                            # ═══► Use instance attribute
            bb_player.current_bet += bb_paid
            bb_player.bet_in_hand += bb_paid
            self.pot += bb_paid                                                                                             # ═══► Add to pot here, this is the only direct pot addition for blinds
            self.current_highest_bet = self.big_blind_val                                                                   # ═══► Use instance attribute
            bb_player.is_big_blind = True
            print(f"{bb_player.name} pays the Big Blind: {bb_paid}")
        # End if
        print(f"Highest bet after the blinds: {self.current_highest_bet}. Pot: {self.pot}")
    # End def
    def collect_bets_to_pot(self):
        # ► Moves chips wagered by players to the main pot.
        print(f"DEBUG: Pot before collection of bets: {self.pot}")
        for player in self.players:
            print(f"DEBUG: player: {player.name}")
            print(f"DEBUG: player.current_bet: {player.current_bet}")
            if player.current_bet > 0:
                self.pot += player.current_bet
                player.current_bet = 0                                                                                      # ═══► Reset the round bet for the next round
            # End if
        # End for
        print(f"DEBUG: Pot after collection of bets: {self.pot}")
        print(f"All bets collected in the pot. Current pot: {self.pot}")
    # End def
    def deal_community_cards(self, num_cards):
        # ► Deal common cards on the table (Flop, Turn, River).
        if num_cards > len(self.deck.cards):
            print("Not enough cards in the deck to deal.")
            return
        # End if
        for _ in range(num_cards):
            if len(self.deck.cards) > 0:                                                                                    # ═══► Burning a card before dealing (poker convention)
                self.deck.deal_card()                                                                                       # ═══► Card burnt (discarded)
            else:
                print("The deck is empty before burning a card.")
                break                                                                                                       # ═══► Do not continue if the pack is empty
            # End if
            self.community_cards.append(self.deck.deal_card())
        # End for
        print(f"Common cards distributed: {', '.join(str(c) for c in self.community_cards)}")
    # End def
    def deal_hole_cards(self):
        # ► Distribue 2 cartes privées à chaque joueur actif."""
        for _ in range(2):                                                                                                  # ═══► 2 cards per player
            for player in self.players:
                if not player.has_folded:                                                                                   # ═══► Do not distribute to eliminated/folded players
                    player.hand.append(self.deck.deal_card())
                # End if
            # End for
        # End for
        print("Private cards distributed.")
    # End def
    def determine_winner(self):
        # ► Determines the winner(s) of the hand and the description of the winning hand.
        # ► This is a MAJOR PLACEHOLDER and must be replaced by a complete poker hand evaluation algorithm (e.g. Straight Flush, Four of a Kind, etc.).
        players_in_hand = self.get_players_in_hand_for_showdown()
        print(f"DEBUG determine_winner: Non-folded players: {[p.name for p in players_in_hand]}")

        if not players_in_hand:
            print("DEBUG determine_winner: No players in hand to determine a winner (all folded or eliminated).")
            return None, "No one won (everyone folded)."
        # End if
        if len(players_in_hand) == 1:
            winner = players_in_hand[0]
            print(f"DEBUG determine_winner: {winner.name} wins by default (all others have folded).")
            return [winner], f"{winner.name} wins by default!"
        # End if
        # ═══► START OF HAND EVALUATION (SIMPLIFIED PLACEHOLDER!) ◀═══
        # ► TODO: REPLACE THIS SECTION WITH A REAL POKER HAND EVALUATOR.
        # ►       Python libraries such as “deuces” or “poker-eval” can be useful.
        best_hand_rank = -1 # Use -1 to ensure that even a “High Card” wins initially
        winners = []
        winning_description = ""
        for player in players_in_hand: # Loop through players in hand for showdown
            # ► Combination of the player's 2 cards and 5 common cards (max. 7 cards)
            # ► Objective: to find the best 5-card hand among these 7.
            player_all_cards = player.hand + self.community_cards # Calling the "bogus" hand evaluator
            current_player_hand_rank, current_player_desc = get_hand_rank_and_description(player_all_cards)                 # ═══► get_hand_rank_and_description should take the player's hand + common cards
            print(f"DEBUG: {player.name}'s best hand: {current_player_desc} (Rank: {current_player_hand_rank})")
            if current_player_hand_rank > best_hand_rank:
                best_hand_rank = current_player_hand_rank
                winners = [player]
                winning_description = f"{player.name} wins with {current_player_desc}."
            elif current_player_hand_rank == best_hand_rank: # Handle ties (kickers, etc.). The hand evaluator should handle this
                winners.append(player)                                                                                      # ═══► PLACEHOLDER (simplified) co-winners
                winning_description += f" and {player.name} (also with {current_player_desc})."
            # End if
        # End for
        # ═══►  END OF HAND EVALUATION (SIMPLIFIED PLACEHOLDER!)  ◀═══
        if not winners:                                                                                                     # ═══► It should not happen
            return None, "Error: No winner found despite active players."
        # End if
        if len(winners) > 1:
            winning_description = f"Pot shared between: {', '.join(w.name for w in winners)}."                              # ═══► The desc will be the same for shares
        # End if
        print(f"Winner(s): {', '.join(w.name for w in winners)}. Description: {winning_description}")
        return winners, winning_description
    # End def
    def distribute_pot(self, winners):
        # ► Distribute the pot to the winners.
        if not winners:
            print("No winner to distribute the pot.")
            return
        # End if
        print(f"DEBUG: Attempt to distribute the {self.pot} to the winners: {[w.name for w in winners]}")
        amount_per_winner = self.pot // len(winners)
        remaining_pot = self.pot % len(winners)                                                                             # ═══► To manage odd-numbered chips
        for winner in winners:
            winner.add_chips(amount_per_winner)
            print(f"{winner.name} receives {amount_per_winner} from the pot.")
        # End for
        if remaining_pot > 0:                                                                                               # ═══► Distribute the remaining chips (if the pot is not divisible) to the first winner, or to the dealer.
            if winners:
                winners[0].add_chips(remaining_pot)
                print(f"{winners[0].name} receives the remaining token from {remaining_pot}.")
            else:
                print(f"Remaining {remaining_pot} not distributed.")                                                        # ═══► If for any reason there is no winner but a remaining pot
        # End if
        self.pot = 0                                                                                                        # ═══► The pot is emptied after distribution
        print(f"Pot distributed. Final pot: {self.pot}")
    # End def
    def get_current_player(self):
        # ► Returns the Player object whose turn it is.
        if self.current_player_index == -1 or not self.players:
            return None
        # End if
        return self.players[self.current_player_index]
    # End def
    def get_next_player_to_act(self):
        # ► Determines the next player who must act in the betting round.
        # ► Manages player rotation and skips those who have folded or are all-in.
        # ► Determine the effective start index for searching for the next player.
        # ► This is typically the player after the one who just acted.
        # ► If it's the very first action of a betting round, `current_player_index` would have been set by `start_betting_round`.
        if self.current_player_index == -1:                                                                                 # ═══► Fallback if current_player_index somehow isn't set, start after dealer
            start_idx_for_search = (self.dealer_index + 1) % len(self.players)
            initial_check_count = 0                                                                                         # ═══► Ensure this fallback skips folded/all-in players to find a true starting point
            while (self.players[start_idx_for_search].has_folded or self.players[start_idx_for_search].is_all_in) and initial_check_count < len(self.players):
                start_idx_for_search = (start_idx_for_search + 1) % len(self.players)
                initial_check_count += 1
            # End while
            if initial_check_count == len(self.players):                                                                    # ═══► No eligible player found
                print("DEBUG get_next_player_to_act: No eligible players found in fallback search.")
                return None
            # End if
        else:
            start_idx_for_search = (self.current_player_index + 1) % len(self.players)
        # End if
        original_start_idx_for_loop_detection = start_idx_for_search                                                        # ═══► To detect a full circle
        for _ in range(len(self.players)):                                                                                  # ═══► Iterate through all players (at most one full circle)
            player = self.players[start_idx_for_search]
            if player.has_folded or player.is_all_in:                                                                       # S═══► kip players who have folded or are all-in (they cannot make a betting action)
                start_idx_for_search = (start_idx_for_search + 1) % len(self.players)
                continue                                                                                                    # ═══► Move to the next player
            # End if
            # ► This player is active. Now, does this player NEED to act?
            # ► A player needs to act if:
            #     1. There's a bet to match (highest_bet > 0) AND the player hasn't matched it yet (current_bet < highest_bet).
            #     2. OR, if there's NO bet (highest_bet == 0) AND the player hasn't acted yet in THIS betting round.
            if (self.current_highest_bet > 0 and player.current_bet < self.current_highest_bet) or (self.current_highest_bet == 0 and not player.has_acted_in_round):
                self.current_player_index = start_idx_for_search # Set this player as the current acting player
                print(f"DEBUG get_next_player_to_act: Found {player.name} (idx {start_idx_for_search}) to act.")
                print(f"  Current bet: {player.current_bet}, Highest bet: {self.current_highest_bet}, Has acted this round: {player.has_acted_in_round}")
                return player
            # End if
            start_idx_for_search = (start_idx_for_search + 1) % len(self.players)                                           # ═══► If the player doesn't need to act, move to the next player in the circle
            # ► Important: If we've completed a full circle and haven't found anyone who needs to act, it means the betting round is implicitly over.
            if start_idx_for_search == original_start_idx_for_loop_detection:
                print("DEBUG get_next_player_to_act: Completed a full circle, no one else needs to act.")
                break                                                                                                       # ═══► All active players have been checked, and none need to act
            # End if
        # End if
        print("DEBUG get_next_player_to_act: No player found who needs to make an action. Betting round potentially over.")
        return None                                                                                                         # ═══► No one needs to act in this round
    # End def
    def get_players_in_hand_for_showdown(self):
        # ► Returns the list of players who have not folded.
        # ► Includes players who are all-in as they are still eligible for the pot.
        return [p for p in self.players if not p.has_folded]
    # End def
    def get_players_remaining_in_game(self):
        # ► Returns the list of players who still have chips > 0, meaning they are not eliminated from the game.
        return [p for p in self.players if p.chips > 0]
    # End def
    def get_players_who_can_make_betting_action(self):
        # Returns the list of players who are not folded, not all-in, and have chips.
        return [p for p in self.players if not p.has_folded and not p.is_all_in and p.chips > 0]
    # End def
    def is_betting_round_over(self):
        # ► Checks if the current betting round has ended.
        # ► A round is over when:
        #     1. Only one player remains in the hand (others folded).
        #     2. OR, if all players still in the hand have matched the highest bet or are all-in.
        players_in_hand = self.get_players_in_hand_for_showdown()
        print(f"DEBUG is_betting_round_over: Checking end of round. Players in hand: {[p.name for p in players_in_hand]}")
        # ► Condition 1: Only one player left in the hand (all others folded).
        if len(players_in_hand) <= 1:
            print("DEBUG is_betting_round_over: Less than 2 players remaining in hand. Round over (hand ends).")
            return True
        # End if
        # ► Condition 2: Check if all players in hand have matched the highest bet or are all-in.
        all_bets_equalized = True
        for p in players_in_hand:
            if not p.is_all_in and p.current_bet < self.current_highest_bet:
                all_bets_equalized = False
                print(f"DEBUG is_betting_round_over: {p.name} has not matched the bet ({p.current_bet} vs {self.current_highest_bet}).")
                break
            # End if
        # End for
        if not all_bets_equalized:
            print("DEBUG is_betting_round_over: All bets are not equalized. The round is not over.")
            return False
        # ► If current_highest_bet is 0, it means no one has placed a bet yet (only checks or folds have happened).
        # ► In this case, the round is only over if all players who could have acted have indeed acted.
        if self.current_highest_bet == 0:
            players_who_can_bet = self.get_players_who_can_make_betting_action()
            if not players_who_can_bet:                                                                                     # ═══► If there are no players who can make a betting action (e.g., all folded/all-in), the round is over.
                print("DEBUG is_betting_round_over: All bets are zero, and no player can make a betting action. Round over.")
                return True
            # End if
            # ► If there are players who can bet, ensure all of them have acted at least once in this zero-bet round.
            # ► This prevents the round from ending prematurely when all current_bet are 0.
            for p in players_who_can_bet:
                if not p.has_acted_in_round:
                    print(f"DEBUG is_betting_round_over: All bets are zero, but {p.name} has not yet acted in this round. Round NOT over.")
                    return False                                                                                            # ═══► Round is not over if someone hasn't acted yet in a zero-bet round.
                # End if
            # End for
            # ► If we reach here, it means all players who could bet have acted, and all bets are zero.
            print("DEBUG is_betting_round_over: All bets are zero, and all eligible players have acted. Round over.")
            return True
        # ► If current_highest_bet > 0 and all_bets_equalized is True, it means everyone has called or raised to the highest bet. The round is over.
        print("DEBUG is_betting_round_over: All bets are equalized and > 0. Round over.")
        return True
    # End def
    def reset_hand(self):
        # ► Resets the state of the game for a new hand.
        self.deck.reset()
        for player in self.players:
            player.reset_for_new_hand()                                                                                     # ═══► Resets the stats of the player's hand
        self.community_cards = []
        self.pot = 0
        self.current_highest_bet = 0
        self.current_player_index = -1
        self.game_state = None
        self.last_raiser_index = -1
        self.num_hands_played += 1
        active_indices = [i for i, p in enumerate(self.players) if p.chips > 0]                                             # ═══► Turn the dealer chip
        if not active_indices:
            print("No more active players, game over.")
            return
        # End if
        new_dealer_found = False                                                                                            # ═══► Find the next active dealer
        for i in range(1, len(self.players) + 1):
            potential_dealer_idx = (self.dealer_index + i) % len(self.players)
            if self.players[potential_dealer_idx].chips > 0:
                self.dealer_index = potential_dealer_idx
                new_dealer_found = True
                break
            # End if
        # End for
        if not new_dealer_found:                                                                                            # ═══► Should not happen if at least one active player
            print("Error: no new active dealer found.")
            return
        # End if
        for i, player in enumerate(self.players):
            player.is_dealer = (i == self.dealer_index)
            player.is_small_blind = False
            player.is_big_blind = False
        # End for
        print(f"New hand. Dealer: {self.players[self.dealer_index].name}")
    # End def
    def start_betting_round(self):
        # ► Prepares the game for a new betting round.
        for p in self.players:                                                                                              # ═══► Reset the round stakes for each active player
            p.current_bet = 0
        # End for
        # ► The current_highest_bet is not reset to 0 if it is pre-flop because the blinds have already established a bet. For post-flop rounds, it is 0.
        if self.game_state != self.GAME_STATE_PREFLOP:
             self.current_highest_bet = 0
        # End if
        # ► Determine the first player to speak for this round.
        # ► At pre-flop, the action starts with the player after the big blind.
        # ► On the following rounds (flop, turn, river), the action starts with the first active player after the dealer..
        start_player_found = False
        players_in_hand = self.get_players_in_hand_for_showdown()                                                           # ═══► Use players_in_hand for general hand status

        if not players_in_hand:
            self.current_player_index = -1
            print("No players in hand to start the betting round.")
            return
        # End if
        eligible_to_act_players_in_round_start = self.get_players_who_can_make_betting_action()                             # ═══►  Find the actual first player to act (who can make a betting action)
        if not eligible_to_act_players_in_round_start:
            self.current_player_index = -1
            print("No players eligible to make a betting action at the start of the round. Skipping betting round.")
            return
        # End if
        if self.game_state == self.GAME_STATE_PREFLOP:                                                                      # ═══► Action starts after the big blind
            bb_player = next((p for p in self.players if p.is_big_blind), None)
            if bb_player:
                bb_index = self.players.index(bb_player)
                for i in range(1, len(self.players) + 1):                                                                   # ═══► Look for the player after the BB
                    idx = (bb_index + i) % len(self.players)
                    if self.players[idx] in eligible_to_act_players_in_round_start:                                         # ═══► Must be eligible to act
                        self.current_player_index = idx
                        start_player_found = True
                        break
                    # End if
                # End for
            # End if
        else:                                                                                                               # ═══► Flop, Turn, River
            dealer_idx = self.dealer_index                                                                                  # ═══► Action begins with the first active player after the dealer
            for i in range(1, len(self.players) + 1):
                idx = (dealer_idx + i) % len(self.players)
                if self.players[idx] in eligible_to_act_players_in_round_start:                                             # ═══► Must be eligible to act
                    self.current_player_index = idx
                    start_player_found = True
                    break
                # End if
            # End for
        # End if
        if not start_player_found:
            self.current_player_index = -1
            print("Unable to find the first player to act in this betting round. The betting round could be over already.")
            return
        # End if
        self.last_raiser_index = self.current_player_index                                                                  # ═══► Initializes the last raiser to the first to act
        print(f"Start of the '{self.game_state}' betting round. First to act Début du tour de mise: {self.players[self.current_player_index].name}")
    # End def
# End class
def get_hand_rank_and_description(cards):
    # ► (PLACEHOLDER) Evaluates a hand of cards and returns a numerical rank and description.
    # ►    This function is VERY SIMPLIFIED function and does NOT correctly handle all poker rules. It must be REPLACED by a real evaluator.
    # ►    A TRUE hand evaluator must be able to identify all 5-card combinations (High Card, Pair, Two Pair, Three of a Kind, Straight, Flush, Full House, Four of a Kind, Straight Flush, Royal Flush) and rank them correctly, including handling kickers and ties.
    # ► Returns (hand_rank, hand_description).
    # ► Higher rank = better hand.
    if len(cards) < 2: # Une main de poker nécessite au moins 2 cartes pour le joueur + communes
        return 0, "Pas assez de cartes"
    # End if
    ranks_values = sorted([card.get_value(aces_high=True) for card in cards])                                               # ═══► Extract ranks and colors for evaluation
    suits = [card.suit for card in cards]
    rank_counts = {}                                                                                                        # ═══► Frequency counting for pairs, three of a kind, four of a kind
    for r in ranks_values:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    # End for
    suit_counts = {}                                                                                                        # ═══► Counting frequencies for colors
    for s in suits:
        suit_counts[s] = suit_counts.get(s, 0) + 1
    # End for
    num_pairs = sum(1 for count in rank_counts.values() if count == 2)                                                      # ═══► Checking pairs, three of a kind, four of a kind
    has_trips = any(count == 3 for count in rank_counts.values())
    has_quads = any(count == 4 for count in rank_counts.values())
    is_flush = any(count >= 5 for count in suit_counts.values())                                                            # ═══► Color check (Flush)
    unique_ranks_sorted = sorted(list(set(ranks_values)))
    is_straight = False                                                                                                     # ═══► Straight verification
    if len(unique_ranks_sorted) >= 5:                                                                                       # ═══► Simple check for 5-card sequences. Aces can be high or low.
        if 14 in unique_ranks_sorted and 2 in unique_ranks_sorted and 3 in unique_ranks_sorted and 4 in unique_ranks_sorted and 5 in unique_ranks_sorted:
           is_straight = True                                                                                               # ═══► Check for Straight information A-5 (Ace low)
        # End if
        for i in range(len(unique_ranks_sorted) - 4):                                                                       # ═══► Check for other suites
            if unique_ranks_sorted[i+4] - unique_ranks_sorted[i] == 4:
                is_straight = True
                break
            # End if
        # End for
    # End if
    if is_straight and is_flush:                                                                                            # ═══► Combination of hands (descending order of force)
        # ► It should be checked whether it's a Royal Flush (T,J,Q,K,A of the same color).
        # ► For this simplified case, group Straight Flush is grouped.
        return 9, "Straight Flush"                                                                                          # ═══► Rank 9: for the highest hand (Royal Flush is a Straight Flush)
    elif has_quads:
        return 8, "Four-of-a-Kind"
    elif has_trips and num_pairs >= 1:                                                                                      # ═══► Three of a kind and at least one pair
        return 7, "Full House"
    elif is_flush:
        return 6, "Flush"
    elif is_straight:
        return 5, "Straight"
    elif has_trips:
        return 4, "Three-of-a-Kind"
    elif num_pairs >= 2:
        return 3, "Two Pairs"
    elif num_pairs == 1:
        return 2, "Pair"
    else:
        high_card_rank = max(ranks_values)                                                                                  # ═══► High Card
        high_card_desc = ""
        for card in cards:
            if card.get_value() == high_card_rank:
                high_card_desc = str(card)
                break
            # End if
        # End for
        return 1, f"Carte Haute ({high_card_desc})"
    # End if
# End def
