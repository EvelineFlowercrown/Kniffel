import os


def pause_menu():
    print("\n--- PAUSEMENÜ ---")
    print("1 - Spiel fortsetzen")
    print("2 - Spiel beenden")
    choice = input("Auswahl: ")
    if choice == "2":
        raise GameExit()


def get_input(prompt: str) -> str:
    value = input(prompt)
    if value.lower() in ("m", "menu", "q"):
        pause_menu()
    return value


def get_integer_input(text):
    while True:
        try:
            return int(get_input(text))
        except ValueError:
            print("bitte gib eine ganze Zahl ein")


def clear():
    os.system('cls')


def get_integer_input_upto(text,maxInput):
    inputNumber = None
    while inputNumber is None:
        inputNumber = get_integer_input(text)
        if inputNumber > maxInput or inputNumber <= -1:
            print(f"{inputNumber} ist ungültig. wähle aus 0 -", maxInput)
            inputNumber = None
    return inputNumber


class GameExit(Exception):
    pass
