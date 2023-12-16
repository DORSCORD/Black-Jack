import cards, games

MIN_BET = 1

class BJ_Card(cards.Positionable_Card):
    ACE_VALUE = 1
    
    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v
    
class BJ_Deck(cards.Deck):
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))
                

class BJ_Hand(cards.Hand):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        
    def __str__(self) -> str:
        rep = self.name  + ":\t" + super().__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep
    
    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None
        t = 0
        contains_ace = False
        for card in self.cards:
            t += card.value
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
        
        if contains_ace and  t <= 11:
            t += 10
        
        return t
    
    def is_busted(self) -> bool:
        return self.total > 21 
    

class BJ_Player(BJ_Hand):
    """Гравець у Блек-Джек"""

    def __init__(self, name, money):
        super().__init__(name)
        self.money = money
    
    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", братиме ще карти")
        return response == "y"
    
    def bust(self):
        print(f"{self.name} перебрав(-ла).")
        self.lose()
        
    def lose(self):
        print(f"{self.name} програв(-ла).")
        
    def win(self):
        self.money += 2 * self.bet_value
        print(f"{self.name} виграв(-ла).")
        
    def push(self):
        self.money += self.bet_value
        print(f"{self.name} зіграв(-ла) з дилером в нічию.")
    
    def bet(self, bet_value):
        if bet_value > self.money:
            return False
        self.bet_value = bet_value
        self.money -= self.bet_value
        return bet_value
    
    def escape(self):
        self.money += int(self.bet_value * 0.5)
        self.clear()
        print(f"{self.name} вийшов(ла) з гри зі збереженням половини ставки")

    def is_escaped(self):
        return len(self.cards) == 0
    
        
class BJ_Dealer(BJ_Hand):
    
    def is_hitting(self):
        return self.total < 17 
    
    def bust(self):
        print(f"{self.name} перебрав.")
        
    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()
        
        
class BJ_Game:
    
    def __init__(self, players):
        self.players: list[BJ_Player] = []
        for name, money in players.items():
            player = BJ_Player(name, money)
            self.players.append(player)
            
        self.dealer = BJ_Dealer("Дилер")

        self.deck = BJ_Deck()
        self.deck.add_new_deck()

    @property
    def still_playing(self):
        sp: list[BJ_Player] = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp
    
    def __additional_cards(self, player: BJ_Player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def __betting(self):
        for player in self.players.copy():
            if player.money < MIN_BET:
                self.players.remove(player)
                print(f"Гравець {player.name} видалення з капіталом {player.money}")
                continue
            bet_value = games.ask_number(
            f"Ваша ставка {player.name} ({MIN_BET} - {player.money}): ", 
            MIN_BET,
            player.money
            )
            player.bet(bet_value)
    
    def __escaping(self, player):
        answer = games.ask_yes_no(f"{player}, чи будете Ви грати?")
        if answer == "n":
            player.escaped()
            return True
        return False
                
    def play(self):
        self.__betting()
        if len(self.deck.cards) < (len(self.players) + 1) * 2:
            self.add_new_deck()

        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)
        for player in self.players:
            if not self.__escaping(player):
                self.__additional_cards(player)
        self.dealer.flip_first_card()
        if not self.still_playing:
            print(self.dealer)
        
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                for player in self.still_playing:
                    player.win()
            else:
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        
        for player in self.players:
            player.clear()
        self.dealer.clear()
        
def main():
    print("\t\tЛаскава просимо до гри Блек-Джек\n")

    players = {}
    number = games.ask_number("Скільки всього гравців (1-7): ", low=1, high=7)
    for i in range(number):
        name = input(f"Введіть ім'я гравця №{i+1}: ")
        money = games.ask_number(f"Введіть капітал гравця {name}: ", MIN_BET, MIN_BET * 100
        )
        players[name] = money
    
    print()
    
    game = BJ_Game(players)

    again =None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nБажання зіграти ще раз ")
    
main()