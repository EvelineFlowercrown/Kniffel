import os


def get_integer_input(text):
    zahl = None
    while not zahl:
        try:
            return int(input(text))
        except:
            print("bitte gib eine ganze zahl ein")


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