import easygui as gui


def ask_yes_no(question, title="Game"):
    """Задає питання з відповіддю (y/n)."""
    return gui.ynbox(question + "?", title)


def ask_number(question, low, high, title="Game"):
    """Просить ввести число із заданого діапазону."""
    return gui.integerbox(
        question, title, default=int((low + high) / 2), lowerbound=low, upperbound=high
    )


if __name__ == "__main__":
    gui.msgbox("Ви запустили модуль games, " "а не імпортували його (import games).")
    gui.msgbox("Тестування модуля.")
    answer = ask_yes_no("Продовжуємо тестування")
    gui.msgbox("Функція ask_yes_no повернула " + str(answer))
    answer = ask_number("Введіть ціле число від 1 до 10:", 1, 10)
    gui.msgbox("Функція ask_number повернула " + str(answer))