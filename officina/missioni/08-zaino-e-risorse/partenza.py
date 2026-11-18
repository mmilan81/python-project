zaino = ["spada", "pala", "torcia"]
zaino.append("pane")

print("Nel tuo zaino ci sono", len(zaino), "oggetti:")
for oggetto in zaino:
    print("-", oggetto)

if "spada" in zaino:
    print("Sei pronto a combattere!")

risorse = {"legno": 64, "ferro": 12, "diamanti": 3}
risorse["diamanti"] = risorse["diamanti"] + 2

print("Le tue risorse:")
for nome in risorse:
    print(nome, ":", risorse[nome])
