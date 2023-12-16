import easygui as gui

import cards
import games


TITLE = "Блек Джек"
ICON = "black-jack.png"


class BJ_Card(cards.Positionable_Card):
    """Карта для гри в Блек-джек."""

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
    """Колода для гри в Блек-джек."""

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(cards.Hand):
    """Рука гравця в Блек-джек."""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super().__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # якщо value однієї з карт дорівнює None,
        # то і властивість в цілому дорівнює None
        for card in self.cards:
            if not card.value:
                return None

        # сумуємо очки, рахуючи кожен туз за 1 очко
        # визначаємо, чи є туз на руках у гравця
        t = 0
        contains_ace = False
        for card in self.cards:
            t += card.value
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # якщо на руках є туз і сума очок не перевищує 11,
        # будемо рахувати туз за 11 очок
        if contains_ace and t <= 11:
            # додати потрібно лише 10,
            # тому що одиниця вже увійшла до загальної суми
            t += 10

        return t

    def is_busted(self):
        return self.total > 21

    def show_message(self, message):
        gui.buttonbox(message, choices=["Ok"], images=self.card_images, title=TITLE)


class BJ_Player(BJ_Hand):
    """Гравець у Блек-джек."""

    def is_hitting(self):
        response = gui.buttonbox(
            f"{self.name}, братимете ще карти ({self.total}) ?",
            choices=["Yes", "No"],
            images=self.card_images,
        )
        return response == "Yes"

    def bust(self):
        self.show_message(self.name + " перебрав(ла).")

    def lose(self):
        self.show_message(self.name + " програв(ла).")

    def win(self):
        self.show_message(self.name + " виграв(ла).")

    def push(self):
        self.show_message(self.name + " зіграв(ла) з дилером внічию.")


class BJ_Dealer(BJ_Hand):
    """Дилер у Блек-джек."""

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        self.show_message(self.name + " перебрав.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game:
    """Гра Блек-джек."""

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Дилер")

        self.deck = BJ_Deck()
        self.deck.add_new_deck()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            if player.is_busted():
                player.bust()

    def play(self):
        # здача всім по дві карти
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()
        # перша з карт, зданих дилеру, перевертається
        self.dealer.show_message("Починаємо гру, Дилер оримав такі карти:")

        # роздавання додаткових карт гравцям
        for player in self.players:
            self.__additional_cards(player)
        # перша карта дилера розкривається
        self.dealer.flip_first_card()

        if not self.still_playing:
            # всі гравці перебрали,
            # покажемо лише "руку" дилера
            self.dealer.show_message(self.dealer.name + " переміг!")
        else:
            # роздача додаткових карт дилеру
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # виграють усі, хто ще залишився у грі
                for player in self.still_playing:
                    player.win()
            else:
                self.dealer.show_message(
                    f"{self.dealer.name} набрав додаткові карти {self.dealer.total}."
                )
                # порівнюємо суми очок у дилера
                # та у гравців, що залишилися у грі
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # видалення всіх карт
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    gui.msgbox("Ласкаво просимо до гри Блек-джек!", TITLE, image=ICON)

    names = []
    number = games.ask_number("Скільки всього гравців? (1 - 7): ", low=1, high=7)
    if number is None:
        exit()
    fields = ["Гравець " + str(i + 1) for i in range(number)]
    names = gui.multenterbox(
        "Введіть імена гравців", TITLE, fields=fields, values=fields
    )
    if names is None:
        exit()
    game = BJ_Game(names)

    again = True
    while again:
        game.play()
        again = games.ask_yes_no("Бажаєте зіграти ще раз", TITLE)


main()