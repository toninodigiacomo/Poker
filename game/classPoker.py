import random

# ╭─────────────────────────────────────────────────────────────────────────────
# │  Card Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class Card:
    # ► Représente une carte à jouer avec une valeur (rank) et une couleur (suit).
    def __init__(self, rank, suit):
        self.rank = rank                                                                                                    # ═══► Ex: "2", "3", ..., "T", "J", "Q", "K", "A"
        self.suit = suit                                                                                                    # ═══► Ex: "H" (Hearts), "D" (Diamonds), "C" (Clubs), "S" (Spades)
    # End def
    def __repr__(self):
        # ► Représentation pour le débogage.
        return f"Card('{self.rank}', '{self.suit}')"
    # End def
    def __str__(self):
        # ► Représentation textuelle de la carte (ex: "AH" pour As de Cœur).
        return f"{self.rank}{self.suit}"
    # End def
    def get_value(self):
        # ► Retourne la valeur numérique de la carte pour le classement des mains.
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
            return 14                                                                                                       # ═══► As peut être 1 ou 14 selon la main
        return 0                                                                                                            # ═══► Valeur par défaut si non reconnue
    # End def
    def get_image_name(self):
        # ► Retourne le nom du fichier image pour Ren'Py.
        # ► Exemple: 'AH.png' pour l'As de Coeur.
        return f"{self.rank}{self.suit}.png"
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Card Deck Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class Deck:
    # ► Gère le paquet de 52 cartes (mélange, distribution.
    def __init__(self):
        self.cards = []
        self.reset()
    # End def
    def reset(self):
        # ► Réinitialise le paquet avec 52 cartes et les mélange.
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'C', 'S']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()
    # End def
    def shuffle(self):
        # ► Mélange les cartes du paquet.
        random.shuffle(self.cards)
    # End def
    def deal_card(self):
        # ► Distribue une carte du dessus du paquet.
        if not self.cards:
            print("Le paquet est vide. Réinitialisation.")
            self.reset()                                                                                                    # ═══► Optionnel: reinitialiser si le paquet est vide, ou lever une erreur
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
    # ► Classe de base pour tous les participants au jeu.
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Player Class Definition (inherits from Player)
# ╰─────────────────────────────────────────────────────────────────────────────
class HumanPlayer(Player):
    # ► Représente un joueur de poker avec ses jetons, sa main et son statut.
    def __init__(self, name, initial_chips, is_human=True):
        super().__init__(name, is_human)
        self.chips          = initial_chips                                                                                 # ═══► Jetons actuels du joueur
        self.hand           = []                                                                                            # ═══► Cartes privées du joueur
        self.current_bet    = 0                                                                                             # ═══► Montant misé par le joueur dans le tour de mise actuel
        self.has_folded     = False                                                                                         # ═══► Vrai si le joueur a foldé cette main
        self.is_all_in      = False                                                                                         # ═══► Vrai si le joueur a mis tous ses jetons
        self.is_dealer      = False                                                                                         # ═══► Vrai si le joueur a le bouton du dealer
        self.is_small_blind = False                                                                                         # ═══► Vrai si le joueur a la petite blinde
        self.is_big_blind   = False                                                                                         # ═══► Vrai si le joueur a la grosse blinde
        self.bet_in_hand = 0                                                                                                # ═══► Total misé par le joueur sur toute la main (pour les pots secondaires)
    # End def
    def add_chips(self, amount):
        # ► Ajoute des jetons au joueur.
        self.chips      += amount
        print(f"{self.name} gagne {amount} jetons. Total: {self.chips}")
    # End def
    def remove_chips(self, amount):
        # ► Retire des jetons du joueur. Gère le cas du all-in.
        # ► Retourne le montant réellement payé.
        if self.chips   >= amount:
            self.chips  -= amount
            return amount
        else:                                                                                                               # ═══► Ne peut pas payer entièrement, va all-in
            all_in_amount   = self.chips
            self.chips      = 0
            self.is_all_in  = True
            return all_in_amount
        # End if
    # End def
    def reset_hand(self):
        # ► Réinitialise le statut du joueur pour une nouvelle main.
        self.hand           = []
        self.current_bet    = 0
        self.has_folded     = False
        self.is_all_in      = False
        #  ► Les statuts de dealer/blinds sont gérés par la classe PokerGame à chaque main
    # End def
    def can_check(self, current_bet_to_match):
        # ► Vérifie si le joueur peut 'check' (pas de mise à égaler).
        return current_bet_to_match == self.current_bet
    # End def
    def can_call(self, current_bet_to_match):
        # ► Vérifie si le joueur peut 'call' (doit égaler une mise et a des jetons).
        return current_bet_to_match > self.current_bet and self.chips > 0
    # End def
    def get_call_amount(self, current_bet_to_match):
        # ► Calcule le montant nécessaire pour 'call'.
        return current_bet_to_match - self.current_bet
    # End def
    def can_bet(self, min_bet=0):
        # ► Vérifie si le joueur peut 'bet' (personne n'a misé et il a des jetons).
        return self.chips > 0 and self.current_bet == 0                                                                     # ═══► Peut miser si personne n'a misé et qu'il a des jetons
    # End def
    def can_raise(self, current_bet_to_match, min_raise_amount):
        # ► Vérifie si le joueur peut 'raise' (quelqu'un a misé, il a des jetons et peut sur-relancer).
        # ► Le joueur doit pouvoir égaler la mise actuelle et ajouter au moins le minimum de relance.
        amount_to_match = current_bet_to_match - self.current_bet
        return self.chips >= (amount_to_match + min_raise_amount) and (amount_to_match + min_raise_amount) > 0              # ═══► Doit avoir des jetons pour payer le call et le raise
    # End def
    def perform_action(self, action_type, amount_needed=0, raise_amount=0):
        # ► ffectue l'action choisie par le joueur.
        # ► Retourne le montant total misé par le joueur dans cette action.
        print(f"{self.name} ({self.chips} chips) performs {action_type}.")
        bet_made_this_action = 0
        if action_type == "fold":
            self.has_folded = True
            print(f"{self.name} folds.")
        elif action_type == "check":
            if self.can_check(amount_needed):
                print(f"{self.name} checks.")
            else:
                print(f"ATTENTION: {self.name} a essayé de 'check' mais ne pouvait pas (mise à égaler={amount_needed}, mise actuelle={self.current_bet}).")
            # End if
        elif action_type == "call":
            call_amount = self.get_call_amount(amount_needed)
            actual_paid = self.remove_chips(call_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} calls {actual_paid} (mise totale dans le tour: {self.current_bet}). Jetons restants: {self.chips}")
        elif action_type == "bet":
            bet_amount = amount_needed # Pour un bet initial, amount_needed est le montant du bet
            actual_paid = self.remove_chips(bet_amount)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} bets {actual_paid} (mise totale dans le tour: {self.current_bet}). Jetons restants: {self.chips}")
        elif action_type == "raise":
            amount_to_call = amount_needed - self.current_bet                                                               # ═══► Le montant total de la mise après le raise
            total_raise_amount_needed = amount_to_call + raise_amount
            actual_paid = self.remove_chips(total_raise_amount_needed)
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            print(f"{self.name} raises to {self.current_bet} (a ajouté {actual_paid}). Jetons restants: {self.chips}")
        elif action_type == "all_in":
            if self.is_all_in:                                                                                              # ═══► Si le joueur est déjà all-in, il ne mise rien de plus
                print(f"{self.name} est déjà ALL-IN.")
                return 0
            # End if
            actual_paid = self.remove_chips(self.chips)                                                                     # ═══► Mise tous les jetons restants
            self.current_bet += actual_paid
            self.bet_in_hand += actual_paid
            bet_made_this_action = actual_paid
            self.is_all_in = True
            print(f"{self.name} goes ALL-IN for {actual_paid} (mise totale dans le tour: {self.current_bet}).")
        else:
            print(f"Action non reconnue: {action_type}")
        # End if
        return bet_made_this_action
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Robot Class Definition (inherits from Player)
# ╰─────────────────────────────────────────────────────────────────────────────
class RobotPlayer(HumanPlayer):
    # ► Représente un joueur d'IA avec une logique de décision.
    def __init__(self, name, initial_chips, aggression_level=3):
        super().__init__(name, initial_chips, is_human=False)
        self.aggression_level = aggression_level                                                                            # ═══► 1 (passif) à 5 (très agressif)
    # End def
    def decide_action(self, current_bet_to_match, pot_size, num_active_players, community_cards, small_blind_val, big_blind_val):
        # ► Décide de l'action de l'IA (fold, check, call, bet, raise, all-in).
        # ► Ceci est une LOGIQUE D'IA TRÈS SIMPLIFIÉE et un PLACEHOLDER.
        # ► Une IA de poker réaliste est extrêmement complexe et nécessite :
        #    - Une évaluation précise de la force de la main (votre propre main + cartes communes).
        #    - L'analyse des cotes du pot (pot odds).
        #    - La lecture des adversaires (patterns de mise, historique).
        #    - La position à la table.
        #    - La phase du jeu (pre-flop, flop, turn, river).
        #    - La gestion de la taille du stack.

        # ► Calcule la force de la main (PLACEHOLDER: implémentez un vrai évaluateur !)
        combined_cards = self.hand + community_cards
        hand_rank, hand_description = get_hand_rank_and_description(combined_cards)
        # ► hand_rank: un chiffre pour la force (ex: 1=high card, 2=pair, ..., 9=straight flush)
        # ► hand_description: "Pair of Aces", "Flush", etc.

        # ► Adaptée à la force de la main (hand_rank) et au niveau d'agressivité
        # ► hand_strength_score est une valeur entre 0 et 1 (0 = faible, 1 = très forte)
        hand_strength_score = hand_rank / 9.0                                                                               # ═══► Max 9 types de mains principales

        print(f"Robot {self.name}: Hand Strength Score = {hand_strength_score:.2f} ({hand_description})")

        amount_to_call   = current_bet_to_match - self.current_bet                                                          # ═══► Calculer les montants potentiels
        min_bet_amount   = big_blind_val * 2                                                                                # ═══► Standard initial bet (2x BB)
        min_raise_amount = big_blind_val * 2                                                                                # ═══► Standard minimum raise amount

        # ► Logique de décision
        if self.chips <= 0:
            return {"action": "check"}                                                                                      # ═══► Si all-in ou 0 chips, ne peut rien faire d'autre
        # End if
        if current_bet_to_match == self.current_bet:                                                                        # ═══► Pas de mise à égaler (peut Check ou Bet)
            if hand_strength_score > 0.6 + (self.aggression_level * 0.05):                                                  # ═══► Main forte ou agressive
                bet_amount = min(self.chips, big_blind_val)                                                                 # ═══► Tente de miser plus fort si agressif
                if bet_amount > 0:
                    return {"action": "bet", "amount": bet_amount}
                else:                                                                                                       # ═══► Pas assez de jetons pour un bet significatif, donc check
                    return {"action": "check"}
                # End if
            else:                                                                                                           # ═══► Main faible, ou pas agressive
                return {"action": "check"}
            # End if
        else:                                                                                                               # ═══► Il y a une mise à égaler (peut Fold, Call ou Raise)
            if self.chips < amount_to_call:                                                                                 # ═══► Pas assez de jetons pour 'call'
                if self.chips > 0:                                                                                          # ═══► Peut aller all-in
                    return {"action": "all_in"}
                else:
                    return {"action": "fold"}                                                                               # ═══► Aucun jeton, doit fold (ou est déjà all-in)
                # End if
            # End if
            # ► Calcul de la probabilité de raise/call/fold basée sur la force et l'agressivité
            fold_threshold = 0.3 - (self.aggression_level * 0.05)                                                           # ═══► Plus agressif = moins enclin à fold
            call_threshold = 0.5 + (self.aggression_level * 0.02)                                                           # ═══► Plus agressif = plus enclin à call/raise
            if hand_strength_score < fold_threshold:
                return {"action": "fold"}
            elif hand_strength_score < call_threshold or not self.can_raise(current_bet_to_match, min_raise_amount):
                return {"action": "call", "amount_needed": current_bet_to_match}                                            # ═══► Assez fort pour call, ou ne peut pas raise
            else:                                                                                                           # ═══► Assez fort pour raise et peut raise
                raise_by_amount = min(self.chips - amount_to_call, big_blind_val)
                if raise_by_amount < big_blind_val and self.chips - amount_to_call > 0:                                     # ═══► Si pas assez pour un vrai raise, va all-in (et a des jetons)
                    return {"action": "all_in"}
                elif raise_by_amount < big_blind_val and self.chips - amount_to_call <= 0:                                  # ═══► Si pas de jetons à relancer
                    return {"action": "call", "amount_needed": current_bet_to_match}                                        # ═══► Alors call
                else:                                                                                                       # ═══► Peut relancer de la Big Blind
                    return {"action": "raise", "amount_needed": current_bet_to_match, "raise_by": raise_by_amount}
            # End if
        # End if
    # End def
# End class
# ╭─────────────────────────────────────────────────────────────────────────────
# │  Poker Game Class Definition
# ╰─────────────────────────────────────────────────────────────────────────────
class PokerGame:
    # ► Gère l'état global du jeu de poker, les joueurs, les tours, le pot et la distribution.
    # ► Constantes du jeu (peuvent être configurées)
    SMALL_BLIND_VAL     = 5
    BIG_BLIND_VAL       = 10
    INITIAL_CHIPS       = 1000

    # ► États du jeu pour le flux logique et l'affichage
    GAME_STATE_PREFLOP  = "preflop"
    GAME_STATE_FLOP     = "flop"
    GAME_STATE_TURN     = "turn"
    GAME_STATE_RIVER    = "river"
    GAME_STATE_SHOWDOWN = "showdown"
    GAME_STATE_END_HAND = "end_hand"

    def __init__(self, human_player_name="Player", num_ai_players=1):                                                       # ═══► 1 IA par défaut
        self.deck = Deck()
        self.players = []
        self.players.append(PokerPlayer(human_player_name, self.INITIAL_CHIPS, is_human=True))                              # ═══► Ajouter le joueur humain
        for i in range(num_ai_players):                                                                                     # ═══► Ajouter les joueurs AI
            self.players.append(AIPlayer(f"AI Player {i+1}", self.INITIAL_CHIPS, aggression_level=random.randint(1, 5)))
        # End for
        self.dealer_index = random.randint(0, len(self.players) - 1)                                                        # ═══► Position initiale du dealer
        self.community_cards        = []
        self.pot                    = 0
        self.current_highest_bet    = 0
        self.current_player_index   = -1                                                                                    # ═══► Index du joueur dont c'est le tour
        self.game_state             = None                                                                                  # ═══► État actuel du jeu (preflop, flop, etc.)
        self.last_raiser_index      = -1                                                                                    # ═══► Index du dernier joueur à avoir fait une action agressive (bet/raise)
        self.num_hands_played       = 0                                                                                     # ═══► Compteur de mains jouées

        print("Jeu de Poker initialisé.")
