class Card:
    """Одна гральна карта"""
    RANKS = [
        "T", "2", "3", "4", "5", 
        "6", "7", "8","9", 
        "10", "В", "Д", "К"
    ]
    SUITS = [u'\u2660', u'\u2663', u'\u2665', u'\u2666']
    
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
        
    def __str__(self) -> str:
        return self.rank + self.suit
    
class UnPrintableCard(Card):
    """Карта, номінал якої не можна надрукувати"""
    def __str__(self) -> str:
        return "<Не можна надрукувати>"
    
class Positionable_Card(Card):
    """Карта, яку можна перегортати"""
    def __init__(self, rank, suit, face_up = True) -> None:
        super().__init__(rank, suit)
        self.is_face_up = face_up
    
    def __str__(self) -> str:
        if self.is_face_up:
            return super().__str__()
        else:
            return "XX"
        
    def flip(self):
        self.is_face_up = not self.is_face_up
        
    
class Hand:
    """Рука: Набір карт на руках для кожного гравця """
    def __init__(self) -> None:
        self.cards = []
        
    def __str__(self) -> str:
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<пусто>"
        return rep
    
    def clear(self):
        # self.cards.clear()
        self.cards = []
        
    def add(self, card):
        self.cards.append(card)
        
    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)
        

class Deck(Hand):
    """Колода гральнх карт"""
    
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))
                
    def shuffle(self):
        from random import shuffle as shf
        shf(self.cards)
        
    def add_new_deck(self):
        self.populate()
        self.shuffle()
        
    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if not self.cards:
                    self.add_new_deck()
                top_card = self.cards[0]
                self.give(top_card,  hand)
                
if __name__ == "__main__":
    print("Ви запустили модуль cards, а не імпортували його.")
    print("Тестування модуля")
    card1 = Card("T", Card.SUITS[0])
    card2 = UnPrintableCard("T", Card.SUITS[1])
    card3 = Positionable_Card("T", Card.SUITS[2])
    print(f"Об'єкт Card: {card1}")
    print(f"Об'єкт UnPrintableCard: {card2}")
    print(f"Об'єкт Positionable_Card: {card3}")
    card3.flip()
    print(f"Перевернутий об'єкт Positionable_Card {card3}")
    deck1 = Deck()
    print(f"Створено нову колоду: {deck1}")
    deck1.populate()
    print(f"У колоді з'явилися карти:\n{deck1}", sep = "\n")
    deck1.shuffle()
    print(f"Перемішана колода:\n{deck1}", sep="\n")
    hand1 = Hand()
    hand2 = Hand()
    deck1.deal(hands=(hand1, hand2), per_hand=5)
    print("Роздано по 5 карт")
    print(f"Рука1: {hand1}")
    print(f"Рука2: {hand2}")
    print(f"Залишилось в колоді: {deck1}", sep = "\n")
    deck1.clear()
    print(f"Колода очищена {deck1}")