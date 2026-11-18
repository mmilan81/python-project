legno = input("Quanti blocchi di legno hai? ")
ferro = int(input("Quanti lingotti di ferro hai? "))

bastoni = legno * 2

if ferro >= 3 and bastoni >= 2:
    print("Puoi costruire un piccone di ferro!")
elif ferro >= 3 and bastoni >= 2:
    print("Ti manca ancora qualcosa...")
else:
    print("Non hai quasi niente: vai a raccogliere risorse!")
