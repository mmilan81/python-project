import winsound

def suona(frequenza, durata):
    winsound.Beep(frequenza, durata)

def melodia(note, durata):
    for frequenza in note:
        suona(frequenza, durata)

def stack_pieni(blocchi):
    return blocchi // 64

DO = 262
RE = 294
MI = 330
FA = 349

melodia([DO, RE, MI, FA, MI, RE, DO], 300)

print("200 blocchi riempiono", stack_pieni(200), "stack")
