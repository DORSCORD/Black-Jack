import easygui as gui

def ask_yes_no(question, title = "Game"):
    return gui.ynbox(question + "? ", title)

def ask_number(question, low, high, title= "Game"):
    response = 0
    while response not in range(low, high+1):
        response = int(input(question))
    return gui.integerbox(question, title, default=int((low+high)/2), lowerbound=low, upperbound = high)

if __name__ == "__main__":
    gui.msgbox("Ви запустили модуль games, а не імпортували його")
    gui.msgbox("Тестування модуля ...")
    gui.msgbox(f"Функція ask_yes_no повернула: {ask_yes_no('Продовжуємо тестування ...')}")
    gui.msgbox(f"Функція ask_number повернула: {ask_number('Введіть число від 1 до 10: ', 1, 10)}")