import winsound

nota = input("Che nota vuoi suonare? (do, re, mi, fa, sol, la, si): ")
ottava = input("Alta, normale o bassa? ")

if nota == "do":
    frequenza = 262
elif nota == "re":
    frequenza = 294
elif nota == "mi":
    frequenza = 330
elif nota == "fa":
    frequenza = 349
elif nota == "sol":
    frequenza = 392
elif nota == "la":
    frequenza = 440
elif nota == "si":
    frequenza = 494
else:
    frequenza = 0

if frequenza == 0:
    print("Non conosco questa nota")
else:
    if ottava == "alta":
        frequenza = frequenza * 2
    elif ottava == "bassa":
        frequenza = frequenza // 2
    print("Suono", nota, "a", frequenza, "Hz")
    winsound.Beep(frequenza, 500)
