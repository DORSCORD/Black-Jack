import easygui as gui


class Card:
    """Одна гральна карта."""

    RANKS = ["Т", "2", "3", "4", "5", "6", "7", "8", "9", "10", "В", "Д", "K"]
    SUITS = ["\u2660", "\u2663", "\u2665", "\u2666"]  # ♠ ♣ ♥ ♦
    SUIT_LETTERS = "schd"

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep


class Unprintable_Card(Card):
    """Карта, номінал та масть якої не можуть бути виведені на екран."""

    def __str__(self):
        return "<не можна надрукувати>"


class Positionable_Card(Card):
    """Карта, яку можна покласти обличчям чи сорочкою нагору."""

    def __init__(self, rank, suit, face_up=True):
        super().__init__(rank, suit)
        self.is_face_up = face_up

    def __str__(self):
        if self.is_face_up:
            rep = super().__str__()
        else:
            rep = "XX"
        return rep

    def flip(self):
        self.is_face_up = not self.is_face_up

    @property
    def image_filename(self):
        if not self.is_face_up:
            filename = "back.png"
        else:
            suit_name = self.SUIT_LETTERS[self.SUITS.index(self.suit)]
            rank_name = self.RANKS.index(self.rank) + 1
            filename = f"{suit_name}{rank_name:0>2}.png"
        return "assets/" + filename


class Hand:
    """Рука: набір карт на руках одного гравця."""

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<пусто>"
        return rep

    @property
    def card_images(self):
        return [card.image_filename for card in self.cards]

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)


class Deck(Hand):
    """Колода гральних карт."""

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):
        import random

        random.shuffle(self.cards)

    def add_new_deck(self):
        self.populate()
        self.shuffle()

    def deal(self, hands, per_hand=1):
        for rounds in range(per_hand):
            for hand in hands:
                # Перевірка на наявність карт у колоді
                if not self.cards:
                    self.add_new_deck()
                top_card = self.cards[0]
                self.give(top_card, hand)


if __name__ == "__main__":
    gui.msgbox("Ви запустили модуль cards, " "а не імпортували його (import cards).")
    gui.msgbox("Тестування модуля.\n")

    card1 = Card("Т", Card.SUITS[0])
    card2 = Unprintable_Card("Т", Card.SUITS[1])
    card3 = Positionable_Card("Т", Card.SUITS[2])
    gui.msgbox("Об'єкт Card: " + str(card1))
    gui.msgbox("Об'єкт Unprintable_Card: " + str(card2))
    gui.msgbox("Об'єкт Positionable_Card: " + str(card3))
    card3.flip()
    gui.msgbox("Перевертаю об'єкт Positionable_Card: " + str(card3))

    deck1 = Deck()
    gui.msgbox("\nСтворено нову колоду: " + str(deck1))
    deck1.populate()
    gui.msgbox("У колоді з'явилися карти: " + str(deck1))
    deck1.shuffle()
    gui.msgbox("Колода перемішана: " + str(deck1))

    hand1 = Hand()
    hand2 = Hand()
    deck1.deal(hands=(hand1, hand2), per_hand=5)
    gui.msgbox("Роздано по 5 карт.")
    gui.msgbox("Рука1: " + str(hand1))
    gui.msgbox("Рука2: " + str(hand2))
    gui.msgbox("Залишилось у колоді: " + str(deck1))
    deck1.clear()
    gui.msgbox("Колода очищена: " + str(deck1))