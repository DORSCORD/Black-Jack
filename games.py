
def ask_yes_no(question: str):
    response = ""
    while response.lower() not in ("y", "n"):
        response = input(question + "y/n? ".lower())
    return response

def ask_number(question: str, low: int, high: int):
    response = 0
    while response not in range(low, high+1):
        response = int(input(question))
    return response

if __name__ == "__main__":
    print("Ви запустили модуль games, а не імпортували його")
    print("Тестування модуля ...")
    print(f"Функція ask_yes_no повернула: {ask_yes_no('Продовжуємо тестування ...')}")
    print(f"Функція ask_number повернула: {ask_number('Введіть число від 1 до 10: ', 1, 10)}")