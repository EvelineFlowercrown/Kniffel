def get_integer_input(text):
    zahl = None
    while not zahl:
        try:
            return int(input(text))
        except:
            print("bitte gib eine ganze zahl ein")