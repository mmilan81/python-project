import random

profondita = random.randint(1, 100)
tentativi = 0
scavo = 0

while scavo != profondita:
    scavo = int(input("A che profondità scavi? (1-100): "))
    tentativi = tentativi + 1
    if scavo < profondita:
        print("Solo terra... scava più in giù")
    elif scavo > profondita:
        print("Troppo profondo, attento alla lava!")

print("DIAMANTE trovato in", tentativi, "tentativi!")
