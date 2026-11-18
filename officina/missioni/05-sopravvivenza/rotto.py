vita = 20
fame = 10

danno = int(input("Quanti punti di danno ti fa il creeper? "))
vita = Vita - danno

cibo = input("Mangi qualcosa? (si/no): ")
if cibo == "si"
    fame = fame + 6

print("Vita:", vita)
print("Fame:", fame)

if vita <= 0:
    print("Sei morto! Game over")
elif vita <= 12:
    print("Stai così così")
elif vita <= 5:
    print("Pericolo! Mangia e riposa")
else:
    print("Stai benissimo")
