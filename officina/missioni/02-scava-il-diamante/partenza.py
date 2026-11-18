import random

profondita = random.randint(1, 10)
scavo = int(input("A che profondità scavi? (1-10): "))

if scavo == profondita:
    print("DIAMANTE!")
elif scavo < profondita:
    print("Solo terra... scava più in giù")
else:
    print("Troppo profondo, attento alla lava!")
