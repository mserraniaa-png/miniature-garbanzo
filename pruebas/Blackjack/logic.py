import random

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self._get_value()

    def _get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.is_busted = False

    def add_card(self, card):
        self.cards.append(card)
        self.calculate_value()

    def calculate_value(self):
        val = 0
        aces = 0
        for card in self.cards:
            val += card.value
            if card.rank == 'A':
                aces += 1
        
        # Adjust for Aces
        while val > 21 and aces > 0:
            val -= 10
            aces -= 1
        
        self.value = val
        self.is_busted = val > 21

    def __repr__(self):
        return f"{self.cards} (Value: {self.value})"

class Participant:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.is_standing = False

    def reset(self):
        self.hand = Hand()
        self.is_standing = False

    @property
    def score(self):
        return self.hand.value

    @property
    def busted(self):
        return self.hand.is_busted

class Player(Participant):
    def __init__(self, name, balance=100, is_bot=True):
        super().__init__(name)
        self.balance = balance
        self.current_bet = 0
        self.is_bot = is_bot

    def place_bet(self, amount):
        if amount <= self.balance:
            self.current_bet = amount
            self.balance -= amount
            return True
        return False

    def win(self, multiplier=2):
        self.balance += int(self.current_bet * multiplier)
        self.current_bet = 0

    def push(self):
        self.balance += self.current_bet
        self.current_bet = 0

    def lose(self):
        self.current_bet = 0
