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
