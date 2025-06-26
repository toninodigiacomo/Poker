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
            bet_amount = amount_needed                                                                                      # ═══► For an initial bet, amount_needed is the bet amount
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
    def assign_blinds(self):
        # ► Assign small and large blinds and collect initial bets.
        active_players_in_hand = [p for p in self.players if p.chips > 0]
        if len(active_players_in_hand) < 2:
            print("Pas assez de joueurs actifs pour assigner les blinds.")
            return
        # End if
        if len(active_players_in_hand) == 2:                                                                                # ═══► For a two-player game (Heads-up): Dealer is SB, other player is BB
            dealer_player = self.players[self.dealer_index]
            other_player = [p for p in active_players_in_hand if p != dealer_player][0]                                     # ═══► Find the other active player
            sb_player = dealer_player
            bb_player = other_player
            sb_player.is_small_blind = True
            bb_player.is_big_blind   = True
#        else:                                                                                                               # ═══► For 3+ players, the normal logic
#            player_order = self.players[self.dealer_index+1:] + self.players[:self.dealer_index+1] # Ordre après le dealer
#            sb_player = None
#            bb_player = None
#            for p in player_order:                                                                                          # ═══► Find the Small Blind (first active player after the dealer)
#                if p.name == self.players[self.dealer_index].name: # Skip dealer (si il est le premier dans player_order)
#                    continue
#                if p.chips > 0:
#                    sb_player = p
#                    break
#                # End if
#            # End for
#            sb_found = False                                                                                                # ═══► Find the Big Blind (first active player after the Small Blind)
#            for p in player_order:
#                if p == sb_player:
#                    sb_found = True
#                    continue
#                if sb_found and p.chips > 0:
#                    bb_player = p
#                    break
#                # End if
#            # End for
        # End if
        if sb_player and sb_player.chips > 0:
            sb_paid = sb_player.remove_chips(self.SMALL_BLIND_VAL)
            sb_player.current_bet += sb_paid
            sb_player.bet_in_hand += sb_paid
            self.pot += sb_paid
            sb_player.is_small_blind = True
            print(f"{sb_player.name} pays the Small Blind: {sb_paid}")
        # End if
        if bb_player and bb_player.chips > 0:
            bb_paid = bb_player.remove_chips(self.BIG_BLIND_VAL)
            bb_player.current_bet += bb_paid
            bb_player.bet_in_hand += bb_paid
            self.pot += bb_paid
            self.current_highest_bet = self.BIG_BLIND_VAL
            bb_player.is_big_blind = True
            print(f"{bb_player.name} pays the Big Blind: {bb_paid}")
        # End if
        print(f"Highest bet after the blinds: {self.current_highest_bet}. Pot: {self.pot}")
    # End def
    def deal_hole_cards(self):
        # ► Distribue 2 cartes privées à chaque joueur actif."""
        for _ in range(2):                                                                                                  # ═══► 2 cards per player
            for player in self.players:
                if player.chips > 0 and not player.has_folded:                                                              # ═══► Do not distribute to eliminated/folded players
                    player.hand.append(self.deck.deal_card())
                # End if
            # End for
        # End for
        print("Private cards distributed.")
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
    def get_active_players_in_hand(self):
        # ► Returns the list of players who have not folded and who have chips.
        return [p for p in self.players if not p.has_folded and p.chips > 0]
    # End def
    def start_betting_round(self):
        # ► Prépare le jeu pour un nouveau tour de mise.
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
        active_players_in_hand = self.get_active_players_in_hand()

        if not active_players_in_hand:
            self.current_player_index = -1
            print("Aucun joueur actif pour commencer le tour de mise.")
            return
        # End if
        if self.game_state == self.GAME_STATE_PREFLOP:                                                                      # ═══► Action commence après la grosse blinde
            bb_player = next((p for p in self.players if p.is_big_blind), None)
            if bb_player:
                bb_index = self.players.index(bb_player)
                for i in range(1, len(self.players) + 1):                                                                   # ═══► Chercher le joueur après la BB
                    idx = (bb_index + i) % len(self.players)
                    if self.players[idx] in active_players_in_hand:
                        self.current_player_index = idx
                        start_player_found = True
                        break
                    # End if
                # End for
            # End if
        else:                                                                                                               # ═══► Flop, Turn, River
            dealer_idx = self.dealer_index                                                                                  # ═══► Action begins with the first active player after the dealer
            for i in range(1, len(self.players) + 1):                                                                       # ═══► Find the player after the dealer
                idx = (dealer_idx + i) % len(self.players)
                if self.players[idx] in active_players_in_hand:
                    self.current_player_index = idx
                    start_player_found = True
                    break
                # End if
            # End for
        # End if
        if not start_player_found:
            self.current_player_index = -1
            print("Impossible to find the first player to act. The betting round could be over.")
            return
        # End if
        self.last_raiser_index = self.current_player_index # Initialise le dernier relanceur au premier à agir
        print(f"Start of the '{self.game_state}' betting round. First to act Début du tour de mise: {self.players[self.current_player_index].name}")
    # End def
    def get_current_player(self):
        # ► Returns the Player object whose turn it is.
        if self.current_player_index == -1 or not self.players:
            return None
        # End if
        return self.players[self.current_player_index]
    # End def
    def get_next_player_to_act(self):
        # ► Détermine le prochain joueur qui doit agir dans le tour de mise.
        # ► Gère la rotation des joueurs et saute ceux qui ont foldé ou sont all-in.
        active_players = self.get_active_players_in_hand()
        if len(active_players) <= 1:
            return None                                                                                                     # ═══► One player left active or none, the round is over
        # End if
        initial_start_index = self.current_player_index                                                                     # ═══► To detect a complete lap
        # ► If the last player to raise is the current player, he is "done" EXCEPT if someone else raised AFTER him, which would reset last_raiser_index.
        # ► The loop stops when all active players have matched the highest bet AND action has returned to the last player to bet/raise (or to the turn initiator if no raise).
        for _ in range(len(self.players)):                                                                                  # ═══► Browse all players to the maximum
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            player = self.players[self.current_player_index]
            if player.has_folded or player.is_all_in or player.chips <= 0:
                continue                                                                                                    # ═══► This player is out of action or has no more tokens
            # End if
            if player.current_bet < self.current_highest_bet:                                                               # ═══► If the current player has to match the highest bet
                return player
            # End if
            # ► Special case: the player has matched the bet, but he is the last raiser, or he is the ‘original’ player who has the floor and the round has gone full circle.
            if player.current_bet == self.current_highest_bet:
                # ► If the action has gone to the last player who made an aggressive move, and everyone else has tied, then the turn is potentially over.
                # ► However, other players may still have a turn if it has not gone to the right person.
                pass                                                                                                        # ═══► Continue to check that the tour is completely finished
            # End if
        # End for
        return None                                                                                                         # ═══► No active player needs to act, the betting round is over
    # End def
    def is_betting_round_over(self):
        # ► Checks if the current betting round has ended.
        # ► A round is over when:
        # ►     1. Only one player remains active (the others have folded).
        # ►     2. All active players (non-folded and non-all-in) have matched the highest bet.
        # ►     3. The action is returned to the player who made the last aggressive action (bet or raise),
        # ►        OR if no one has bet, the action must have taken a full turn and everyone has checked.
        active_players = self.get_active_players_in_hand()
        # ► Case 1: Less than 2 active players
        if len(active_players) <= 1:
            print("Betting round over: less than 2 active players.")
            return True
        # End if
        # ► Case 2: All active players have matched the highest bet or are all-in
        all_bets_equalized = True
        for p in active_players:
            # ► A player is considered to have “matched” if he has bet current_highest_bet
            # ► OR if he is all-in (and therefore can no longer bet).
            if not p.is_all_in and p.current_bet < self.current_highest_bet:
                all_bets_equalized = False
                break
            # End if
        # End for
        if not all_bets_equalized:
            return False                                                                                                    # ═══► Some players still need to match the bet
        # End if
        # ► Case 3: Action reverts to the player who made the last aggressive move (bet/raise)
        # ►         OR if the current_highest_bet is 0, everyone has checked and the action has returned to the first to speak.
        first_to_act_in_round_idx = -1                                                                                      # ═══► Find the player who started the betting round (the one with the “button” or the word) at the beginning of THIS round.
        if self.game_state == self.GAME_STATE_PREFLOP:
            bb_player = next((p for p in self.players if p.is_big_blind), None)                                             # ═══► At pre-flop, the action starts with the player after the big blind
            if bb_player:
                bb_index = self.players.index(bb_player)
                for i in range(1, len(self.players) + 1):
                    idx = (bb_index + i) % len(self.players)
                    if self.players[idx] in active_players:
                        first_to_act_in_round_idx = idx
                        break
                    # End if
                # End for
            # End if
        else:                                                                                                               # ═══► Flop, Turn, River
            dealer_idx = self.dealer_index                                                                                  # ═══► Action begins with the first active player after the dealer
            for i in range(1, len(self.players) + 1):
                idx = (dealer_idx + i) % len(self.players)
                if self.players[idx] in active_players:
                    first_to_act_in_round_idx = idx
                    break
                # End if
            # End for
        # End if
        if first_to_act_in_round_idx == -1:                                                                                 # ═══► No player to start the round, already handled above
            return True
        # End if
        if self.current_highest_bet == 0:                                                                                   # ═══► If current_highest_bet is 0 (everyone has checked), the round is over if everyone has tied (at 0).
            return all_bets_equalized                                                                                       # ═══► If everyone has checked, and all bets are at 0, you're in.
        # End if

        # ► If current_highest_bet > 0, action must have returned to the last raiser.
        # ► AND all other players who acted AFTER him must have paid the bet.
        # ► This means that `current_player_index` must be the `last_raiser_index`.
        # ► AFTER all other players have had their turn and paid.
        
        # ► One way of checking this is that the player whose turn it is is the last to raise, and that he no longer has to act (he has already matched his own bet).
        # ► OR that it's a "normal" betting round and all active players have already acted, and the action has returned to the round's starting point.
        
        # ► Simulate the “next” player to see if there's anyone who still has an action waiting.
        # ► This part is tricky without a more robust action history.
        # ► Simplified: If all bets are equal, and the current player is the last raiser, the round is over.
        # ►             Or if the next player to act (according to get_next_player_to_act) is None.
        
        temp_current_player_index = self.current_player_index                                                               # ═══► Let's test whether the “next player to act” (conceptually) no longer needs to act
        for _ in range(len(self.players)):                                                                                  # ═══► Find the next player who should theoretically act, WITHOUT advancing current_player_index
            temp_current_player_index = (temp_current_player_index + 1) % len(self.players)
            p = self.players[temp_current_player_index]
            if not p.has_folded and not p.is_all_in and p.chips > 0:
                if p.current_bet < self.current_highest_bet:
                    return False                                                                                            # ═══► Someone still has to act (pay the bet)
                # End if
                if self.current_highest_bet > 0 and temp_current_player_index == self.last_raiser_index:                    # ═══► If the player has matched the bet, does the last raiser “close” the round?
                    # ► The turn came back to the last raiser, and he paid his own raise.
                    # ► All the others before him have paid. The round is over.
                    return True # Le tour de mise est terminé
                elif self.current_highest_bet > 0 and temp_current_player_index == first_to_act_in_round_idx:
                    # ► If there has been no raise since the beginning of the turn (or the last raiser), and the action has returned to the first to speak, the round is over.
                    # ► This handles the case where no one has raised and everyone has called.
                    return True
                # End if
            # End if
        # End for
        return True                                                                                                         # ═══► If the loop ends, no one needs to act
    # End def
    def collect_bets_to_pot(self):
        # ► Moves chips wagered by players to the main pot.
        for player in self.players:
            if player.current_bet > 0:
                self.pot += player.current_bet
                player.current_bet = 0                                                                                      # ═══► Reset the round bet for the next round
            # End if
        # End for
        print(f"All bets collected in the pot. Current pot: {self.pot}")
    # End def
    def determine_winner(self):
        # ► Determines the winner(s) of the hand and the description of the winning hand.
        # ► This is a MAJOR PLACEHOLDER and must be replaced by a complete poker hand evaluation algorithm (e.g. Straight Flush, Four of a Kind, etc.).
        active_players = [p for p in self.players if not p.has_folded]
        if not active_players:
            print("No active players to determine a winner (all folded or eliminated).")
            return None, "No one won (everyone folded)."
        # End if
        if len(active_players) == 1:
            winner = active_players[0]
            print(f"{winner.name} wins by default (all others have folded).")
            return [winner], f"{winner.name} wins by default!"
        # End if
        # ═══► START OF HAND EVALUATION (SIMPLIFIED PLACEHOLDER!) ◀═══ 
        # ► TODO: REPLACE THIS SECTION WITH A REAL POKER HAND EVALUATOR.
        # ►       Python libraries such as “deuces” or “poker-eval” can be useful.
        best_hand_rank = -1                                                                                                 # ═══► Use -1 to ensure that even a “High Card” wins initially
        winners = []
        winning_description = ""
        for player in active_players:
            # ► Combination of the player's 2 cards and 5 common cards (max. 7 cards)
            # ► Objective: to find the best 5-card hand among these 7.
            player_all_cards = player.hand + self.community_cards                                                           # ═══► Calling the "bogus" hand evaluator
            current_player_hand_rank, current_player_desc = get_hand_rank_and_description(player_all_cards)                 # ═══► get_hand_rank_and_description should take the player's hand + common cards
            print(f"Debug: {player.name}'s best hand: {current_player_desc} (Rank: {current_player_hand_rank})")
            if current_player_hand_rank > best_hand_rank:
                best_hand_rank = current_player_hand_rank
                winners = [player]
                winning_description = f"{player.name} wins with {current_player_desc}."
            elif current_player_hand_rank == best_hand_rank:                                                                # ═══► Handle ties (kickers, etc.). The hand evaluator should handle this
                winners.append(player)                                                                                      # ═══►PLACEHOLDER (simplified) co-winners
                winning_description += f" et {player.name} (également avec {current_player_desc})."
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




























