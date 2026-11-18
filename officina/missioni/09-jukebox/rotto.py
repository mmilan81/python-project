import winsound

def suona(frequenza, durata):
    winsound.Beep(frequenza, durata)

melodia([262, 294, 330], 300)

def melodia(note, durata):
    for frequenza in note:
        suona(frequenza)

def stack_pieni(blocchi):
    blocchi // 64

print("200 blocchi riempiono", stack_pieni(200), "stack")
