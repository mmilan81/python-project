profondita = 42
scavo = int(input("A che profondità scavi? (1-100): "))

while scavo != profondita:
    tentativi = tentativi + 1
    if scavo < profondita:
        print("Solo terra... scava più in giù")
    else:
        print("Troppo profondo, attento alla lava!")

print("DIAMANTE trovato in", tentativi, "tentativi!")
