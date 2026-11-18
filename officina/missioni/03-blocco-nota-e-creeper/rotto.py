import winsound

# Il sibilo del creeper: dovrebbe salire sempre di più...
for frequenza in range(0, 1000, 100):
    winsound.Beep(frequenza, 150)
