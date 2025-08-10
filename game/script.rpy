# ╔═════════════════════════════════════════════════════════════════════════════
# ║  Strip Poker Texas Hold'em - Ren'Py                                         ──
# ║   ► Two players: human vs. robot.
# ║   ► Each player starts each round with 100 tokens and 5 clothes
# ║   ► If a player loses a round, he removes a suit and gets back 100 tokens.
# ║   ► Standard bet management 
# ║   ►     (S. Blind, B. Blind, Check, Call, Raise, Bet, All-In)
# ║   ► Displaying maps with images/cards/02C.png ... 14S.png
# ╚═════════════════════════════════════════════════════════════════════════════
#    └────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Global variables                                                           ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
default TEXT_INFOS_MESSAGE_1    = ""
default TEXT_INFOS_MESSAGE_2    = ""
default CHEAT_POKER             = True
default DEBUG_POKER             = True

image bg poker                  = "images/PokerTable.jpg"

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Global Python classes                                                      ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
init python:
    import random

    SUITS                                        = ['C', 'D', 'H', 'S']
    RANKS                                        = [str(n).zfill(2) for n in range(2, 15)]
    CARDNAMES                                    = [r+s for r in RANKS for s in SUITS]

    # ┌───────────────────────────────┤  Class  ├───────────────────────────────┐
    # │  Class representing a Poker Texas Hold'em player                        │
    # └─────────────────────────────────────────────────────────────────────────┘
    class Player:
        # │ ┌────────────────────────────────────────────────────────────────────
        # ├─┤ Attributes:
        # │ └────────────────────────────────────────────────────────────────────
        # │  ├─► name (str)       : Player's name.
        # │  ├─► chips (int)      : Number of chips currently owned.
        # │  ├─► clothes (int)    : Number of clothes currently worn.
        # │  ├─► max_clothes (int): Maximum number of clothes (initial value).
        # │  ├─► cards (list)     : List of cards in hand (e.g. ["02C", "14S"]).
        # │  ├─► bet (int)        : Player's current bet for the current round.
        # │  ├─► folded (bool)    : Indicates whether the player has folded.
        # │  ├─► human (bool)     : Indicates whether the player is human (True) or AI (False).
        # │  └─► allin (bool)     : Indicates whether the player has gone All-In.
        # │ ┌────────────────────────────────────────────────────────────────────
        # └─┤ Methods :
        #   └────────────────────────────────────────────────────────────────────
        #    ├─► __init__(name, chips=100, clothes=5)
        #    │    └───► Initializes a player with a name, chips and clothes.
        #    ├─► reset()
        #    │    └───► Resets the player's hand for a new round, empties the cards, resets the bets and removes the state.
        #    └─► manage_clothes()
        #         └───► As long as the player doesn't have the maximum number of clothes and has > 110 chips, buys a new cloth for 100 chips.
        def __init__(self, name, chips=100, clothes=5, human=False):
            self.name                            = name
            self.chips                           = chips
            self.clothes                         = clothes
            self.max_clothes                     = clothes
            self.cards                           = []
            self.bet                             = 0
            self.folded                          = False
            self.human                           = human
            self.allin                           = False
        # End def
        def reset(self):
            self.cards                           = []
            self.bet                             = 0
            self.folded                          = False
            self.allin                           = False
        # End def
        def manage_clothes(self):
            while self.clothes < self.max_clothes and self.chips >= 110:
                self.clothes   += 1
                self.chips     -= 100
                engine.messages("You buy a cloth for 100 chips!" if self.human else f"{self.name} buys a cloth for 100 chips!", pause=2.0)
            # End while
            if self.clothes > 0 and self.chips <= 0 :
                self.clothes   -= 1
                self.chips     += 100
                engine.messages("You don't have chips anymore." if self.human else f"{self.name} doesn't have chips anymore.", "You sell a cloth for 100 chips." if self.human else f"{self.name} sells a cloth for 100 chips.", pause=2.0)
            # End if
        # End def
    # End class
    # ┌───────────────────────────────┤  Class  ├───────────────────────────────┐
    # │  Class to manages a Texas Hold'em game between two players              │
    # └─────────────────────────────────────────────────────────────────────────┘
    class PokerGame:
        # │ ┌────────────────────────────────────────────────────────────────────
        # ├─┤ Attributes:
        # │ └────────────────────────────────────────────────────────────────────
        # │  ├─► players (list[Player]) : List of two players (human and AI).
        # │  ├─► community (list[str])  : Common cards on the table.
        # │  ├─► pot (int)              : Total amount of pot.
        # │  ├─► deck (list[str])       : Deck of remaining cards.
        # │  ├─► round (int)            : Betting round number 
        # │  │                            (0=préflop, 1=flop, 2=turn, 3=river).
        # │  ├─► dealer (int)           : Dealer's index (0 or 1).
        # │  ├─► small_blind (int)      : Value of the small blind.
        # │  ├─► big_blind (int)        : Value of the big blind.
        # │  ├─► current_bettor (int)   : Index of the player to act.
        # │  ├─► last_bet (int)         : Amount of last bet.
        # │  ├─► finished (bool)        : Indicates whether the run is over.
        # │  ├─► winner (int|None)      : Round winner's index (0, 1 or None for a tie).
        # │  ├─► manche (int)           : Round counter.
        # │  ├─► betting_round_over     : Indicates whether the betting round is over.
        # │  ├─► last_to_act (int|None) : Index of the last player to act.
        # │  └─► quit (bool)            : Indicates whether the game has been exited.
        # │ ┌────────────────────────────────────────────────────────────────────
        # └─┤ Methods :
        #   └────────────────────────────────────────────────────────────────────
        #    ├─► __init__(human_name, robot_name, ...)
        #    │    └───► Initializes the game and the players.
        #    ├─► deal_community()
        #    │    └───► Distributes community cards (flop, turn, river) and resets bets.
        #    ├─► get_state()
        #    │    └───► Returns the current state of the game in dictionary form (for the UI).
        #    ├─► is_game_over()
        #    │    └───► Returns True if the game is over (one player without  clothes or quit).
        #    ├─► player_action(idx, action, amount=0)
        #    │    └───► Applies a player's action (fold, call, raise, check, allin, quit).
        #    ├─► robot_action()
        #    │    └───► Determines and returns the AI action (call, raise, fold, etc.).
        #    ├─► showdown()
        #    │    └───► Compares hands, determines winner, distributes pot and handles ties.
        #    └─► start_new_hand()
        #    │    └───► Prepare a new round (mixing, distribution, blinds...).
        def __init__(self, human_name, robot_name, small_blind=10, big_blind=20, chips=100, clothes=5, aggressiveness=0.5, max_raises_per_round=4):
            self.action_robot                    = None
            self.aggressiveness                  = aggressiveness
            self.betting_round_over              = False
            self.big_blind                       = big_blind
            self.chips                           = chips 
            self.clothes                         = clothes
            self.community                       = []
            self.current_bettor                  = 0
            self.current_raises                  = 0
            self.dealer                          = 0
            self.deck                            = []
            self.finished                        = False
            self.last_bet                        = 0
            self.last_to_act                     = None
            self.manche                          = 0
            self.max_raises_per_round            = max_raises_per_round  # Limite de raises par tour
            self.players                         = [Player(human_name, chips=chips, clothes=clothes, human=True), Player(robot_name, chips=chips, clothes=clothes, human=False)]
            self.pot                             = 0
            self.quit                            = False
            self.round                           = 0
            self.small_blind                     = small_blind
            self.winner                          = None
        # End def
        def deal_community(self):
            # ──┤ Distributes the common cards for the table and prepares the next round of bids.
            #   ├───► According to the current round :
            #   │      ├───► Round 0 → deals the flop (3 community cards).
            #   │      └───► Rounds 1 or 2 → deal an additional card (turn or river).
            #   ├───► Resets the players' bets and prepares the variables for the new round.
            #   └───► Returns the number of the new round after distribution.
            if self.round == 0:
                # ──┤ Flop : 3 cards
                self.community = [self.deck.pop() for _ in range(3)]
            elif self.round < 3:
                # ──┤ Turn or River : 1 card
                self.community.append(self.deck.pop())
            # End if
            self.round += 1                                                                                                             # ═══► Move on to the next round
            if not any(p.allin for p in self.players):
                # ──┤ If no player is All-In, reset the bets
                for p in self.players:
                    p.bet = 0                                                                                                           # ═══► Resets the bets of each player
                # End for
                self.last_bet = 0
            # End if
            self.betting_round_over = False
            self.current_bettor = (self.dealer + 1) % 2
            self.last_to_act = self.dealer
            self.current_raises = 0                                                                                                     # ═══► Resets the raises counter for each new round
            return self.round
        # End def
        def get_state(self):
            return {
                'players':                       [vars(p) for p in self.players],
                'action_robot':                  self.action_robot,
                'betting_round_over':            self.betting_round_over,
                'big_blind':                     self.big_blind,
                'community':                     self.community[:],
                'current_bettor':                self.current_bettor,
                'current_raises':                self.current_raises,
                'dealer':                        self.dealer,
                'finished':                      self.finished,
                'last_bet':                      self.last_bet,
                'last_to_act':                   self.last_to_act,
                'manche':                        self.manche,
                'pot':                           self.pot,
                'quit':                          self.quit,
                'round':                         self.round,
                'small_blind':                   self.small_blind,
                'winner':                        self.winner
            }
        # End def
        def is_game_over(self):
            # ──┤ Checks if the game is over.
            #   ├───► There are two possible conditions for stopping the game:
            #   │      ├───► (1) One of the players has no clothes left (clothes == 0)
            #   │      └───► (2) The "quit" flag is set to True.
            #   └───► Retourne True si le jeu est fini, sinon False.
            return any(p.clothes == 0 and p.chips == 0 for p in self.players) or self.quit
        # End def
        def messages(self, principal_message="", secondary_message="", pause=1.0):
            # ──┤ Displays messages to the players.
            #   ├───► Parameters :
            #   │      ├───► "principal_message" : main message to display.
            #   │      ├───► "secondary_message" : secondary message to display (optional).
            #   │      └───► "pause" : duration of the pause before displaying the next message (default 1.0 seconds).
            #   └───► Updates the global variables TEXT_INFOS_MESSAGE_1 and TEXT_INFOS_MESSAGE_2 with the messages to display.
            global TEXT_INFOS_MESSAGE_1, TEXT_INFOS_MESSAGE_2
            #renpy.say(None, "DEBUG ├───► " + principal_message)
            #renpy.say(None, "DEBUG ├───► " + secondary_message)
            TEXT_INFOS_MESSAGE_1 = principal_message
            TEXT_INFOS_MESSAGE_2 = secondary_message
            renpy.pause(pause)
        # End def
        def player_action(self, idx, action, amount=0):
            # ──┤ Manages a player's action (`idx`) during a betting round.
            #   ├───► Parameters :
            #   │      ├───► "idx" : player index (0 or 1)
            #   │      ├───► "action" : action choosen ('quit', 'fold', 'call', 'bet', 'raise', 'check', 'allin')
            #   │      └───► "amount" : amount associated with the action (optional, default 0)
            #   └───► Updates the status of the game, the players, the pot, and displays messages.
            p   = self.players[idx]                                                                                                     # ═══► Get the player object based on the index
            opp = self.players[1-idx]                                                                                                   # ═══► Get the opponent player object based on the index
            if action == 'quit':                                                                                                        # ═══► If the player chooses to quit the game
                self.quit                        = True
                self.finished                    = True
                self.betting_round_over          = True
                return
            # End if
            if action == 'fold':                                                                                                        # ═══► Player folds. Opponent wins the pot
                self.finished                    = True
                self.betting_round_over          = True
                p.folded                         = True
                self.winner                      = 1 - idx
                self.players[self.winner].chips += self.pot
                self.messages(f"You fold." if idx == 0 else f"{p.name} folds.", f"{self.players[self.winner].name} wins the pot of {self.pot} chips." if idx == 0 else f"You win the pot of {self.pot} chips.", pause=2.0)
                self.community                   = []
                self.pot                         = 0
                p.manage_clothes()                                                                                                      # ═══► Check if the player needs to buy or sell clothes based on their chips
                p.reset()                                                                                                               # ═══► Reset the player's state
                opp.reset()                                                                                                             # ═══► Reset the opponent's state
                return
            elif action == 'check':                                                                                                     # ═══► The player checks (if possible)
                self. messages("You check." if idx == 0 else f"{p.name} checks.", "", pause=2.0 if idx == 0 else 0.0)
                if self.last_to_act == idx:                                                                                             # ═══► If the player who checks is the last to act, the betting round is over.
                    self.betting_round_over = True
                else:
                    self.current_bettor = 1 - idx
                # End if
            elif action == 'call':                                                                                                      # ═══► The player follows the current bet           
                to_call                          = self.last_bet - p.bet
                p.chips                         -= to_call
                p.bet                           += to_call
                self.pot                        += to_call
                self.messages("You are following." if idx == 0 else f"{p.name} follows.", f"The raise is {to_call} chips.", pause=2.0 if idx == 0 else 0.0)
                if self.last_to_act == idx or opp.allin == True:                                                                        # ═══► If the player who call is the last to act, the betting round is over.
                    self.betting_round_over = True
                    if opp.allin == True:
                        p.allin = True
                    # End if
                else:
                    self.current_bettor = 1 - idx
                # End if
            elif action == 'bet':                                                                                                       # ═══► The player makes a bet
                amount                           = self.big_blind
                p.chips                         -= amount
                p.bet                           += amount
                self.pot                        += amount
                self.last_bet                    = p.bet
                self.last_to_act                 = idx
                self.current_bettor              = 1 - idx                                                                              # ═══► Hands over to the other player
                self.current_raises             += 1
                self.messages("You bet." if idx == 0 else f"{p.name} bets.", f"The raise is {amount} chips.", pause=2.0 if idx == 0 else 0.0)
            elif action == 'raise':                                                                                                     # ═══► The player raises the bet
                amount                           = self.big_blind
                to_call                          = self.last_bet - p.bet
                total                            = to_call + amount
                p.chips                         -= total
                p.bet                           += total
                self.pot                        += total
                self.last_bet                    = p.bet
                self.last_to_act                 = idx
                self.current_bettor              = 1 - idx
                self.current_raises             += 1
                self.messages("You raise." if idx == 0 else f"{p.name} raises.", f"The raise is {total} chips.", pause=2.0 if idx == 0 else 0.0)
            elif action == 'allin':                                                                                                     # ═══► The player goes All-In (bets all his remaining chips)
                # ──┤ The player goes All-In (bets all his remaining chips)
                #   ├───► Calculates how much it must pay to follow (`to_call`)
                #   ├───► If he doesn't have enough, he stakes everything he has.
                #   └───► Update:
                #          ├───► His bet (`bet`), the pot, his remaining chips (0), the last bet (`last_bet`), etc.
                #          └───► Marks the player as All-In.
                to_call                          = self.last_bet - p.bet
                total                            = p.chips
                if to_call > total:                                                                                                     # ═══► If the player cannot follow through completely, he bets everything he has
                    to_call = total
                # End if
                p.bet                           += total
                self.pot                        += total
                p.chips                          = 0
                self.last_bet                    = max(self.last_bet, p.bet)
                self.last_to_act                 = idx
                p.allin                          = True
                self.messages("You go all-in." if idx == 0 else f"{p.name} goes all-in.", f"The bet is {total} chips", pause=2.0)
                # Correction ici :
                if opp.allin or opp.folded:                                                                                             # ═══► If the player who checks is the last to act, the betting round is over.
                #if self.last_to_act == idx:                                                                                             # ═══► If the player who checks is the last to act, the betting round is over.
                    self.betting_round_over = True
                else:
                    self.current_bettor = 1 - idx
                # End if
            # End if
            p.manage_clothes()                                                                                                          # ═══► Check if the player needs to buy or sell clothes based on their chips
        # End def
        def robot_action(self):
            # ──┤ Determines and executes the robot's action during a betting round.
            #   ├───► The decision depends on :  
            #   │       ├───► its condition (chips, clothes),
            #   │       ├───► the current situation (follow-up, dunning history),
            #   │       └───► its aggressiveness.
            #   └───► Key steps in the decision-making process :
            #         1. If no more chips but still clothes → exchange one garment for 100 chips.
            #         2. If already folded → return “fold” immediately.
            #         3. Otherwise → builds a list of possible actions with weights and chooses an action randomly.
            robot = self.players[1]
            # ──┤ If already folded, returns “fold”.
            if robot.folded:
                return 'fold', 0
            # End if
            # ──┤ If not, calculate how much you have to pay to follow.
            to_call = self.last_bet - robot.bet
            actions = []
            # ──┤ Determines possible actions depending on the situation
            if to_call > 0:
                if self.players[0].allin:
                    actions =   [
                                ('call',  to_call)
                                ]
                elif robot.chips <= to_call and robot.clothes == 0:                                                                     # ═══► Doesn't have enough to follow AND out of clothes → Can go All-In, or Fold
                    actions =   [
                                ('allin', robot.chips), 
                                ('fold',  0)
                                ]
                elif robot.chips <= 40 and robot.clothes == 0:                                                                          # ═══► Has 20 or less left and no clothes → Forced All-In without option
                    actions =   [
                                ('allin', robot.chips)
                                ]
                elif robot.chips > to_call + self.big_blind:                                                                            # ═══► More than enough to follow + relaunch
                    actions =   [
                                ('call',  to_call), 
                                ('raise', self.big_blind), 
                                ('fold',  0)
                                ]
                elif robot.chips > to_call:                                                                                             # ═══► Enough to follow
                    actions =   [
                                ('call',  to_call), 
                                ('fold',  0)
                                ]
                else:
                    actions =   [
                                ('fold', 0)
                                ]
                # End if
            else:                                                                                                                       # ═══► No bet in progress, can “check” (stay without betting) or bet voluntarily
                if robot.chips <= 40 and robot.clothes == 0:                                                                            # ═══► Very few chips and no more clothes → Has to bet everything
                    actions =   [
                                ('allin', robot.chips)
                                ]
                elif robot.chips >= self.big_blind:                                                                                     # ═══► Can choose to check or bet the big blind.
                    actions =   [
                                ('check', 0), 
                                ('bet',   self.big_blind)
                                ]
                else:                                                                                                                   # ═══► Nothing to bet on
                    actions =   [
                                ('check', 0)
                                ]
                # End if
            # End if
            if not actions:
                return 'check', 0
            if ('check', 0) in actions:                                                                                                 # ═══► Should not fold if it can check for free
                actions = [a for a in actions if a[0] != 'fold']
            # End if
            if to_call > 0:                                                                                                             # ═══► Must never be able to check if it has to follow a bet
                actions = [a for a in actions if a[0] != 'check']
            # End if
            weights = []                                                                                                                # ═══► List of weights for each action
            # ──┤ Weighting according to aggressiveness
            #   └───► Selects an action based on possible actions, game state and AI aggression. 
            #         Returns a randomly chosen action, weighted by calculated weights.
            #          ├───► actions: liste de tuples (action:str, amount:int), ex : [((“raise”, 20), (“call”, 10), (“fold”, 0)]
            #          ├───► engine: object with current_raises and max_raises_per_round
            #          ├───► aggressiveness: float between 0 and 1
            #          └───► :return: tuple (action:str, amount:int)
            for action, amount in actions:                                                                                              # ═══► Evaluate each action and assign it a weighting
                if action in ('raise', 'bet'):
                    if engine.current_raises < engine.max_raises_per_round:                                                             # ═══► If we can still "Raise" or "Bet", we need to balance it with aggression
                        weights.append(self.aggressiveness)
                    else:
                        weights.append(0)
                    # End if
                elif action in ('call', 'check'):                                                                                       # ═══► If the maximum number of retries is reached, very low weight
                    weights.append(1 - self.aggressiveness)                                                                             # ═══► These actions are more attractive to a prudent AI
                elif action == 'allin':
                    # ──┤ If all-in is the only way to stay in the game (already considered above):
                    #   ├───► we shouldn't get here with other viable actions;
                    #   └───► we can give a slightly higher weight than ‘fold’ but less than a normal ‘raise’.
                    weights.append(0.5 * self.aggressiveness + 0.1)                                                                     # ═══► To adapt
                else:
                    weights.append(0.2)                                                                                                 # ═══► If the action is 'fold', we give it a small weight to keep the AI prudent
                # End if
            total = sum(weights)                                                                                                        # ═══► Normalising weights to form a valid distribution
            if total > 0:
                weights = [w / total for w in weights]                                                                                  # ═══► If the total is not zero, we standardise the probability
            else:
                weights = [1 / len(actions)] * len(actions)                                                                             # ═══► If the total is zero (highly unlikely), we standardise the probability
            # End if
            self.action_robot = random.choices(actions, weights=weights, k=1)[0]                                                        # ═══► Select an action at random, taking into account the weights
            return self.action_robot
        # End def
        def showdown(self):
            hand_names = {
                8: "Straight flush",
                7: "Four of a kind",
                6: "Full house",
                5: "Flush",
                4: "Straight",
                3: "Three of a kind",
                2: "Two pair",
                1: "One pair",
                0: "High card"
            }
            def card_value(card):                                                                                                       # ═══► Internal function: numerical value of a card ("02C" -> 02)
                return int(card[:2])
            # End def
            def card_suit(card):                                                                                                        # ═══► Internal function: card color (suit) ("02C" -> "C")
                return card[2]
            # End def
            def hand_rank(cards):
                # ──┤ Evaluate the best poker hand in the given list of 7 cards.
                #   ├───► Returns a tuple indicating the rank of the hand and relevant tie-breakers.
                #   │      Examples:
                #   │         (8, high_card, …)  → Straight Flush
                #   │         (7, quad_value, …) → Four of a Kind
                #   │         …
                #   └───► Higher tuple values mean stronger hands.
                values = sorted([card_value(c) for c in cards], reverse=True)                                                           # ═══► Extract numeric values of cards, sorted descending
                suits  = [card_suit(c) for c in cards]                                                                                  # ═══► Extract suits of all cards
                counts = {v: values.count(v) for v in set(values)}                                                                      # ═══► Identify pairs, trips (three of a kind), and quads (four of a kind)
                pairs  = [v for v, c in counts.items() if c == 2]
                trips  = [v for v, c in counts.items() if c == 3]
                quads  = [v for v, c in counts.items() if c == 4]
                flush  = None
                for s in set(suits):                                                                                                    # ═══► Check for flush (5 or more cards of the same suit)
                    if suits.count(s) >= 5:
                        flush = s
                        break
                    # End if
                # End for        
                uniq = sorted(set(values), reverse=True)                                                                                # ═══► Create a sorted list of unique card values (for straights).
                if 14 in uniq:
                    uniq.append(1)
                # End if
                straight = None                                                                                                         # ═══► Check for straight (5 consecutive values
                for i in range(len(uniq) - 4):
                    if uniq[i] - uniq[i + 4] == 4:
                        straight = uniq[i]
                        break
                    # End if
                # End for        
                straight_flush = None                                                                                                   # ═══► Check for straight flush
                if flush:
                    flush_cards = [card_value(c) for c in cards if card_suit(c) == flush]
                    flush_uniq = sorted(set(flush_cards), reverse=True)
                    if 14 in flush_uniq:
                        flush_uniq.append(1)
                    # End if
                    for i in range(len(flush_uniq) - 4):
                        if flush_uniq[i] - flush_uniq[i + 4] == 4:
                            straight_flush = flush_uniq[i]
                            break
                        # End if
                    # End for
                # End if
                # ──┤ Determine best hand and return corresponding tuple.
                if straight_flush:                                                                                                      # ═══► Straight flush
                    return (8, straight_flush, values)
                if quads:                                                                                                               # ═══► Four of a kind
                    return (7, max(quads), values)
                if trips and pairs:                                                                                                     # ═══► Full house
                    return (6, max(trips), max(pairs), values)
                if flush:                                                                                                               # ═══► Flush
                    flush_cards = [card_value(c) for c in cards if card_suit(c) == flush]
                    return (5, sorted(flush_cards, reverse=True))
                if straight:                                                                                                            # ═══► Straight
                    return (4, straight, values)
                if trips:                                                                                                               # ═══► Three of a kind
                    return (3, max(trips), values)
                if len(pairs) >= 2:                                                                                                     # ═══► Two pair
                    return (2, max(pairs), min(pairs), values)
                if pairs:                                                                                                               # ═══► One pair
                    return (1, max(pairs), values)
                return (0, values)                                                                                                      # ═══► High card
            # End def
            def rank_to_str(rank):                                                                                                      # ═══► Convert rank value to understandable string
                return hand_names[rank[0]]
            # End def
            def distribute_pot(winner):
                # ──┤ Distributes the pot at the end of the round according to the winner and bets.
                #   └───► Handles different scenarios:
                #          ├───► Takes into account equal and unequal bets, and ties.
                #          └───► If winner is None → tie.
                p1, p2 = self.players                                                                                                   # ═══► Retrieve players
                bet1, bet2 = p1.bet, p2.bet                                                                                             # ═══► Retrieve their respective bets
                # ──┤ Determine the smallest of the two players' bets for this round.
                #   ├───► bet1 and bet2 are the amounts that player 1 and player 2 wagered in this hand.
                #   ├───► This is used to identify the *minimum common bet*, which is the amount both players have "matched".
                #   ├───► The excess (the difference between the largest and the smallest bet) belongs to the player who bet more,
                #   │      unless special rules apply depending on the winner.
                #   └───► Example:
                #          │ bet1 = 50
                #          │ bet2 = 80
                #          │ ⇒ min_bet = 50 (the smallest amount among both bets)
                min_bet = min(bet1, bet2)
                max_bet = max(bet1, bet2)
                diff = max_bet - min_bet                                                                                                # ═══► Compute difference between highest and lowest bet
                pot_before = self.pot
                total_distributed = 0
                # ──┤ Case 1: Unequal bets
                if bet1 != bet2:
                    # ──┤ Case 1.1: Player with higher bet wins → wins entire pot.
                    if (bet1 > bet2 and winner == 0) or (bet2 > bet1 and winner == 1):
                        winner_player = self.players[winner]
                        winner_player.chips += self.pot
                        renpy.say(None, f"{'You win' if winner == 0 else (p2.name + 'wins')} the whole pot ({self.pot} chips)!")
                        winner_player.manage_clothes()
                    # ──┤ Case 1.2: Player with lower bet wins → gets min_bet*2, loser keeps the difference.
                    elif (bet1 > bet2 and winner == 1) or (bet2 > bet1 and winner == 0):
                        loser = self.players[winner ^ 1]
                        winner_player = self.players[winner]                                                                            # ═══► Calculation of the winner's total winnings
                        winner_gain = self.pot + (bet1 if winner == 1 else bet2)
                        loser_gain = (bet2 - bet1) if winner == 1 else (bet2 - bet1)
                        winner_player.chips += winner_gain
                        loser.chips += loser_gain
                        renpy.say(None, f"{'You win' if winner == 0 else (p2.name + 'wins')} {2*min_bet} chips, and {p2.name if winner == 0 else 'you'} get the difference ({diff} chips)..")
                    # ──┤ Case 1.3: Tie (bets unequal) → each recovers min_bet + surplus goes to the one who bet more.
                    else:
                        p1.chips += min_bet + (diff if bet1 > bet2 else 0)
                        p2.chips += min_bet + (diff if bet2 > bet1 else 0)
                        renpy.say(None, f"Equality: everyone gets their bets back ({min_bet}) and the difference ({diff}) goes to the one who bet more.")
                    # End if
                # ──┤ Case 2: Equal bets
                else:
                    # ──┤ Case 2.1: Perfect tie → pot split equally.
                    if winner is None:
                        p1.chips += self.pot // 2
                        p2.chips += self.pot // 2
                        renpy.say(None, f"Equality: everyone gets theirs {self.pot // 2} chips back.")
                    # ──┤ Case 2.2: Someone wins → takes entire pot.
                    else:
                        winner_player = self.players[winner]
                        winner_player.chips += self.pot
                        renpy.say(None, f"{'You win, you' if winner == 0 else (p2.name + ' wins and get')} the pot ({self.pot} chips)!")
                        winner_player.manage_clothes()
                    # End if
                # End if
            # End def
            p1, p2 = self.players                                                                                                       # ═══► Unpack the two players from the `self.players` list into p1 (human) and p2 (robot)
            cards1 = p1.cards + self.community                                                                                          # ═══► Combine each player’s private cards with the community cards
            cards2 = p2.cards + self.community
            # ──┤ Determine the winner of the current poker hand.
            #   ├───► Compares both players’ hands using `hand_rank`.
            #   ├───► Announces the result and updates chips, clothes and pot accordingly.
            #   └───► Handles end-of-round state and resets bets.
            rank1 = hand_rank(cards1)                                                                                                   # ═══► Evaluate each player’s hand strength using the `hand_rank()` function
            rank2 = hand_rank(cards2)
        
            renpy.say(None, f"Your hand: {p1.cards} | {p2.name} hand: {p2.cards}")
            renpy.say(None, f"Common cards: {self.community}")
            renpy.say(None, f"Your hand: {rank_to_str(rank1)} | {p2.name} hand: {rank_to_str(rank2)}")
        
            if rank1 > rank2:
                winner = 0
                renpy.say(None, "You win!")
            elif rank2 > rank1:
                winner = 1
                renpy.say(None, f"{p2.name} win!")
            else:
                winner = None
                renpy.say(None, "Perfect tie!")
            #End if
            self.finished           = True
            self.betting_round_over = True
            self.winner             = winner
            distribute_pot(winner)                                                                                                      # ═══► Distribute the pot
            self.pot                = 0                                                                                                 # ═══► Reset the pot
        # End def
        def start_new_hand(self):
            self.messages("", "", pause=0.25)
            self.manche += 1
            self.deck = CARDNAMES[:]
            random.shuffle(self.deck)
            for p in self.players:
                p.reset()
                try:
                    p.cards = [self.deck.pop(), self.deck.pop()]
                except IndexError:
                    self.finished                     = True
                    self.winner                       = None
                    return
                # End try
            # End for
            self.community                            = []
            self.pot                                  = 0
            self.round                                = 0                                                                               # ═══► Reset the round to 0 (pre-flop)
            self.finished                             = False
            self.winner                               = None
            self.dealer                               = 1 - self.dealer                                                                 # ═══► Changing the dealer (button) for the new round
            self.current_raises                       = 0                                                                               # ═══► Reset the number of raises for the new round
            self.messages(f"Round {self.manche} starts!", f"You are the dealer. It's {self.players[1 - self.dealer].name} turn." if self.dealer == 0 else f"{self.players[self.dealer].name} is the dealer. It's your turn.", pause=2.0 if self.dealer == 0 else 0.0)
            # ─┤ Determining who starts talking pre-flop
            #  ├───►In a 2-player game:
            #  ├───► Dealer (SB) speaks second
            #  └───► Non-dealer (BB) speaks first
            self.current_bettor                       = (self.dealer + 1) % 2                                                           # ═══► Changing the dealer (button) for the new sleeve
            self.last_bet                             = self.big_blind
            # ► Blinds
            self.players[self.dealer].chips          -= self.small_blind                                                                # ═══►  The player with the dealer button places the Small Blind
            self.players[self.dealer].bet             = self.small_blind
            self.players[(self.dealer+1)%2].chips    -= self.big_blind                                                                  # ═══►  The player to the left of the dealer places the Big Blind
            self.players[(self.dealer+1)%2].bet       = self.big_blind
            self.pot                                  = self.small_blind + self.big_blind
            self.betting_round_over                   = False                                                                           # ═══►  The betting round is not over
            self.last_to_act                          = self.dealer                                                                     # ═══►  The last player to act is the dealer
            # ──┤  At this stage :
            #   ├───► blinds have been bet
            #   ├───► dealer has changed
            #   ├───► round is reset to 0
            #   └───► the right player is ready to talk
        # End def
    # End class
    # ┌──────────────────────────────┤  Function  ├─────────────────────────────┐
    # │  Function for obtaining player and game status                          │
    # └─────────────────────────────────────────────────────────────────────────┘
    def get_player_state(engine):
        # ──┤ Retrieves the current status of both players and the game.
        #   ├───► Calls "engine.get_state()" to get the global state of the game.
        #   ├───► Extracts the two players from the "state[players]" list.
        #   └───► Returns a tuple (player 1, player 2, complete state).
        state = engine.get_state()                                                                                                      # ═══► Get the current state of the game
        p1 = state['players'][0]
        p2 = state['players'][1]
        return p1, p2, state
    # End def
    # ┌──────────────────────────────┤  Function  ├─────────────────────────────┐
    # │  Function for displaying cards images                                   │
    # └─────────────────────────────────────────────────────────────────────────┘
    def get_card_image(card):
        # ──┤ Returns the path to the image corresponding to a given map.
        #   ├───► Takes `card` as a parameter (for example: ‘14S’, “10H”, ‘13D’, ...).
        #   └───► Builds and returns the path string to the PNG image of the map.
        return f"images/cards/{card}.png"
    # End def
# End init python

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Global Labels                                                              ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
label start:
    python:
        engine = PokerGame("Vous", "Robot", small_blind=10, big_blind=20, chips=100, clothes=1, aggressiveness=0.4, max_raises_per_round=2)
        #engine = PokerGame("Vous", "Robot", small_blind=10, big_blind=20, chips=100, clothes=5, aggressiveness=0.4, max_raises_per_round=4)
    jump LB_GAME_POKER
# End label
label LB_GAME_POKER:
    # └───► Initializes a new poker round: 
    #   └───► It increments the round counter. 
    #   └───► It prepares the distribution of the cards and blinds.
    #   └───► Then it displays the state of play on the screen.
    #   └───► It then transfers control to the betting_round label to manage the betting round.
    #   └───► This is the main entry point for each new hand in the betting loop.
    scene bg poker
    $ new_game = True
    show screen SC_POKER_ACTION(engine, new_game=True)                                                                                  # ═══► Displays the screen for choosing: New game or Quit
    while new_game:

        scene bg poker

        $ result = ui.interact()
        if result == "quit":
            return
        # End if
        if result == "new_game":
            $ new_game = False                                                                                                          # ═══► Exit loop
        # End if
    # End while
    python:
        engine.start_new_hand()                                                                                                         # ═══► Starts a new hand by resetting the game state and dealing cards
    # End python
    show screen SC_POKER_STATUS(engine, reveal_ai=False)                                                                                # ═══► Displays the current state of the game (without revealing AI cards)
    show screen SC_POKER_ACTION(engine, new_game=False)                                                                                 # ═══► Displays the action screen for the player
    jump LB_BETTING_ROUND                                                                                                               # ═══► Jumps to the betting round label to manage the betting process
# End label
label LB_BETTING_ROUND:
    # ──┤ Manages a betting round in the poker game.
    #   ├───► Retrieves the current state of the game and players.
    #   │      ├───► If the round is over, displays the winner or a tie, strips the loser and returns to `LB_GAME_POKER`.
    #   │      ├───► If the betting round is over but not the round:
    #   │      │      ├───► Deal the community cards (Flop, Turn, River).
    #   │      │      └───► Or starts the showdown if all cards are dealt.
    #   │      ├──► If it is the human player's turn:
    #   │      │      └───► Displays the action screen and calls `LB_PLAYER_ACTION`.
    #   │      └───► If it's the AI's turn to play:
    #   │             ├───► The AI chooses an action and performs it.
    #   │             └───► Updates messages and turn status.
    #   └──► Loops back to `LB_BETTING_ROUND` until end of round.
    python:
        state        = engine.get_state()
        finished     = state['finished']
        betting_over = state['betting_round_over']
        round_num    = state['round']
        p1, p2, _    = get_player_state(engine)
        player_turn = engine.current_bettor == 0                                                                                        # ═══► Determines who plays now
    # End python
    if finished:                                                                                                                        # ═══► If the round is finished, display the winner or a tie
        if state['winner'] is not None:                                                                                                 # ═══► If there is a winner, display the winner's name and the result
            $ winner_name = state['players'][state['winner']]['name']
            $ loser_name  = state['players'][1 - state['winner']]['name']
            $ engine.messages("You win." if state['winner'] == 0 else f"{winner_name} wins.", "You loose." if state['winner'] == 1 else f"{engine.players[1].name} looses.", pause=1.0)
        else:
            $ engine.messages("Equality!", "", pause=1.0)
        # End if
        hide screen SC_POKER_ACTION
        if engine.is_game_over():
            jump LB_GAME_OVER
        # End if
        jump LB_GAME_POKER
    # End if
    if betting_over or (p1['allin'] and p2['allin']):                                                                                   # ═══► If the betting round is over but the round is not finished, deal community cards or start showdown
        if round_num < 3:                                                                                                               # ═══► If the round is not finished, deal community cards
            python:
                result = engine.deal_community()
                if result == 1:                                                                                                         # ═══► FLOP
                    engine.messages("Flop! 3 common cards are dealt.", "It's your turn to play!" if engine.current_bettor == 0 else f"It's {engine.players[1].name}'s turn to play!", pause=0.0 if engine.current_bettor == 0 else 3.0)                                                     # ═══► Display the message for the flop
                elif result == 2:                                                                                                       # ═══► TURN
                    engine.messages("Turn! 1 common card is dealt.", "It's your turn to play!" if engine.current_bettor == 0 else f"It's {engine.players[1].name}'s turn to play!", pause=0.0 if engine.current_bettor == 0 else 3.0)                                                     # ═══► Display the message for the flop
                elif result == 3:                                                                                                       # ═══► RIVER
                    engine.messages("River! 1 common card is dealt.", "It's your turn to play!" if engine.current_bettor == 0 else f"It's {engine.players[1].name}'s turn to play!", pause=0.0 if engine.current_bettor == 0 else 3.0)                                                     # ═══► Display the message for the flop
                # End if
            # End python
            jump LB_BETTING_ROUND
        else:                                                                                                                           # ═══► If all the cards are dealt, the showdown begins
            python:
                engine.showdown()
            # End python
            $ TEXT_INFOS_MESSAGE_1 = "Showdown..."
            $ TEXT_INFOS_MESSAGE_2 = "The cards are revealed."
            hide screen SC_POKER_ACTION
            show screen SC_POKER_STATUS(engine, reveal_ai=True)
            jump LB_BETTING_ROUND
        # End if
    # End if
    if player_turn and not engine.players[0].folded:                                                                                    # ═══► If it's the Human's turn and Human haven't folded, display action buttons
        show screen SC_POKER_ACTION(engine, new_game=False)                                                                             # ═══► Displays the player's action screen
        call LB_PLAYER_ACTION
        jump LB_BETTING_ROUND
    elif not engine.players[1].folded:                                                                                                  # ═══► Otherwise, it's up to the Robot
        hide screen SC_POKER_ACTION
        python:
            action, amount = engine.robot_action()                                                                                      # ═══► "engine.robot_action()" method is called. It returns two values : "action" and "amount"
            engine.player_action(1, action, amount)
            renpy.restart_interaction()
        # End python
        jump LB_BETTING_ROUND
    # End if
# End label
label LB_PLAYER_ACTION:                                                                                                                 # ═══► Displays the action screen and waits for the player's choice
    $ action_tuple = ui.interact()
    $ action = action_tuple[0]
    python:
        engine.player_action(0, action)
    # End python
    if action   == "fold":
        pass
    elif action == "call":
        pass
    elif action == "raise":
        pass
    elif action == "check":
        pass
    elif action == "bet":
        pass
    elif action == "allin":
        pass
    elif action == "quit":
        python:
            engine.messages("You're leaving the game.")
        # End python
    # End if
    show screen SC_POKER_STATUS(engine, reveal_ai=False)
    hide screen SC_POKER_ACTION
    $ renpy.pause(1.0)
    return
# End label
label LB_GAME_OVER:
    # └───► Displays an end-of-game screen with the message "Game over!":
    #   └───► Then offers the player the option of playing a new game or quitting.
    #   └───► It therefore manages the conclusion of the game and the choice of restarting or quitting.
    scene bg poker
    show text "Game over!" at truecenter with dissolve
    $ renpy.pause(1.0)
    menu:
        "Play a game again?"
        "Yes":
            jump start
        "No":
            $ renpy.quit()
    # End menu
# End label

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Global Screens                                                             ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
screen SC_POKER_STATUS(engine, reveal_ai=False):
    $ p1, p2, state = get_player_state(engine)
    # ┌────────────────────────┤      MAIN FRAME      ├─────────────────────────┐
    frame:
        background "#404040a0"
        xalign 1.0
        yalign 0.5
        xsize 0.22
        ysize 1.0
    # End frame
    # ┌────────────────────────┤   BACKGROUNE FRAME    ├────────────────────────┐
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.8
        xsize 0.21
        ysize 0.2
    # End frame
    # ┌────────────────────────┤  HUMAN'S INFORMATION  ├────────────────────────┐
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.8
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}Your chips: [p1['chips']]    [p1['clothes']] clothes{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for c in p1['cards']:
                        add get_card_image(c) size (188, 251)
                    # End for
                # End hbox
            # End grid
        # End vbox
    # End frame
    if not state['finished']:                                                                                                           # ═══► If the game is not finished, display the player's bet
        frame:
            background "#00000000"
            xalign 1.0
            yalign 0.905
            xsize 0.21
            ysize   0.04
            hbox:
                text "{b}Current bet: {color=#FF6600}[p1['bet']]{/color}{/b}" size 26 color "#FFFFFF"
            # End hbox
        # End frame
    # End if
    # ┌────────────────────────┤  ROBOT'S INFORMATION  ├────────────────────────┐
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.1
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}[p2['name']] chips: [p2['chips']]    [p2['clothes']] clothes{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    if CHEAT_POKER:
                        for c in p2['cards']:
                            add get_card_image(c) size (188, 251)
                            add "images/cards/back1.png" size (188, 251) alpha 0.5 xpos -30
                    else:
                        for c in (p2['cards'] if reveal_ai else ["back1", "back1"]):
                            if c == "back":
                                add "images/cards/back.png" size (188, 251)
                            else:
                                add get_card_image(c) size (188, 251)
                            # End if
                        # End for
                    # End if
                # End hbox
            # End grid
        # End vbox
    # End frame
    if not state['finished']:                                                                                                           # ═══► If the game is not finished, display the robot's bet
        frame:
            background "#00000000"
            xalign 1.0
            yalign 0.32
            xsize 0.21
            ysize   0.04
            hbox:
                text "{b}Current bet: {color=#FF6600}[p2['bet']]{/color}{/b}" size 26 color "#FFFFFF"
            # End hbox
        # End frame
    # End if
    # ┌────────────────────────┤     DEALER BUTTON     ├────────────────────────┐
    frame:
        if engine.dealer == 0:                                                                                                          # ═══► Display the dealer icon based on the current dealer
            background "#40404000"
            xalign 1.0
            yalign 0.85
            xsize 0.08
            ysize 0.2
            vbox:
                add "Dealer.png" size (100, 100)
            # End vbox
        else:
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
    # ┌────────────────────────┤          POT          ├────────────────────────┐
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: {color=#00FF00}[state['pot']]{/color}{/b}   (round: [state['manche']])" size 26 color "#FFFFFF"
        # End hbox
    # End frame
    # ┌────────────────────────┤    COMMUNITY CARDS    ├────────────────────────┐
    frame:
        background "#40404000"
        xalign 0.997
        yalign 0.5
        xsize 0.21
        ysize 0.185
        hbox spacing -120:
            for c in state['community']:
                add get_card_image(c) xsize 160 ysize 220
            # End for
        # End hbox
    # End frame
    # ┌────────────────────────┤   INFORMATION FRAME   ├────────────────────────┐
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.005
        xsize 0.21
        ysize 0.07
        vbox:
            grid 1 2:
                hbox:
                    text "[TEXT_INFOS_MESSAGE_1]" size 22 color "#FFFFFF"
                # End hbox
                hbox:
                    text "[TEXT_INFOS_MESSAGE_2]" size 22 color "#FFFFFF"
                # End hbox
            # End grid
        # End vbox
    # End frame
    # ┌────────────────────────┤      DEBUG FRAME      ├────────────────────────┐
    frame:
        xalign 0.0
        yalign 1.0
        xsize 670
        ysize 480
        background "#2228"
        padding (20, 10)
        vbox:
            if DEBUG_POKER:
                text "Round: [state['manche']]" size 22 color "#FFFFFF"
                text "Actual turn: [state['round']]" size 22 color "#FFFFFF"
                text "Blinds: [state.get('small_blind', 'N/A')] / [state.get('big_blind', 'N/A')]" size 22 color "#FFFFFF"
                text "Player 1: [p1['name']] - Clothes: [p1['clothes']] - Chips: [p1['chips']] - Bet: [p1['bet']]" size 22 color "#FFFFFF"
                text "Player 2: [p2['name']] - Clothes: [p2['clothes']] - Chips: [p2['chips']] - Bet: [p2['bet']]" size 22 color "#FFFFFF"
                text "Dealer: [state['dealer']]" size 22 color "#FFFFFF"
                text "Pot: [state['pot']]" size 22 color "#FFFFFF"
                text "Player 1 Cards: [p1['cards']]" size 22 color "#FFFFFF"
                if reveal_ai:
                    text "Player 2 Cards: [p2['cards']]" size 22 color "#FFFFFF"
                else:
                    text "Player 2 Cards: [p2['cards']] (hidden)" size 22 color "#FFFFFF"
                text "Community Cards: [state['community']]" size 22 color "#FFFFFF"
                text "Player 2 last action: [state['action_robot']]" size 22 color "#FFFFFF"
                text "Last bet: [state.get('last_bet', 'N/A')]" size 22 color "#FFFFFF"
                text "Last to act: [state.get('last_to_act', 'N/A')]" size 22 color "#FFFFFF"
                text "Actual bettor: [state['current_bettor']]" size 22 color "#FFFFFF"
                text "Betting round over: [state['betting_round_over']]" size 22 color "#FFFFFF"
                text "Round finished: [state['finished']]" size 22 color "#FFFFFF"
                text "Current raises: [state['current_raises']]" size 22 color "#FFFFFF"
            # End if
        # End vbox
    # End frame
# End screen
screen SC_POKER_ACTION(engine, new_game=False):
    zorder 100
    if not new_game:
        $ p1, p2, state = get_player_state(engine)
        # ┌────────────────────────┤         FOLD          ├────────────────────────┐
        frame:
            # ──┤ "FOLD" action button displayed in a frame.
            #   ├───► Positioned at bottom right of screen.
            #   └───► Contains a "textbutton" which returns the action ("fold",) when clicked.
            xalign  0.842                                                                                                               # ═══► Horizontal position (aligned at ~84% of width)
            yalign  0.960                                                                                                               # ═══► Vertical position (aligned at ~96% of height)
            xsize   0.060                                                                                                               # ═══► Relative width (~6% of screen)
            ysize   0.050                                                                                                               # ═══► Relative height (~5% of screen)
            textbutton ("FOLD") action [Hide("SC_POKER_ACTION"), Return(("fold",))]:
                # ──┤ Clickable text button
                #   ├───► Centered horizontally in the frame with a slight vertical offset.
                #   └───► Returns the tuple ("fold",) to the engine when clicked.
                xanchor     0.5                                                                                                         # ═══► Horizontal anchor in center of knob
                xpos        67                                                                                                          # ═══► Horizontal offset of button within frame
                ypos        -5                                                                                                          # ═══► Vertical offset for an aesthetic fit
                text_style "STYLE_CHOICE_BUTTON_RED"
            # End textbutton
        # End frame
        # ┌────────────────────────┤ CHECK, CALL or ALL-IN ├────────────────────────┐
        frame:
            # ──┤ Contextual action buttons within a frame.
            #   ├───► Displayed at the bottom right of the screen (further to the right than “FOLD”).
            #   └───► Contains ONLY ONE of the following buttons:
            #           • ALL-IN → if the player is almost out of chips.
            #           • CHECK  → if no additional wager to pay.
            #           • CALL   → if a bet is to be followed.
            xalign  0.914
            yalign  0.960
            xsize   0.060
            ysize   0.050
            if p1['chips'] <= 40 and p1['clothes'] == 0:
                # ──┤ Case 1 : ALL-IN
                #   └───► If the player has ≤ 30 chips and no more clothes, we force the "ALL-IN" action.
                textbutton ("ALL-IN") action [Hide("SC_POKER_ACTION"), Return(("allin",))]:
                    xanchor 0.5
                    xpos 67
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            elif engine.last_bet == p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                # ──┤ Case 2 : CHECK
                #   └───► If the player has already matched the current bet (and still has resources), "CHECK" is proposed.
                textbutton ("CHECK") action [Hide("SC_POKER_ACTION"), Return(("check",))]:
                    xanchor 0.5
                    xpos 67
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            elif engine.last_bet > p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                # ──┤ Case 3 : CALL
                #   └───► If the player still needs to bet to match the bet, "CALL" is suggested.
                textbutton ("CALL") action [Hide("SC_POKER_ACTION"), Return(("call", engine.last_bet - p1['bet']))]:
                    xanchor 0.5
                    xpos 66
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            # End if
        # End frame
        # ┌────────────────────────┤      BET or RAISE     ├────────────────────────┐
        if engine.current_raises < engine.max_raises_per_round:
            #   ├───► This block displays a BET or RAISE button, only if the maximum number of bets for this turn has not been reached and the opponent is not in ALL-IN.
            #   │     • BET   → if no bet has been placed yet in this round.
            #   │     • RAISE → if a bid is already in progress but can be overbid.
            #   └───► Condition: further raises possible in this round.
            if engine.last_bet == p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                # ──┤ Case 1 : BET
                #   └───► If the player has matched the current bet, and still has resources, "BET" is proposed.
                frame:
                    xalign  0.986
                    yalign  0.960
                    xsize   0.060
                    ysize   0.050
                    textbutton ("BET") action [Hide("SC_POKER_ACTION"), Return(("bet", engine.big_blind))]:
                        xanchor 0.5
                        xpos 66
                        ypos -5
                        text_style "STYLE_CHOICE_BUTTON_ORANGE"
                    # End textbutton
                # End frame
            elif engine.last_bet > p1['bet'] and (p1['chips'] > (engine.last_bet - p1['bet'] + 10) or p1['clothes'] > 1) and not p2['allin']:
                # ──┤ Case 2 : RAISE
                #   └───► If a bet already exists in this round, player can "RAISE" and the opponent is not in ALL-IN.
                frame:
                    xalign  0.986
                    yalign  0.960
                    xsize   0.060
                    ysize   0.050
                    textbutton ("RAISE") action [Hide("SC_POKER_ACTION"), Return(("raise", engine.last_bet + engine.big_blind))]:
                        xanchor 0.5
                        xpos 66
                        ypos -5
                        text_style "STYLE_CHOICE_BUTTON_ORANGE"
                    # End textbutton
                # End frame
            # End if
        # End if
    elif new_game:
        # ┌────────────────────────┤      MAIN FRAME       ├─────────────────────────┐
        frame:
            #   └───► Display a help panel ("HELP") with the rules of the game, at the top right of the screen.
            #         • HELP → ouvre une fenêtre d’information détaillée
            $ information = "{b}Aim of the Game:{/b} Defeat the opponent by winning all its tokens so that it loses its clothes, before it undresses you.\n\n" \
                            "{b}How it works:{/b} Each round, players start with " + str(engine.chips) + " chips and " + str(engine.clothes) + " clothes. If you lose all your chips, you take off one cloth and receive " + str(engine.chips) + " again. " \
                            "If you have enough chips (" + str(engine.chips) + ") and fewer than " + str(engine.clothes) + " clothes, you can buy a new cloth. The game ends when a player runs out of clothes.\n\n" \
                            "{b}Poker Actions:{/b} The main actions are: Check, Call, Bet, Raise, All-In or Fold."
            background "#404040a0"
            xalign 1.0
            yalign 0.5
            xsize 0.22
            ysize 1.0
            textbutton __("HELP") action Show("SC_POKER_INFORMATION_WINDOW", int_X0=1000, int_Y0=600, text_title=__("GAME INFORMATION"), text_message=information, text_continue=__("CONTINUE...")):
                xalign 1.0
                yalign 0.0
                text_style "STYLE_CHOICE_BUTTON_HELP"
            # End textbutton
        # End frame
        # ┌────────────────────────┤       NEW GAME        ├────────────────────────┐
        frame:
            xalign  0.876
            yalign  0.960
            xsize   0.088
            ysize   0.050
            textbutton ("NEW GAME") action [Hide("SC_POKER_ACTION"), Return("new_game",)]:
                xanchor  0.5
                xpos   108
                ypos    -5
                text_style "STYLE_CHOICE_BUTTON_LIME"
            # End textbutton
        # End frame
        # ┌────────────────────────┤         QUIT          ├────────────────────────┐
        frame:
            xalign  0.980
            yalign  0.960
            xsize   0.088
            ysize   0.050
            textbutton ("QUIT") action Show("SC_POKER_INFORMATION_WINDOW", int_X0=800, int_Y0=300, text_title=__("QUESTION"), text_message=__("Are you sure you want to leave the game?"), text_size=32, confirm_mode=True, action_yes=Quit(confirm=True), action_no=Return(False), text_yes=__("YES"), text_no=__("NO")):
                xanchor 0.5
                xpos  100
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_RED"
            # End textbutton
        # End frame
    # End if
# End screen
# ┌─────────────────────────────────────────────────────────────────────────────
# │  Game information window
# └─────────────────────────────────────────────────────────────────────────────
screen SC_POKER_INFORMATION_WINDOW(
        int_X0          = 1000, 
        int_Y0          = 600, 
        text_title      = __("GAME INFORMATION"), 
        text_message    = __("Game Information"), 
        text_size       = 22,
        confirm_mode    = False,     
        action_yes      = None,
        action_no       = None,
        text_continue   = "CONTINUE...",
        text_yes        = "YES",
        text_no         = "NO",
        colorBackground = "#01008290", 
        pos_X           = 0.5, 
        pos_Y           = 0.5
    ):
    # ► Creates a modal window to display game information.
    # ► Args:
    # ►     int_X0 (int): Width of the window.
    # ►     int_Y0 (int): Height of the window.
    # ►     text_message (str): Text to display in the information window.
    # ►     text_title (str): Title of the window.
    # ►     pos_X (float): Horizontal position of the window (0.0 to 1.0).
    # ►     pos_Y (float): Vertical position of the window (0.0 to 1.0).
    # ►     colorBackground (str): Background color of the window frame.
    zorder 200                                                                                                                          # ═══► Sets the window's z-order to 200
    modal  True                                                                                                                         # ═══► Makes the window modal, blocking interaction with other elements
    window:
        xsize int_X0                                                                                                                    # ═══► Sets the window's width
        ysize int_Y0                                                                                                                    # ═══► Sets the window's height
        xalign pos_X                                                                                                                    # ═══► Aligns the window horizontally
        yalign pos_Y                                                                                                                    # ═══► Aligns the window vertically
        xpadding 6                                                                                                                      # ═══► Adds padding to the left and right of the window
        ypadding 6                                                                                                                      # ═══► Adds padding to the top and bottom of the window
        background "#91908E90"                                                                                                        # ═══► Sets the window's background color (Grey)
        frame:
            xsize int_X0 - 12                                                                                                           # ═══► Sets the frame's width
            ysize int_Y0 - 12                                                                                                           # ═══► Sets the frame's height
            background colorBackground                                                                                                  # ═══► Sets the frame's background color
            grid 1 2:                                                                                                                   # ═══► Creates a 1x2 grid layout within the frame
                hbox:                                                                                                                   # ═══► Creates a horizontal box for the title and bar
                    xsize int_X0 - 12                                                                                                   # ═══► Sets the horizontal box's width
                    ysize 100                                                                                                           # ═══► Sets the horizontal box's height
                    text "[text_title]" at truecenter size 40                                                                           # ═══► Displays the title text
                # End hbox
                hbox:                                                                                                                   # ═══► Creates a horizontal box for the information bar
                    xsize int_X0 - 12                                                                                                   # ═══► DSets the horizontal box's width
                    ysize 40                                                                                                            # ═══► Sets the horizontal box's height
                    bar xsize int_X0 - 30 ysize 5 right_bar "#91908E90"                                                               # ═══► Draws a horizontal bar
                # End hbox
            # End grid
            grid 1 1:                                                                                                                   # ═══► Creates a 1x1 grid layout for the information text
                ypos 140                                                                                                                # ═══► Sets the vertical position of the grid
                hbox:
                    text "[text_message]" justify 1 first_indent 20 rest_indent 20 size text_size
                # End hbox
            # End grid
            if confirm_mode:                                                                                                            # ═══► If confirm_mode is True, display Yes/No buttons
                grid 2 1:
                    ypos int_Y0 - 60                                                                                                    # ═══► Sets the vertical position of the grid
                    hbox:
                        textbutton (text_yes) action [Hide("SC_POKER_INFORMATION_WINDOW"), Return("quit",)]:
                            xpos int_X0 - 300                                                                                         # ═══► Sets the horizontal position of the button
                            ypos -8                                                                                                      # ═══► Sets the vertical position of the button
                            text_style "STYLE_TEXTBUTTON_HORIZONTAL_RED"
                        # End textbutton
                        textbutton (text_no) action [Hide("SC_POKER_INFORMATION_WINDOW"), Return (value=0)]:
                            xpos int_X0 - 250                                                                                         # ═══► Sets the horizontal position of the button
                            ypos -8                                                                                                      # ═══► Sets the vertical position of the button
                            text_style "STYLE_TEXTBUTTON_HORIZONTAL_LIME"
                        # End textbutton
                    # End hbox
                # End grid
            else:
                grid 1 1:                                                                                                               # ═══► Creates a 1x1 grid layout for the "Continue..." button
                    ypos int_Y0 - 60                                                                                                    # ═══► Sets the vertical position of the grid
                    hbox:
                        textbutton (text_continue) action [Hide("SC_POKER_INFORMATION_WINDOW"), Return (value=0)]:                    # ═══► Creates a "Continue..." button
                            xpos int_X0 - 250 
                            ypos -8 
                            text_style "STYLE_TEXTBUTTON_HORIZONTAL_RED"
                        # End textbutton
                    # End hbox
                # End grid
            # End if  
        # End frame
    # End window
# End screen

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Global Text Styles                                                         ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
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
style STYLE_CHOICE_BUTTON_HELP:
    font "Futura.ttc"
    size 22
    idle_color "#FFFFFF"
    hover_color "#FF0000"
    insensitive_color "#808080"
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]
# End style
style STYLE_TEXTBUTTON_HORIZONTAL_RED:
    vertical False
    color "#777777"
    hover_color "#FF0000"
    bold True
    size 28
    adjust_spacing True
    antialias True
# End style
style STYLE_TEXTBUTTON_HORIZONTAL_LIME:
    vertical False
    color "#777777"
    hover_color "#00FF00"
    bold True
    size 28
    adjust_spacing True
    antialias True
# End style

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Game Betting Rules                                                         ──
# └─────────────────────────────────────────────────────────────────────────────
 # ┌───────────────┬─────────────────────────────────┬──────────────────────────┐
 # │   Condition   │            Situation            │         Actions          │─┐
 # ├───────────────┼─────────────────────────────────┼──────────────────────────┤ │
 # │ to_call > 0   │ robot.chips > to_call + BB      │ call, raise, fold        │ │
 # │ to_call > 0   │ to_call < chips <= to_call+BB   │ call, fold               │ │
 # │ to_call > 0   │ chips <= to_call and no clothes │ all-in, fold             │ │
 # │ to_call > 0   │ chips <= 20 and no clothes      │ all-in                   │ │
 # ├───────────────┼─────────────────────────────────┼──────────────────────────┤ │
 # │ to_call == 0  │ chips => BB                     │ check, bet               │ │
 # │ to_call == 0  │ chips <= 30 and no clothes      │ all-in                   │ │
 # │ to_call == 0  │ otherwise                       │ check                    │ │
 # └───────────────┴─────────────────────────────────┴──────────────────────────┘ │
 #   └────────────────────────────────────────────────────────────────────────────┘
 
# ┌─────────────────────────────────────────────────────────────────────────────
# │  Game Logic                                                                 ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
 #      ┌─────────────────────────────────┐
 #      │         Start of Game           │
 #      ├─────────────────────────────────┤
 #      │ 1. Initialize game              │
 #      │ 2. Create players               │
 #      └────────────────┬────────────────┘
 #                       │
 #      ┌────────────────▼────────────────┐
 #      │         Main Game Loop          │
 #      ├─────────────────────────────────┤
 #      │ (While is_game_over() is False) │
 #      └────────────────┬────────────────┘
 #                       │                        ┌───────────────────┐
 #            ┌──────────▼──────────┐  YES        │     Game Over     │
 #           <   Is the game over?   >────────────►   (Quit screen)   │
 #            └──────────┬──────────┘             └───────────────────┘
 #                       │NO
 #                       │
 #      ┌────────────────▼────────────────┐
 #      │        start_new_hand()         │
 #      ├─────────────────────────────────┤
 #      │ 1. Shuffle deck of cards        │
 #      │ 2. Deal 2 cards to each player  │
 #      │ 3. Post Small & Big Blinds      │
 #      │ 4. Reset pot/round variables    │
 #      └────────────────┬────────────────┘
 #                       │
 #      ┌────────────────▼────────────────┐
 #      │       Betting Rounds Loop       │
 #      ├─────────────────────────────────┤
 #      │  (Pre-Flop, Flop, Turn, River)  │
 #      └────────────────┬────────────────┘
 #                       │
 #      ┌────────────────▼────────────────┐
 #      │       Active Player's Turn      │
 #      ├─────────────────────────────────┤
 #      │   - If Human, player_action()   │
 #      │   - If Robot, robot_action()    │
 #      └────────────────┬────────────────┘
 #                       │
 #      ┌────────────────▼────────────────┐
 #      │       Process Player Action     │
 #      ├─────────────────────────────────┤
 #      │   - Update pot,                 │
 #      │     chips, and player state     │
 #      │   - Display messages            │ 
 #      │     (using messages())          │
 #      │   - Check betting round end     │
 #      └────────────────┬────────────────┘
 #                       │
 #       ┌───────────────▼────────────┐  YES 
 #      <  Is the betting round over?  >────────────────────────────┐
 #       └────────────────────────────┘  (all active players have acted and equalized bets)
 #         │ NO                                                     │
 #         │(action taken)                                          │
 #         │                                                        │
 #         │                                                YES  ┌──▼────────────────────┐
 #         │                          ┌─────────────────────────<   More rounds to play?  >
 #         │                          │                          └───────────┬───────────┘
 #         │                          │                                      │ NO            
 #      ┌──▼──────────────────────────▼───┐                                  │(We are at the River) 
 #      │       Next active player        │                                  │
 #      └────────────────▲────────────────┘                 ┌────────────────▼────────────────┐
 #                       │                                  │            showdown()           │
 #                       │                                  ├─────────────────────────────────┤
 #      ┌────────────────┴────────────────┐                 │   - Evaluate and display hands  │
 #      │        deal_community()         │                 │   - Determine the winner        │
 #      ├─────────────────────────────────┤                 └────────────────┬────────────────┘
 #      │   - Deal Flop, Turn, or River   │                                  │
 #      └────────────────┬───────┬────────┘                                  │
 #                       │       │                          ┌────────────────▼────────────────┐
 #                       │       │                          │        distribute_pot()         │
 #                       │       │                          ├─────────────────────────────────┤
 #                       │       │                          │   - Distribute pot to winner    │
 #                       │       │                          │   - Handle side pots and ties   │
 #                       │       │                          └────────────────┬────────────────┘
 #                       │       └─────────────────────────────────────┐     │
 #                       │                                             │     │
 #      ┌────────────────▼────────────────┐                 ┌──────────▼─────▼────────────────┐
 #      │    Start Next Betting Round     │                 │         manage_clothes()        │   
 #      └────────────────────────┬────────┘                 ├─────────────────────────────────┤
 #                               │                          │   - Check chips & clothes       │
 #                               │                          │   - Buy/sell clothes as needed  │
 #                               │                          └────────────────┬────────────────┘
 #                               └─────────────────────────────────────┐     │
 #                                                                     │     │
 #                                                          ┌──────────▼─────▼────────────────┐
 #                                                          │         End of the hand         │
 #                                                          └─────────────────────────────────┘
 
# ┌─────────────────────────────────────────────────────────────────────────────
# │  Showdown diagram                                                           ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
 #                          ┌─────────────────────┐
 #                          │      showdown()     │
 #                          └──────────┬──────────┘
 #                                     │
 #                ┌────────────────────┴────────────────────┐
 #                │                                         │
 #      ┌─────────┴─────────┐                     ┌─────────┴─────────┐
 #      │ Hand calculation  │                     │   Hand display    │
 #      └─────────┬─────────┘                     └─────────┬─────────┘
 #                │                                         │
 #     - Collect cards from each player           - Disclose Human and Robot cards
 #     - Evaluates hand strength                  - Disclose hand strength
 #                │                                         │
 #      ┌─────────┴─────────┐                               │
 #      │ Determines winner │ ◄═════════════════════════════╛
 #      └─────────┬─────────┘
 #                │
 #      (Human, Robot, or equality)
 #                │
 #      ┌─────────┴─────────┐
 #      │Distribute the pot │
 #      └─────────┬─────────┘
 #                │
 #     - Different bet cases :
 #         * winner takes all
 #         * loser recovers diff
 #         * or share
 #     - Equal bets case :
 #         * winner takes all
 #         * or share
 #                │
 #      ┌─────────┴─────────┐
 #      │ Manages chips < 0 │
 #      └─────────┬─────────┘
 #                │
 #      - If Human/Robot has 0 chips :
 #         * Lose a cloth
 #         * Starts with 100 new chips
 #                │
 #      ┌─────────┴─────────┐
 #      │ Reset game status │
 #      └─────────┬─────────┘
 #                │
 #         - pot = 0
 #         - bets reset to 0
 #         - all-in reset to False
 #                │
 #      ┌─────────┴─────────┐
 #      │        End        │
 #      └───────────────────┘

# ┌─────────────────────────────────────────────────────────────────────────────
# │  Distribution Pot diagram                                                   ──
# └─────────────────────────────────────────────────────────────────────────────
#    └────────────────────────────────────────────────────────────────────────────
 #             ┌────────────────────────┐
 #             │ distribute_pot(winner) │
 #             └───────────┬────────────┘
 #                         │
 #               ┌─────────▼──────────┐
 #               │    Bets equal?     ├────────────┐
 #               └───────┬────────────┘            │
 #                       │Yes                      │No
 #            ┌──────────▼────────┐    ┌───────────▼──────────┐
 #            │      Winner?      │    │ Winner = higher bet? ├──┐
 #            └─┬────────┬───────┬┘    └┬─────────┬───────────┘  │
 #              │Yes     │No     │Yes   │Yes      │No            │
 #         ┌────▼───┐ ┌──▼────┐ ┌▼──────▼┐  ┌─────▼─────────┐ ┌──▼─────────────┐
 #         │ Win all│ │ Split │ │ Win all│  │ Winner:       │ │ Tie: both get  │
 #         │  pot   │ │ pot/2 │ │  pot   │  │ pot           │ │ min_bet+diff→  │
 #         │        │ │       │ │        │  │               │ │ higher better  │
 #         └────────┘ └───────┘ └────────┘  │               │ └────────────────┘
 #                                          │ OR: lower     │
 #                                          │ bet wins →    │
 #                                          │ pot+2×min     │
 #                                          │ surplus→loser │
 #                                          └───────────────┘