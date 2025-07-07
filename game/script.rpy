# ╔═════════════════════════════════════════════════════════════════════════════
# ║  Strip Poker Texas Hold'em - Ren'Py                                         ──
# ║   ► Two players: human vs. computer.
# ║   ► Each player starts each round with 100 tokens and 5 clothes
# ║   ► If a player loses a round, he removes a suit and gets back 100 tokens.
# ║   ► Gestion des mises standards 
# ║   ►     (S. Blind, B. Blind, Check, Call, Raise, Bet, All-In)
# ║   ► Displaying maps with images/cards/02C.png ... 14S.png
# ╚═════════════════════════════════════════════════════════════════════════════
#    ╰────────────────────────────────────────────────────────────────────────────
    
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global Python classes                                                      ──
# ╰─────────────────────────────────────────────────────────────────────────────
#    ╰────────────────────────────────────────────────────────────────────────────
init python:
    import random

    SUITS                                             = ['C', 'D', 'H', 'S']
    RANKS                                             = [str(n).zfill(2) for n in range(2, 15)]
    CARDNAMES                                         = [r+s for r in RANKS for s in SUITS]

    # ┌───────────────────────────────┤  Class  ├───────────────────────────────┐
    # │  Class representing a Strip Poker Texas Hold'em player                  │
    # └─────────────────────────────────────────────────────────────────────────┘
    class Player:
        # │ ┌────────────────────────────────────────────────────────────────────
        # ╰─┤ Attributes:
        #   └────────────────────────────────────────────────────────────────────
        #    ├─ name (str)       : Player's name.
        #    ├─ chips (int)      : Number of chips currently owned.
        #    ├─ clothes (int)    : Number of clothes currently worn.
        #    ├─ max_clothes (int): Maximum number of clothes (initial value).
        #    ├─ cards (list)     : List of cards in hand (e.g. ["02C", "14S"]).
        #    ├─ bet (int)        : Player's current bet for the current round.
        #    ├─ folded (bool)    : Indicates whether the player has folded.
        # │ ┌────────────────────────────────────────────────────────────────────
        # ╰─┤ Methods :
        #   └────────────────────────────────────────────────────────────────────
        #    ├─ __init__(name, chips=100, clothes=5)
        #    ├───► Initializes a player with a name, chips and clothes.
        #    ├─ reset()
        #    ├───► Resets the player's hand for a new round, empties the 
        #    │     cards, resets the bets and removes the state.
        #    ├─ try_buy_clothes()
        #    ├───► As long as the player doesn't have the maximum number of 
        #    │     clothes and has > 110 chips, buys a new cloth for 100 chips.
        def __init__(self, name, chips=100, clothes=5):
            self.name                                 = name
            self.chips                                = chips
            self.clothes                              = clothes
            self.max_clothes                          = clothes
            self.cards                                = []
            self.bet                                  = 0
            self.folded                               = False
        # End def
        def reset(self):
            self.cards                                = []
            self.bet                                  = 0
            self.folded                               = False
        # End def
        def try_buy_clothes(self):
            while self.clothes < self.max_clothes and self.chips >= 110:
                self.clothes += 1
                self.chips -= 100
                renpy.say(None, f"{self.name} rachète un habit pour 100 jetons !")
                renpy.pause(1.0)
        # End def
    # End class
    # ┌───────────────────────────────┤  Class  ├───────────────────────────────┐
    # │  Class to manages a Strip Poker Texas Hold'em game between two players  │
    # └─────────────────────────────────────────────────────────────────────────┘
    class PokerGame:
        # │ ┌────────────────────────────────────────────────────────────────────
        # ╰─┤ Attributes:
        #   └────────────────────────────────────────────────────────────────────
        #    ├─ players (list[Player]) : List of two players (human and AI).
        #    ├─ community (list[str])  : Common cards on the table.
        #    ├─ pot (int)              : Total amount of pot.
        #    ├─ deck (list[str])       : Deck of remaining cards.
        #    ├─ round (int)            : Betting round number 
        #    │                           (0=préflop, 1=flop, 2=turn, 3=river).
        #    ├─ dealer (int)           : Dealer's index (0 or 1).
        #    ├─ small_blind (int)      : Value of the small blind.
        #    ├─ big_blind (int)        : Value of the big blind.
        #    ├─ current_bettor (int)   : Index of the player to act.
        #    ├─ last_bet (int)         : Amount of last bet.
        #    ├─ finished (bool)        : Indicates whether the run is over.
        #    ├─ winner (int|None)      : Round winner's index (0, 1 or None for a tie).
        #    ├─ manche (int)           : Round counter.
        #    ├─ betting_round_over     : Indicates whether the betting round is over.
        #    ├─ last_to_act (int|None) : Index of the last player to act.
        #    ├─ quit (bool)            : Indicates whether the game has been exited.
        # │ ┌────────────────────────────────────────────────────────────────────
        # ╰─┤ Methods :
        #   └────────────────────────────────────────────────────────────────────
        #    ├─ __init__(player_name, ai_name, ...)
        #    ├───► Initializes the game and the players.
        #    ├─ ai_action()
        #    ├───► Determines and returns the AI action (call, raise, fold, etc.).
        #    ├─ check_habit_jetons(idx)
        #    ├───► Manages the logic of losing/buying clothes and reloading
        #    │     tokens according to the idx player's state.
        #    ├─ deal_community()
        #    ├───► Distributes community cards (flop, turn, river) and
        #    │     resets bets.
        #    ├─ get_state()
        #    ├───► Returns the current state of the game in dictionary
        #    │     form (for the UI).
        #    ├─ is_game_over()
        #    ├───► Returns True if the game is over (one player without 
        #    │     clothes or quit).
        #    ├─ player_action(idx, action, amount=0)
        #    ├───► Applies a player's action (fold, call, raise, check, 
        #    │     allin, quit).
        #    ├─ showdown()
        #    ├───► Compares hands, determines winner, distributes pot 
        #    │     and handles ties.
        #    ├─ start_new_hand()
        #    ├───► Prepare a new round (mixing, distribution, blinds...).
        #    ├─ strip_loser()
        #    ├───► If the loser runs out of tokens, he loses a 
        #    │     cloth and receives 100 tokens.
        def __init__(self, player_name, ai_name, small_blind=10, big_blind=20, chips=100, clothes=5, aggressiveness=0.5, max_raises_per_round=4):
            self.action_ai                              = None
            self.aggressiveness                         = aggressiveness
            self.betting_round_over                     = False
            self.big_blind                              = big_blind
            self.community                              = []
            self.current_bettor                         = 0
            self.current_raises                         = 0
            self.dealer                                 = 0
            self.deck                                   = []
            self.finished                               = False
            self.last_bet                               = 0
            self.last_to_act                            = None
            self.manche                                 = 0
            self.max_raises_per_round                   = max_raises_per_round  # Limite de raises par tour
            self.players                                = [Player(player_name, chips, clothes), Player(ai_name, chips, clothes)]
            self.pot                                    = 0
            self.quit                                   = False
            self.round                                  = 0
            self.small_blind                            = small_blind
            self.winner                                 = None
        # End def
        def ai_action(self):
            ai = self.players[1]
            if ai.chips <= 0 and ai.clothes > 0:                                                                                        # ═══► Automatic reload if AI has no more tokens but still has clothes
                ai.clothes -= 1
                ai.chips   += 100
                renpy.say(None, "[ai.name] has no more chips, so it sells a suit and receives 100 chips to continue the hand.")
                renpy.pause(1.0)
                ai.try_buy_clothes()
            # End if
            if ai.folded:
                return 'fold', 0
            # End if
            to_call = self.last_bet - ai.bet
            actions = []
            if to_call > 0:
                if ai.chips > to_call + self.big_blind:
                    actions = [('call', to_call), ('raise', self.big_blind), ('fold', 0)]
                elif ai.chips >= to_call:
                    actions = [('call', to_call), ('fold', 0)]
                # End if
            else:
                if ai.chips > self.big_blind:
                    actions = [('check', 0), ('bet', self.big_blind)]
                else:
                    actions = [('check', 0)]
                # End if
            # End if
            if not actions:
                return 'check', 0
            if ('check', 0) in actions:                                                                                                 # ═══► AI should not fold if it can check for free
                actions = [a for a in actions if a[0] != 'fold']
            # End if
            if to_call > 0:                                                                                                             # ═══► AI must never be able to check if it has to follow a bet.                                                                                    
                actions = [a for a in actions if a[0] != 'check']
            # End if
            # ──┤  Weighting according to aggressiveness
            #   ╰───► Selects an action based on possible actions, game state and AI aggression. 
            #         Returns a randomly chosen action, weighted by calculated weights.
            #          ├───► actions: liste de tuples (action:str, amount:int), ex : [((“raise”, 20), (“call”, 10), (“fold”, 0)]
            #          ├───► engine: object with current_raises and max_raises_per_round
            #          ├───► aggressiveness: float between 0 and 1
            #          ╰───►  :return: tuple (action:str, amount:int)
            weights = []                                                                                                                # ═══► List of weights for each action
            for action, amount in actions:                                                                                              # ═══► Evaluate each action and assign it a weighting
                if action in ('raise', 'bet'):
                    if engine.current_raises < engine.max_raises_per_round:                                                             # ═══► If we can still "Raise" or "Bet", we need to balance it with aggression
                        weights.append(self.aggressiveness)
                    else:
                        weights.append(0)
                    # End if
                elif action in ('call', 'check'):                                                                                       # ═══► If the maximum number of retries is reached, very low weight
                    weights.append(1 - self.aggressiveness)                                                                             # ═══► These actions are more attractive to a prudent AI
                else:
                    weights.append(0.2)                                                                                                 # ═══► If the action is 'fold', we give it a small weight to keep the AI prudent
                # End if
            total = sum(weights)                                                                                                        # ═══► Normalising weights to form a valid distribution
            if total > 0:
                weights = [w / total for w in weights]
            else:
                weights = [1 / len(actions)] * len(actions)                                                                             # ═══► If the total is zero (highly unlikely), we standardise the probability
            # End if
            self.action_ai = random.choices(actions, weights=weights, k=1)[0]                                                           # ═══► Select an action at random, taking into account the weights
            return self.action_ai
        # End def
        def check_habit_jetons(self, idx):
            p = self.players[idx]
            if p.chips < 20 and p.clothes == 1:                                                                                         # ═══► If the player has fewer than 20 tokens and only one cloth, he is forced to All-In
                renpy.say(None, f"{p.name} est forcé de faire All-In !")
                return 'allin'
            elif p.clothes > 1 and p.chips <= 0:                                                                                        # ═══► Lose a cloth and reload 100 chhips if cloth > 1 and tokens <= 0
                p.clothes  -= 1
                p.chips    += 100
                renpy.say(None, f"{p.name} perd un habit et reçoit 100 jetons.")
                return 'recharge'
            elif p.clothes < p.max_clothes and p.chips >= 110:                                                                          # ═══► Buy a cloth if clothes < max_clothes and tokens >= 110
                p.clothes  += 1
                p.chips    -= 100
                renpy.say(None, f"{p.name} rachète un habit pour 100 jetons !")
                return 'buy'
            # End if
            return None
        # End def
        def deal_community(self):
            if self.round == 0:
                self.community = [self.deck.pop() for _ in range(3)]
            elif self.round < 3:
                self.community.append(self.deck.pop())
            # End if
            self.round += 1
            for p in self.players:
                p.bet = 0
            # End for
            self.last_bet = 0
            self.betting_round_over = False
            self.current_bettor = (self.dealer + 1) % 2
            self.last_to_act = self.dealer
            self.current_raises = 0  # Réinitialise le compteur de raises à chaque nouveau tour
            return self.round
        # End def
        def get_state(self):
            return {
                'players':                          [vars(p) for p in self.players],
                'action_ai':                        self.action_ai,
                'betting_round_over':               self.betting_round_over,
                'big_blind':                        self.big_blind,
                'community':                        self.community[:],
                'current_bettor':                   self.current_bettor,
                'finished':                         self.finished,
                'last_bet':                         self.last_bet,
                'last_to_act':                      self.last_to_act,
                'manche':                           self.manche,
                'pot':                              self.pot,
                'quit':                             self.quit,
                'round':                            self.round,
                'small_blind':                      self.small_blind,
                'winner':                           self.winner
            }
        # End def
        def is_game_over(self):
            return any(p.clothes == 0 for p in self.players) or self.quit
        # End def
        def player_action(self, idx, action, amount=0):
            global TEXT_INFOS_MEASSAGE_1, TEXT_INFOS_MEASSAGE_2, TEXT_INFOS_MEASSAGE
            p = self.players[idx]
            opp = self.players[1-idx]
            if action == 'quit':
                self.quit = True
                self.finished = True
                self.betting_round_over = True
                return
            # End if
            if action == 'fold':
                p.folded = True
                self.finished = True
                self.winner = 1 - idx
                self.betting_round_over = True
                self.players[self.winner].chips += self.pot
                global TEXT_INFOS_MEASSAGE
                TEXT_INFOS_MEASSAGE = f"{self.players[self.winner].name} remporte le pot de {self.pot} jetons car l'autre joueur s'est couché.\nLe pot est remis à zéro."
                self.pot = 0
                return
            elif action == 'call':
                to_call = self.last_bet - p.bet
                p.chips -= to_call
                p.bet += to_call
                if self.current_bettor == 0:
                    TEXT_INFOS_MEASSAGE_1 = "Vous suivez."
                else:
                    TEXT_INFOS_MEASSAGE_1 = f"{p.name} suit."
                # End if
                TEXT_INFOS_MEASSAGE_2 = f"La relance est de {to_call} jetons."
                self.pot += to_call
                if p.chips <= 0:
                    p.clothes -= 1
                    global TEXT_INFOS_MEASSAGE
                    TEXT_INFOS_MEASSAGE = f"{p.name} n'a plus de jetons, il/elle perd un habit et reçoit 100 jetons pour continuer la main."
                    p.chips += 100
                p.try_buy_clothes()
                if self.last_to_act == idx:
                    self.betting_round_over = True
                else:
                    self.current_bettor = 1 - idx
            elif action == 'bet':
                amount = self.big_blind
                p.chips -= amount
                p.bet += amount
                self.pot += amount
                self.last_bet = p.bet
                self.last_to_act = idx
                self.current_bettor = 1 - idx  # Passe la main à l'autre joueur (IA)
                self.current_raises += 1
                if p.chips <= 0:
                    p.clothes -= 1
                    global TEXT_INFOS_MEASSAGE
                    TEXT_INFOS_MEASSAGE = f"{p.name} n'a plus de jetons, il/elle perd un habit et reçoit 100 jetons pour continuer la main."
                    p.chips += 100
                    p.try_buy_clothes()
            elif action == 'raise':
                amount = self.big_blind
                to_call = self.last_bet - p.bet
                total = to_call + amount
                p.chips -= total
                p.bet += total
                if self.current_bettor == 0:
                    TEXT_INFOS_MEASSAGE_1 = "Vous relancez."
                else:
                    TEXT_INFOS_MEASSAGE_1 = f"{p.name} relance."
                # End if
                TEXT_INFOS_MEASSAGE_2 = f"La relance est de {total} jetons."
                self.pot += total
                self.last_bet = p.bet
                self.last_to_act = idx
                self.current_bettor = 1 - idx  # Passe la main à l'autre joueur (IA)
                self.current_raises += 1
                if p.chips <= 0:
                    p.clothes -= 1
                    TEXT_INFOS_MEASSAGE = f"{p.name} n'a plus de jetons, il/elle perd un habit et reçoit 100 jetons pour continuer la main."
                    p.chips += 100
                # End if
                p.try_buy_clothes()
            elif action == 'check':
                if self.current_bettor == 0:
                    TEXT_INFOS_MEASSAGE_1 = "Vous checkez."
                else:
                    TEXT_INFOS_MEASSAGE_1 = f"{p.name} check."
                # End if
                TEXT_INFOS_MEASSAGE_2 = " "
                if self.last_to_act == idx:                                                                                             # ═══► If the player who checks is the last to act, the betting round is over.
                    self.betting_round_over = True
                else:
                    self.current_bettor = 1 - idx
                # End if
            elif action == 'allin':
                to_call = self.last_bet - p.bet
                total = p.chips
                if to_call > total:
                    to_call = total
                p.bet += total
                self.pot += total
                p.chips = 0
                global TEXT_INFOS_MEASSAGE
                TEXT_INFOS_MEASSAGE = f"{p.name} fait tapis avec {total} jetons !"
                self.last_bet = max(self.last_bet, p.bet)
                self.last_to_act = idx
                self.betting_round_over = True
                return
            # End if
        # End def
        def showdown(self):
            def card_value(card):
                return int(card[:2])
            # End def
            def card_suit(card):                                                                                                        # ═══► Function for obtaining the value and colour of a card
                return card[2]                                                                                                          #      Ex: "02C" -> (2, 'C')
            # End def
            def hand_rank(cards):
                values  = sorted([card_value(c) for c in cards], reverse=True)
                suits   = [card_suit(c) for c in cards]
                counts  = {v: values.count(v) for v in set(values)}
                pairs   = [v for v, c in counts.items() if c == 2]
                trips   = [v for v, c in counts.items() if c == 3]
                quads   = [v for v, c in counts.items() if c == 4]
                flush   = None
                for s in set(suits):
                    if suits.count(s) >= 5:
                        flush = s
                        break
                    # End if
                # End for
                uniq = sorted(set(values), reverse=True)
                if 14 in uniq:
                    uniq.append(1)
                # End if
                straight = None
                for i in range(len(uniq)-4):
                    if uniq[i] - uniq[i+4] == 4:
                        straight = uniq[i]
                        break
                    # End if
                # End for
                straight_flush = None
                if flush:
                    flush_cards = [card_value(c) for c in cards if card_suit(c) == flush]
                    flush_uniq = sorted(set(flush_cards), reverse=True)
                    if 14 in flush_uniq:
                        flush_uniq.append(1)
                    # End if
                    for i in range(len(flush_uniq)-4):
                        if flush_uniq[i] - flush_uniq[i+4] == 4:
                            straight_flush = flush_uniq[i]
                            break
                        # End if
                    # End for
                # End if
                if straight_flush:
                    return (8, straight_flush, values)
                # End if
                if quads:
                    return (7, max(quads), values)
                # End if
                if trips and pairs:
                    return (6, max(trips), max(pairs), values)
                # End if
                if flush:
                    flush_cards = [card_value(c) for c in cards if card_suit(c) == flush]
                    return (5, sorted(flush_cards, reverse=True))
                # End if
                if straight:
                    return (4, straight, values)
                # End if
                if trips:
                    return (3, max(trips), values)
                # End if
                if len(pairs) >= 2:
                    return (2, max(pairs), min(pairs), values)
                # End if
                if pairs:
                    return (1, max(pairs), values)
                # End if
                return (0, values)
            # End def
            p1, p2 = self.players                                                                                                       # ═══► Compose hands
            cards1 = p1.cards + self.community
            cards2 = p2.cards + self.community
            rank1 = hand_rank(cards1)
            rank2 = hand_rank(cards2)
            renpy.say(None, f"Votre main : {p1.cards} | Main IA : {p2.cards}")
            renpy.say(None, f"Cartes communes : {self.community}")
            renpy.say(None, f"Votre force : {rank1} | Force IA : {rank2}")
            if rank1 > rank2:
                winner = 0
                renpy.say(None, "Vous gagnez la main !")
            elif rank2 > rank1:
                winner = 1
                renpy.say(None, "L'ordinateur gagne la main !")
            else:
                winner = None
                renpy.say(None, "Égalité parfaite ! Le pot est partagé.")
            # End if
            self.winner = winner
            bet1, bet2  = p1.bet, p2.bet
            min_bet     = min(bet1, bet2)
            max_bet     = max(bet1, bet2)
            diff        = max_bet - min_bet
            if bet1 != bet2:
                if bet1 > bet2:
                    if winner == 0:
                        p1.chips += self.pot
                        renpy.say(None, f"Vous remportez tout le pot ({self.pot} jetons) !")
                        p1.try_buy_clothes()
                    elif winner == 1:
                        p2.chips += 2 * bet2
                        p1.chips += diff
                        renpy.say(None, f"L'ordinateur remporte {2*bet2} jetons, vous récupérez la différence ({diff} jetons).")
                    else:
                        p1.chips += diff
                        p1.chips += min_bet
                        p2.chips += min_bet
                        renpy.say(None, f"Égalité : chacun récupère {min_bet} jetons, vous récupérez la différence ({diff} jetons).")
                    # End if
                else:
                    if winner == 1:
                        p2.chips += self.pot
                        renpy.say(None, f"L'ordinateur remporte tout le pot ({self.pot} jetons) !")
                        p2.try_buy_clothes()
                    elif winner == 0:
                        p1.chips += 2 * bet1
                        p2.chips += diff
                        renpy.say(None, f"Vous remportez {2*bet1} jetons, l'ordinateur récupère la différence ({diff} jetons).")
                    else:
                        p2.chips += diff
                        p1.chips += min_bet
                        p2.chips += min_bet
                        renpy.say(None, f"Égalité : chacun récupère {min_bet} jetons, l'ordinateur récupère la différence ({diff} jetons).")
                    # End if
                # End if
            else:
                if winner == 0:
                    p1.chips += self.pot
                    renpy.say(None, f"Vous remportez tout le pot ({self.pot} jetons) !")
                    p1.try_buy_clothes()
                elif winner == 1:
                    p2.chips += self.pot
                    renpy.say(None, f"L'ordinateur remporte tout le pot ({self.pot} jetons) !")
                    p2.try_buy_clothes()
                else:
                    p1.chips += self.pot // 2
                    p2.chips += self.pot // 2
                    renpy.say(None, f"Égalité : le pot est partagé ({self.pot // 2} jetons chacun).")
                # End if
            # End if
            self.finished = True
            self.betting_round_over = True
            if p1.chips <= 0:
                renpy.say(None, "Vous n'avez plus de jetons, vous perdez un habit et repartez avec 100 jetons de plus.")
                p1.clothes -= 1
                p1.chips += 100
                renpy.pause(1.0)
            elif p2.chips <= 0:
                renpy.say(None, "L'ordinateur n'a plus de jetons, il perd un habit et repart avec 100 jetons de plus.")
                p2.clothes -= 1
                p2.chips += 100
                renpy.pause(1.0)
            # End if
            renpy.say(None, f"Le pot est maintenant remis à zéro.")
            self.pot = 0
            renpy.pause(1.0)
            for p in self.players:
                p.bet = 0
            # End for
        # End def
        def start_new_hand(self):
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
            # ► Determining who starts talking pre-flop
            # ►   In a 2-player game:
            # ►     Dealer (SB) speaks second
            # ►     Non-dealer (BB) speaks first
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
            #   ╰───► the right player is ready to talk
        # End def
        def strip_loser(self):
            if self.winner is not None:
                loser = 1 - self.winner
                if self.players[loser].chips <= 0:
                    self.players[loser].clothes      -= 1
                    self.players[loser].chips        += 100
                    if self.players[0]:
                        renpy.say(None, "Vous perdez un habit et vous recevez 100 jetons.")
                    # End if
                    if self.players[1]:
                        renpy.say(None, f"{self.players[loser].name} perd un habit et reçoit 100 jetons.")
                    # End if
                    renpy.pause(1.0)
                # End if
            # End if
        # End def
    # End class
    # ┌──────────────────────────────┤  Function  ├─────────────────────────────┐
    # │  Function for obtaining player and game status                          │
    # └─────────────────────────────────────────────────────────────────────────┘
    def get_player_state(engine):
        state = engine.get_state()                                                                                                      # ═══► Get the current state of the game
        p1 = state['players'][0]
        p2 = state['players'][1]
        return p1, p2, state
    # End def
    # ┌──────────────────────────────┤  Function  ├─────────────────────────────┐
    # │  Function for displaying cards images                                   │
    # └─────────────────────────────────────────────────────────────────────────┘
    def get_card_image(card):
        return f"images/cards/{card}.png"
    # End def
# End init python

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global variables                                                           ──
# ╰─────────────────────────────────────────────────────────────────────────────
#    ╰────────────────────────────────────────────────────────────────────────────
default TEXT_INFOS_MEASSAGE     = ""
default TEXT_INFOS_MEASSAGE_1   = ""
default TEXT_INFOS_MEASSAGE_2   = ""
default CHEAT_POKER             = True
default DEBUG_POKER             = True

image bg poker                  = "images/poker.jpg"

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global Labels                                                              ──
# ╰─────────────────────────────────────────────────────────────────────────────
#    ╰────────────────────────────────────────────────────────────────────────────
label start:
    python:
        engine = PokerGame("Vous", "Ordinateur", small_blind=10, big_blind=20, chips=100, clothes=5, aggressiveness=0.4, max_raises_per_round=4)
    jump LB_GAME_POKER
# End label
label LB_GAME_POKER:
    # ╰───► Initializes a new poker round: 
    #   ╰───► It increments the round counter. 
    #   ╰───► It prepares the distribution of the cards and blinds.
    #   ╰───► Then it displays the state of play on the screen.
    #   ╰───► It then transfers control to the betting_round label to manage the betting round.
    #   ╰───► This is the main entry point for each new hand in the betting loop.
    scene bg poker
    show screen SC_POKER_ACTION(engine, new_game=True)                                          # Affiche le screen de choix nouvelle partie/quit
    $ result = ui.interact()
    if result == "quit":
        return
    # End if
    python:
        engine.start_new_hand()
    # End python
    show screen SC_POKER_STATUS(engine, reveal_ai=False)                                                        # ═══► Sinon, on continue la partie normalement
    show screen SC_POKER_ACTION(engine, new_game=False)                                          # Affiche le screen de choix nouvelle partie/quit
    jump LB_BETTING_ROUND
# End label
label LB_BETTING_ROUND:
    python:
        state        = engine.get_state()
        finished     = state['finished']
        betting_over = state['betting_round_over']
        round_num    = state['round']
        p1, p2, _    = get_player_state(engine)
    # End python
    if finished:
        if state['winner'] is not None:
            $ winner_name  = state['players'][state['winner']]['name']
            $ loser_name   = state['players'][1 - state['winner']]['name']
            if state['winner'] == 0:
                $ win_text = f"Vous gagnez la manche !"
            else:
                $ win_text = f"{winner_name} gagne la manche !"
            # End if
        else:
            $ win_text = "Égalité ! Personne ne se déshabille."
        # End if
        hide screen SC_POKER_ACTION
        $ TEXT_INFOS_MEASSAGE_2 = win_text
        python:
            engine.strip_loser()
            if engine.is_game_over():
                renpy.jump("LB_GAME_OVER")
            # End if
        # End python
        jump LB_GAME_POKER
    if betting_over:
        if round_num < 3:
            python:
                result = engine.deal_community()
                if result == 1:
                    TEXT_INFOS_MEASSAGE_1 = "Flop ! 3 cartes communes sont distribuées."
                    if engine.current_bettor == 0:
                        TEXT_INFOS_MEASSAGE_2 = "C'est à votre tour de jouer !"
                    else:
                        TEXT_INFOS_MEASSAGE_2 = f"C'est au tour de {engine.players[1].name} de jouer !"
                    # End if    
                    renpy.pause(2, hard=True)                                                                                  # ═══► Pause to let the player see the community cards before AI plays
                elif result == 2:
                    TEXT_INFOS_MEASSAGE_1 = "Turn ! 1 carte commune est distribuée."
                    if engine.current_bettor == 0:
                        TEXT_INFOS_MEASSAGE_2 = "C'est à votre tour de jouer !"
                    else:
                        TEXT_INFOS_MEASSAGE_2 = f"C'est au tour de {engine.players[1].name} de jouer !"
                    # End if    
                    renpy.pause(2, hard=True)                                                                                  # ═══► Pause to let the player see the community cards before AI plays
                elif result == 3:
                    TEXT_INFOS_MEASSAGE = "River ! 1 carte commune est distribuée."
                    if engine.current_bettor == 0:
                        TEXT_INFOS_MEASSAGE_2 = "C'est à votre tour de jouer !"
                    else:
                        TEXT_INFOS_MEASSAGE_2 = f"C'est au tour de {engine.players[1].name} de jouer !"
                    # End if    
                    renpy.pause(2, hard=True)                                                                                  # ═══► Pause to let the player see the community cards before AI plays
                else:
                    TEXT_INFOS_MEASSAGE_1 = "Fin de la manche !"
                    TEXT_INFOS_MEASSAGE_2 = " "
                    " ... DEBUG: FIN DE LA MANCHE ... "
                # End if
            # End python
            jump LB_BETTING_ROUND
        else:
            python:
                engine.showdown()
            # End python
            $ TEXT_INFOS_MEASSAGE_1 = "Showdown."
            $ TEXT_INFOS_MEASSAGE_2 = "Les cartes sont révélées."
            hide screen SC_POKER_ACTION
            show screen SC_POKER_STATUS(engine, reveal_ai=True)
            " ... DEBUG: SHOWDOWN ... "
            jump LB_BETTING_ROUND
    python:
        player_turn = engine.current_bettor == 0
        p1, p2, _ = get_player_state(engine)
    if player_turn and not engine.players[0].folded:                                                                        # ═══► If it's the player's turn and they haven't folded, display action buttons
        $ renpy.pause(1.0, hard=True)
        show screen SC_POKER_ACTION(engine, new_game=False)                                          # Affiche le screen d’action du joueur
        call LB_PLAYER_ACTION
        jump LB_BETTING_ROUND
    elif not engine.players[1].folded:
        hide screen SC_POKER_ACTION
        python:
            action, amount = engine.ai_action()
            engine.player_action(1, action, amount)
            result = engine.check_habit_jetons(1)
            if result == 'allin':
                engine.player_action(1, 'allin')
                engine.betting_round_over = True
                TEXT_INFOS_MEASSAGE = f"{engine.players[1].name} est forcé de faire All-In !"
            elif result == 'recharge':
                TEXT_INFOS_MEASSAGE_1 = f"{engine.players[1].name} n'a plus de jetons."
                TEXT_INFOS_MEASSAGE_2 = f"{engine.players[1].name} vend un habit et reçoit 100 jetons."
            elif result == 'buy':
                TEXT_INFOS_MEASSAGE_1 = f"{engine.players[1].name} rachète un habit pour 100 jetons !"
                TEXT_INFOS_MEASSAGE_2 = f"{engine.players[1].name} a maintenant {engine.players[1].clothes} habits."
            else:
                if action == 'fold':
                    TEXT_INFOS_MEASSAGE_1 = f"{engine.players[1].name} se couche !"
                    TEXT_INFOS_MEASSAGE_2 = f"Vous remportez le pot de {engine.pot} jetons."
                    engine.betting_round_over = True
                elif action == 'call':
                    if engine.last_to_act == 1:
                        engine.betting_round_over = True
                    else:
                        engine.current_bettor = 0
                elif action == 'raise':
                    engine.current_bettor = 0
                elif action == 'check':
                    if engine.last_to_act == 1:
                        engine.betting_round_over = True
                    else:
                        engine.current_bettor = 0
                elif action == 'allin':
                    TEXT_INFOS_MEASSAGE_1 = "L'ordinateur fait tapis !"
                    TEXT_INFOS_MEASSAGE_2 = "C'est à votre tour de jouer."
                    engine.current_bettor = 0
            renpy.pause(1.0)
            renpy.restart_interaction()
        jump LB_BETTING_ROUND
# End label

label LB_PLAYER_ACTION:
    # Affiche le screen d’action et attend le choix du joueur
    $ action_tuple = ui.interact()
    $ action = action_tuple[0]
    python:
        engine.player_action(0, action)
    if action == "fold":
        $ TEXT_INFOS_MEASSAGE_1 = "Vous vous couchez."
        $ TEXT_INFOS_MEASSAGE_2 = "Vous abandonnez la main."
    elif action == "call":
        pass
    elif action == "raise":
        pass
    elif action == "check":
        pass
    elif action == "bet":
        $ TEXT_INFOS_MEASSAGE_1 = "Vous misez."
        $ TEXT_INFOS_MEASSAGE_2 = "Vous misez {} jetons.".format(action_tuple[1])
    elif action == "allin":
        $ TEXT_INFOS_MEASSAGE = "Vous faites tapis !"
    elif action == "quit":
        $ TEXT_INFOS_MEASSAGE = "Vous quittez la partie."
    show screen SC_POKER_STATUS(engine, reveal_ai=False)
    hide screen SC_POKER_ACTION
    $ renpy.pause(1.0)
    return

label LB_GAME_OVER:
    # ╰───► Displays an end-of-game screen with the message "Game over!":
    #   ╰───► Then offers the player the option of playing a new game or quitting.
    #   ╰───► It therefore manages the conclusion of the game and the choice of restarting or quitting.
    scene bg poker
    show text "Fin de la partie !" at truecenter with dissolve
    $ renpy.pause(1.0)
    menu:
        "Rejouer une partie ?"
        "Oui":
            jump start
        "Non":
            $ renpy.quit()
    # End menu
# End label

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global Screens                                                             ──
# ╰─────────────────────────────────────────────────────────────────────────────
#    ╰────────────────────────────────────────────────────────────────────────────
screen SC_POKER_STATUS(engine, reveal_ai=False):
    $ p1, p2, state = get_player_state(engine)
    # ┌────────────────────────┤      Main Frame      ├─────────────────────────┐
    frame:
        background "#404040a0"
        xalign 1.0
        yalign 0.5
        xsize 0.22
        ysize 1.0
    # End frame
    # ┌────────────────────────┤   Background Frame    ├────────────────────────┐
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.8
        xsize 0.21
        ysize 0.2
        vbox spacing 30:
            text "{b}Your chips: [p1['chips']]{/b}" size 26 color "#FFFFFF"
            grid 2 1:
                hbox spacing -220:
                    xsize 350
                    for c in p1['cards']:
                        add get_card_image(c) xsize 188 ysize 251
                    # End for
                # End hbox
            # End Grid
        # End vbox
    # End frame
    # ┌────────────────────────┤  Human's Information  ├────────────────────────┐
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
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.905
        xsize 0.21
        ysize   0.04
        hbox:
            text "{b}Current bet: [p1['bet']]{/b}" size 26 color "#FFFFFF"
        # End hbox
    # End frame
    # ┌────────────────────────┤  Robot's Information  ├────────────────────────┐
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
    frame:
        background "#00000000"
        xalign 1.0
        yalign 0.32
        xsize 0.21
        ysize   0.04
        hbox:
            text "{b}Current bet: [p2['bet']]{/b}" size 26 color "#FFFFFF"
        # End hbox
    # End frame
    # ┌────────────────────────┤     Dealer Button     ├────────────────────────┐
    frame:
        if engine.dealer == 0:                                                                                                          # ═══► Display the dealer icon based on the current dealer
            background "#40404000"
            xalign 1.0
            yalign 0.85
            xsize 0.08
            ysize 0.2
            vbox:
                add "Dealer.png" size (100, 100)
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
    # ┌────────────────────────┤          Pot          ├────────────────────────┐
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.45
        xsize 0.21
        ysize 0.2
        hbox:
            text "{b}Pot: [state['pot']]{/b}   (round: [state['manche']])" size 26 color "#FFFFFF"
        # End hbox
    # End frame
    # ┌────────────────────────┤    Community Cards    ├────────────────────────┐
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
    # ┌────────────────────────┤   Information frame   ├────────────────────────┐
    frame:
        background "#40404000"
        xalign 1.0
        yalign 0.005
        xsize 0.21
        ysize 0.07
        vbox:
            grid 1 2:
                hbox:
                    text "[TEXT_INFOS_MEASSAGE_1]" size 22 color "#FFFFFF"
                # End hbox
                hbox:
                    text "[TEXT_INFOS_MEASSAGE_2]" size 22 color "#FFFFFF"
                # End hbox
            # End grid

        # End vbox
    # End frame
    # ┌────────────────────────┤      Debug frame      ├────────────────────────┐
    frame:
        xalign 0.0
        yalign 1.0
        xsize 650
        ysize 440
        background "#2228"
        padding (20, 10)
        vbox:
            if DEBUG_POKER:
                text "Round: [state['manche']]" size 22 color "#FFFFFF"
                text "Actual turn: [state['round']]" size 22 color "#FFFFFF"
                text "Blinds: [state.get('small_blind', 'N/A')] / [state.get('big_blind', 'N/A')]" size 22 color "#FFFFFF"
                text "Player 1: [p1['name']] - Clothes: [p1['clothes']] - Chips: [p1['chips']] - Bet: [p1['bet']]" size 22 color "#FFFFFF"
                text "Player 2: [p2['name']] - Clothes: [p2['clothes']] - Chips: [p2['chips']] - Bet: [p2['bet']]" size 22 color "#FFFFFF"
                text "Pot: [state['pot']]" size 22 color "#FFFFFF"
                text "Player 1 Cards: [p1['cards']]" size 22 color "#FFFFFF"
                if reveal_ai:
                    text "Player 2 Cards: [p2['cards']]" size 22 color "#FFFFFF"
                else:
                    text "Player 2 Cards: [p2['cards']] (hidden)" size 22 color "#FFFFFF"
                text "Community Cards: [state['community']]" size 22 color "#FFFFFF"
                text "Player 2 last action: [state['action_ai']]" size 22 color "#FFFFFF"
                text "Last bet: [state.get('last_bet', 'N/A')]" size 22 color "#FFFFFF"
                text "Last to act: [state.get('last_to_act', 'N/A')]" size 22 color "#FFFFFF"
                text "Actual bettor: [state['current_bettor']]" size 22 color "#FFFFFF"
                text "Betting round over: [state['betting_round_over']]" size 22 color "#FFFFFF"
                text "Round finished: [state['finished']]" size 22 color "#FFFFFF"
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
            xalign  0.842
            yalign  0.960
            xsize   0.060
            ysize   0.050
            textbutton ("FOLD") action Return(("fold",)):
                xanchor  0.5
                xpos    67
                ypos    -5
                text_style "STYLE_CHOICE_BUTTON_RED"
            # End textbutton
        # End frame
        # ┌────────────────────────┤     CHECK or CALL     ├────────────────────────┐
        frame:
            xalign  0.914
            yalign  0.960
            xsize   0.060
            ysize   0.050
            if engine.last_bet == p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                textbutton ("CHECK") action Return(("check",)):
                    xanchor 0.5
                    xpos 67
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            # End if
            if engine.last_bet > p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                textbutton ("CALL") action Return(("call", engine.last_bet - p1['bet'])):
                    xanchor 0.5
                    xpos 66
                    ypos -5
                    text_style "STYLE_CHOICE_BUTTON_ORANGE"
                # End textbutton
            # End if
        # End frame
        # ┌────────────────────────┤      BET or RAISE     ├────────────────────────┐
        if engine.current_raises < engine.max_raises_per_round:
#            if (engine.last_bet == p1['bet'] and p1['bet'] == 0) and (p1['chips'] > 0 or p1['clothes'] > 1):
            if engine.last_bet == p1['bet'] and (p1['chips'] > 0 or p1['clothes'] > 1):
                frame:
                    xalign  0.986
                    yalign  0.960
                    xsize   0.060
                    ysize   0.050
                    textbutton ("BET") action Return(("bet", engine.big_blind)):
                        xanchor 0.5
                        xpos 66
                        ypos -5
                        text_style "STYLE_CHOICE_BUTTON_ORANGE"
                    # End textbutton
                # End frame
            # End if
            if engine.last_bet > p1['bet'] and (p1['chips'] > (engine.last_bet - p1['bet'] + 10) or p1['clothes'] > 1):
                frame:
                    xalign  0.986
                    yalign  0.960
                    xsize   0.060
                    ysize   0.050
                    textbutton ("RAISE") action Return(("raise", engine.last_bet + engine.big_blind)):
                        xanchor 0.5
                        xpos 66
                        ypos -5
                        text_style "STYLE_CHOICE_BUTTON_ORANGE"
                    # End textbutton
                # End frame
            # End if
        # End if
    elif new_game:
        # ┌────────────────────────┤      Main Frame      ├─────────────────────────┐
        frame:
            background "#404040a0"
            xalign 1.0
            yalign 0.5
            xsize 0.22
            ysize 1.0
        # End frame
        # ┌────────────────────────┤       NEW GAME        ├────────────────────────┐
        frame:
            xalign  0.876
            yalign  0.960
            xsize   0.088
            ysize   0.050
            textbutton ("NEW GAME") action Return("continue",):
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
            textbutton ("QUIT") action Return("quit",):
                xanchor 0.5
                xpos  100
                ypos -5
                text_style "STYLE_CHOICE_BUTTON_RED"
            # End textbutton
        # End frame
    # End if
# End screen

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Global Text Styles                                                         ──
# ╰─────────────────────────────────────────────────────────────────────────────
#    ╰────────────────────────────────────────────────────────────────────────────
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