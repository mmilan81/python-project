# Dispensa di Python: le basi

*Per le Missioni e le Sfide di Officina*

**Com’è fatto questo libro**

- **Parte 1** (capitoli da 1 a 16): le basi, dalla prima riga di codice agli errori.
- **Approfondimento**: variabili e condizioni, per le Missioni 4, 5 e 6.
- **Parte 2** (capitoli da 17 a 23): `while`, liste, dizionari e funzioni, per le Missioni 7, 8 e 9.
- **Parte 3**: come ragionare per scrivere un programma da solo, per le Sfide.
- **Parte 4**: esempi pratici, un programma per ogni argomento.
- **Parte 5**: tre piccoli progetti completi che mettono insieme tutto.

Per imparare davvero, riscrivi a mano gli esempi, eseguili e poi cambiali per vedere cosa succede. Copiare non basta: sono le dita che imparano.

Questa dispensa non va studiata a memoria. Tienila aperta mentre lavori alle missioni e consultala quando un concetto non ti è chiaro. La prima volta che usi una cosa ti sembrerà strana, la quinta ti verrà naturale. Prova sempre gli esempi in Officina: cambiare un numero e vedere cosa succede insegna più di qualsiasi spiegazione.

## 1. print: far parlare il programma

`print` scrive qualcosa sullo schermo.

```python
print("Ciao, Steve!")
print("Vita:", 20)
```

Sullo schermo compare:

```
Ciao, Steve!
Vita: 20
```

- Il testo va tra virgolette, doppie o singole, purché uguali all’inizio e alla fine.
- Le virgolette non compaiono sullo schermo: servono a Python per capire dove il testo inizia e dove finisce.
- Se separi più cose con la virgola, Python le scrive una accanto all’altra con uno spazio in mezzo.

## 2. Commenti

Tutto quello che scrivi dopo un `#` viene ignorato da Python. Serve a spiegare il codice a chi lo legge, cioè a te tra una settimana.

```python
vita = 20   # i punti vita iniziali
```

## 3. Variabili: scatole con un nome

Una variabile è una scatola con un’etichetta: dentro ci metti un valore e lo ritrovi usando il nome.

```python
nome = "Steve"
vita = 20
vita = 18       # la scatola ora contiene 18
print(nome, vita)
```

- Il simbolo `=` non significa «uguale», significa «metti dentro»: a sinistra il nome della scatola, a destra il valore.
- Un nome può contenere lettere, numeri e il trattino basso `_`. Non può iniziare con un numero né contenere spazi.
- Maiuscole e minuscole contano: `Vita` e `vita` sono due variabili diverse.
- Scegli nomi che spiegano cosa c’è dentro: `blocchi_di_terra` è meglio di `x`.
- Una variabile va creata prima di usarla, altrimenti Python risponde con un `NameError`.
- `print(nome)` scrive il contenuto della variabile, `print("nome")` scrive la parola nome.

## 4. I tipi di dati

Ogni valore ha un tipo, e il tipo decide cosa ci puoi fare.

- `str` (stringa): testo, sempre tra virgolette. Esempi: `"Steve"`, `"200"`.
- `int`: numero intero. Esempi: `20`, `-3`.
- `float`: numero decimale, scritto con il punto e non con la virgola. Esempio: `3.5`.
- `bool`: vero o falso, cioè `True` o `False`, con la maiuscola e senza virgolette.

Con `type()` puoi chiedere a Python di che tipo è un valore: `print(type(20))` scrive `<class 'int'>`.

Attenzione: `"200"` (testo) e `200` (numero) sono cose diverse. `"200" + "1"` dà `2001`, perché il testo si incolla. `200 + 1` dà `201`, perché i numeri si sommano.

## 5. input: fare una domanda

```python
nome = input("Come ti chiami? ")
```

`input` ferma il programma, mostra la domanda, aspetta che scrivi e premi Invio, poi mette quello che hai scritto nella variabile.

**Regola d’oro: `input` restituisce sempre testo**, anche se scrivi `200`. Per questo i calcoli sui numeri chiesti all’utente non funzionano senza una conversione.

## 6. Convertire i tipi: int(), float(), str()

```python
blocchi = int(input("Quanti blocchi hai? "))
```

Si legge dall’interno verso l’esterno: prima `input` raccoglie il testo, poi `int` lo trasforma in numero intero.

- `int("200")` dà `200`, `float("3.5")` dà `3.5`, `str(200)` dà `"200"`.
- Se il testo non assomiglia a un numero, per esempio `int("tanti")`, Python si ferma con un `ValueError`.
- Un decimale scritto con la virgola, come `"3,5"`, non viene capito: in Python si usa il punto.

## 7. Calcoli

- `+` somma, `-` sottrae, `*` moltiplica
- `/` divide e dà sempre un decimale (`7 / 2` dà `3.5`, `8 / 2` dà `4.0`)
- `//` divisione intera: quante volte ci sta, senza resto
- `%` resto della divisione
- `**` potenza (`2 ** 3` dà `8`)

Esempio con gli stack di Minecraft:

```python
blocchi = 200
stack = blocchi // 64     # 3 stack pieni
avanzo = blocchi % 64     # 8 blocchi che avanzano
```

Python rispetta l’ordine della matematica: `*` e `/` prima di `+` e `-`. Con le parentesi decidi tu: `(2 + 3) * 4` dà `20`.

Con i testi, `+` li incolla (`"Ciao " + "Steve"`) e `*` li ripete (`"ab" * 3` dà `ababab`). Ma non puoi sommare un testo e un numero: `"Ho " + 5` provoca un `TypeError`.

## 8. f-string: testo con le variabili dentro

```python
nome = "Steve"
stack = 3
print(f"{nome} riempie {stack} stack")
```

Sullo schermo: `Steve riempie 3 stack`. Metti una `f` davanti alle virgolette e scrivi le variabili tra parentesi graffe. È più comoda del `+` perché trasforma i numeri in testo da sola. Sulla tastiera italiana di Windows le graffe si scrivono con AltGr + Maiusc + è (apre) e AltGr + Maiusc + + (chiude).

## 9. Confronti

Un confronto dà come risultato `True` o `False`.

- `==` uguale
- `!=` diverso
- `<` minore, `>` maggiore
- `<=` minore o uguale, `>=` maggiore o uguale

```python
print(5 > 3)     # True
print(5 == 3)    # False
```

**Il classico errore:** `=` assegna un valore a una variabile, `==` confronta due valori. Dentro un `if` serve sempre `==`.

## 10. if, elif, else: far scegliere il programma

```python
if scavo == profondita:
    print("DIAMANTE!")
elif scavo < profondita:
    print("Solo terra... scava più in giù")
else:
    print("Troppo profondo, attento alla lava!")
```

Python legge dall’alto: esegue il primo blocco la cui condizione è vera e salta tutti gli altri. `else` non ha condizione: scatta quando nessuna delle precedenti era vera. `elif` ed `else` sono facoltativi, e puoi mettere più `elif`.

Due regole che non si possono dimenticare:

- **I due punti** `:` alla fine delle righe `if`, `elif` ed `else` (e anche di `for`, `while`, `def`).
- **Il rientro**: le righe che appartengono al blocco vanno spostate a destra di 4 spazi (nell’editor basta premere Tab), tutte con lo stesso rientro. In Python il rientro fa parte della sintassi: dice cosa sta «dentro» e cosa no.

Puoi combinare più condizioni con `and` (tutte vere), `or` (almeno una vera) e `not` (il contrario):

```python
if vita > 0 and fame > 0:
    print("Sei vivo e non hai fame")
```

## 11. import e random

Un modulo è una raccolta di strumenti già pronti, scritti da altri. Per usarlo lo si importa all’inizio del programma.

```python
import random

numero = random.randint(1, 10)
```

`random.randint(1, 10)` sceglie un numero intero a caso tra 1 e 10, con gli estremi inclusi. A ogni esecuzione può uscire un numero diverso. Si scrive `modulo.strumento`: prima il nome del modulo, poi il punto, poi quello che vuoi usare.

Per sapere cosa contiene un modulo si legge la documentazione ufficiale (docs.python.org/it/3/). Saperla leggere è la vera abilità da programmatore: nessuno conosce tutto a memoria.

## 12. for e range: ripetere

Un ciclo `for` ripete un blocco di righe, una volta per ogni valore di una serie.

```python
for i in range(3):
    print("Tic")
```

Scrive `Tic` tre volte. `range` produce la serie di numeri:

- `range(5)` dà 0, 1, 2, 3, 4 (parte da 0 e si ferma prima di 5)
- `range(1, 4)` dà 1, 2, 3
- `range(200, 1000, 100)` dà 200, 300, 400, …, 900 (inizio, fine, passo)

Il numero di fine **non** viene mai incluso. La variabile dopo `for` assume a ogni giro il valore successivo, quindi la puoi usare dentro il blocco:

```python
for frequenza in range(200, 1000, 100):
    winsound.Beep(frequenza, 150)
```

## 13. winsound: suonare

```python
import winsound

winsound.Beep(440, 500)
```

`Beep(frequenza, durata)`: la frequenza è in hertz e deve stare tra 37 e 32767, la durata è in millisecondi (1000 sono un secondo). Più la frequenza è alta, più il suono è acuto. Il programma aspetta che la nota finisca prima di passare alla riga dopo. Alcune frequenze utili: 262 Do, 294 Re, 330 Mi, 349 Fa, 440 La. Il modulo esiste solo su Windows.

## 14. Gli errori: cosa ti stanno dicendo

Un errore non è una bocciatura: è Python che ti dice dove guardare. Gli errori più comuni:

- `SyntaxError`: qualcosa è scritto male (due punti mancanti, parentesi o virgolette non chiuse).
- `IndentationError`: il rientro è sbagliato.
- `NameError`: hai usato un nome che Python non conosce (errore di battitura, o variabile non ancora creata).
- `TypeError`: stai combinando tipi che non vanno insieme, come testo e numero.
- `ValueError`: il tipo è giusto ma il valore no, per esempio `int("tanti")` o `Beep(0, 150)`.
- `ZeroDivisionError`: hai diviso per zero.

Come si legge un errore:

1. Leggi l’**ultima riga**: dice che cosa non va.
2. Guarda il **numero di riga** indicato e vai a vedere quella riga.
3. Se la riga sembra giusta, controlla anche quella **sopra**: spesso l’errore nasce lì.
4. Cambia **una cosa sola** e riprova. Se cambi tre cose insieme non capisci più quale ha funzionato.

Nelle missioni il riquadro «Cosa è successo» ti dà una mano in italiano, ma impara a leggere anche l’errore originale in rosso: sul lavoro vedrai solo quello.

## 15. Piccolo glossario

- **Istruzione**: una riga di codice che dice a Python di fare qualcosa.
- **Variabile**: un nome che contiene un valore.
- **Tipo**: la categoria di un valore (testo, intero, decimale, vero/falso).
- **Condizione**: qualcosa che è vero o falso, usato da `if`.
- **Ciclo**: un blocco che si ripete.
- **Modulo**: una raccolta di strumenti da importare.
- **Bug**: un errore nel programma. **Debug**: il lavoro di cercarlo e correggerlo.

## 16. Domande per controllare

Prima rispondi a voce o su carta, poi verifica in Officina. Per la domanda 1 usa questo codice:

```python
x = 7
print(x // 2, x % 2)
```

1. Cosa stampa il codice qui sopra?
2. Perché `"5" + 3` provoca un errore?
3. Qual è la differenza tra `=` e `==`?
4. Quali numeri produce `range(10, 40, 10)`?
5. Cosa stampa `print(f"{2 + 3} diamanti")`?
6. Perché `input` e `int` si usano spesso insieme?

### Soluzioni (per chi fa da copilota)

1. `3 1`: 7 diviso 2 fa 3 con resto 1.
2. Si cerca di sommare un testo e un numero, e Python non li mescola da solo. Si corregge con `"5" + str(3)` oppure con `int("5") + 3`.
3. `=` mette un valore in una variabile, `==` confronta due valori e dà `True` o `False`.
4. 10, 20, 30. Il 40 non è incluso.
5. `5 diamanti`: l’espressione tra graffe viene calcolata prima.
6. Perché `input` dà sempre testo, e `int` lo trasforma in un numero su cui si può calcolare.

## Approfondimento: variabili e condizioni

Queste pagine accompagnano le Missioni 4, 5 e 6. Non ci sono concetti nuovi: sono strumenti per usare meglio quelli che già conosci.

### and, or, not: come ragiona Python

- `and` è vera solo se **tutte** le condizioni sono vere.
- `or` è vera se **almeno una** è vera.
- `not` rovescia il risultato.

```python
ferro = 4
bastoni = 0

print(ferro >= 3 and bastoni >= 2)   # False
print(ferro >= 3 or bastoni >= 2)    # True
print(not ferro >= 3)                # False
```

Leggi la condizione ad alta voce: «ferro almeno 3 **e** bastoni almeno 2». Se la frase non ha senso per il gioco, la condizione è sbagliata. Due avvertimenti:

- Due condizioni identiche una dopo l’altra sono un campanello d’allarme: la seconda non può scattare mai.
- Ai due lati di `and` e `or` serve una condizione completa. Si scrive `nota == "do" or nota == "re"`, non `nota == "do" or "re"`.

### L’ordine in una catena di elif conta

Python si ferma al **primo** ramo vero e salta tutti gli altri. Quindi si va dal caso più stretto al più largo:

```python
vita = 3

if vita <= 5:
    print("Pericolo!")
elif vita <= 12:
    print("Così così")
else:
    print("Benissimo")
```

Stampa `Pericolo!`. Se scambi i primi due rami, con `vita = 3` stampa invece «Così così», perché `3 <= 12` è già vero e il ramo più stretto non scatta mai. Non c’è nessun errore: il programma gira e dà un risultato sbagliato.

### if dentro if

Un blocco può contenere un altro `if`, con quattro spazi di rientro in più:

```python
if cibo == "si":
    fame = fame + 6
    if fame > 20:
        fame = 20
```

Il secondo `if` viene controllato solo se il primo è vero. Così si mette un limite a un valore: prima lo cambi, poi controlli che non l’abbia superato. Esistono anche due scorciatoie: `min(a, b)` dà il valore più piccolo e `max(a, b)` il più grande. Quindi `max(vita, 0)` impedisce alla vita di scendere sotto 0, e `min(fame, 20)` di superare 20.

### Confrontare i testi

`==` funziona anche con i testi, ma devono combaciare **esattamente**: `"Si"` e `"si"` sono diversi, e anche `"si "` con uno spazio in fondo. Per ignorare maiuscole e minuscole si trasforma la risposta in minuscolo con `.lower()`:

```python
risposta = input("Mangi qualcosa? (si/no): ").lower()
```

Si legge da sinistra a destra: prima `input` raccoglie il testo, poi `.lower()` lo rende minuscolo. Se l’utente scrive `SI` o `Si`, `risposta` contiene `si`.

L’`else` alla fine di una catena è la tua rete di sicurezza: cattura tutto quello che non avevi previsto. Senza `else`, un valore imprevisto può lasciare una variabile mai creata, e Python risponde con un `NameError`.

### Una variabile assegnata in rami diversi

```python
if nota == "do":
    frequenza = 262
elif nota == "re":
    frequenza = 294
else:
    frequenza = 0
```

Ogni ramo assegna la stessa variabile, che dopo la catena si può usare. La regola: dopo una catena di `if` e `elif`, la variabile deve avere un valore **in ogni caso**. Se un ramo manca, o manca l’`else`, la variabile può non esistere.

### Divisione: / o //?

`/` dà sempre un decimale (`440 / 2` dà `220.0`), `//` dà un intero (`440 // 2` dà `220`). Alcune funzioni, come `winsound.Beep`, vogliono un numero intero: se ricevono `220.0` si fermano con un `TypeError`. Per tornare a un intero si usa `//` oppure `int(220.0)`.

### Come provare un programma con condizioni

- Un caso per **ogni ramo**.
- I casi sul **confine**: se la soglia è 5, prova 5 e 6.
- Un valore **strano**: 0, un numero negativo, una parola che non ti aspetti.

Scrivi prima cosa ti aspetti: è il passo «prevedi» delle missioni. Ogni differenza tra la previsione e il risultato è un bug trovato.

### Domande per controllare (Missioni 4, 5 e 6)

Tre piccoli programmi, D, E e F.

Programma D:

```python
x = 10
if x > 5:
    print("A")
elif x > 8:
    print("B")
else:
    print("C")
```

Programma E:

```python
a = 4
b = 0
if a > 3 and b > 0:
    print("1")
elif a > 3 or b > 0:
    print("2")
else:
    print("3")
```

Programma F:

```python
vita = 20 - 25
vita = max(vita, 0)
print(vita)
```

1. Cosa stampa il programma D? Esiste un valore di `x` che faccia stampare B?
2. Cosa stampa il programma E?
3. Cosa stampa il programma F?
4. Perché `if nota == "do" or "re":` non fa quello che sembra?
5. Quanto fanno `440 / 2` e `440 // 2`? Perché la differenza conta con `winsound.Beep`?
6. Come fai ad accettare «SI», «Si» e «si» con un solo confronto?

#### Soluzioni (per chi fa da copilota)

1. Stampa `A`. No, nessun valore: ogni `x` maggiore di 8 è anche maggiore di 5, quindi il ramo B non scatta mai. Andrebbe messo prima.
2. Stampa `2`: `a > 3` è vera ma `b > 0` è falsa, quindi `and` non basta, mentre `or` sì.
3. Stampa `0`: la vita vale `-5`, e `max(-5, 0)` dà 0.
4. Perché `"re"` da solo è un testo non vuoto, e Python lo considera sempre vero: la condizione risulta vera qualunque sia la nota. Si scrive `nota == "do" or nota == "re"`.
5. `220.0` e `220`. `Beep` vuole un numero intero, quindi con `220.0` si ferma con un `TypeError`.
6. Con `.lower()` sulla risposta: `risposta = input(...).lower()`, e poi si confronta con `"si"`.

## Parte 2: ripetere, raccogliere, riutilizzare

Queste pagine accompagnano le Missioni 7, 8 e 9. Come prima: tienile aperte mentre lavori e consultale quando serve.

## 17. while: ripetere finché una condizione è vera

Il `for` ripete un numero di volte che conosci già. Il `while` ripete **finché** una condizione resta vera, e non sai in anticipo quanti giri serviranno.

```python
vita = 20
while vita > 0:
    print("Il creeper ti colpisce! Vita:", vita)
    vita = vita - 5
print("Game over")
```

Sullo schermo:

```
Il creeper ti colpisce! Vita: 20
Il creeper ti colpisce! Vita: 15
Il creeper ti colpisce! Vita: 10
Il creeper ti colpisce! Vita: 5
Game over
```

- Prima di ogni giro Python controlla la condizione: se è vera esegue il blocco, se è falsa salta alla riga dopo il ciclo.
- La riga del `while` finisce con i due punti e il blocco ha il rientro, come per `if`.
- **Qualcosa dentro il ciclo deve far cambiare la condizione.** Qui `vita` scende a ogni giro. Se niente cambia, la condizione resta vera per sempre e il ciclo non finisce mai: è un ciclo infinito.
- Se il programma non si ferma, premi **Stop** in Officina (nel terminale di VS Code si usa Ctrl+C). Non è un danno: capita a tutti i programmatori.
- Per contare i giri si usa un contatore: `tentativi = tentativi + 1`, che si può abbreviare in `tentativi += 1`. La variabile va creata prima del ciclo (`tentativi = 0`), altrimenti arriva un `NameError`.
- Si possono combinare condizioni con `and`: `while scavo != profondita and tentativi < 7:` continua solo se il diamante non è stato trovato **e** hai ancora tentativi.
- `break` esce subito dal ciclo, qualunque sia la condizione:

```python
while True:
    risposta = input("Scrivi esci per uscire: ")
    if risposta == "esci":
        break
```

`while True` significa «sempre vero»: l’unico modo per uscirne è `break`.

- Come scegliere: `for` quando sai quante volte ripetere o hai una serie di valori; `while` quando la ripetizione dipende da una condizione.

## 18. Liste: più valori in una sola variabile

```python
zaino = ["spada", "pala", "torcia"]
print(zaino[0])        # spada
print(zaino[-1])       # torcia
zaino.append("pane")   # aggiunge in fondo
zaino.remove("pala")   # toglie questo elemento
print(len(zaino))      # 3
```

- Una lista si scrive tra parentesi quadre, con gli elementi separati da virgole. Sulla tastiera italiana di Windows le quadre si scrivono con AltGr + è e AltGr + +.
- Ogni elemento ha una **posizione** (indice) che parte da **0**: il primo è `zaino[0]`, il secondo `zaino[1]`. Con `-1` si prende l’ultimo.
- Se chiedi una posizione che non esiste, Python risponde con un `IndexError`. Una lista di 3 elementi ha le posizioni 0, 1, 2.
- `len(lista)` dice quanti elementi ci sono, `append` aggiunge in fondo, `remove` toglie un elemento (se non c’è, arriva un `ValueError`).
- `"spada" in zaino` dà `True` o `False`: serve per controllare prima di agire.
- Per cambiare un elemento si assegna alla sua posizione: `zaino[1] = "arco"`.
- Con `for` si scorre tutta la lista, un elemento per giro:

```python
for oggetto in zaino:
    print("-", oggetto)
```

- Una lista può contenere numeri: `[262, 294, 330]` è una serie di note, e un `for` può suonarle una per una.

## 19. Dizionari: valori con un nome

```python
risorse = {"legno": 64, "ferro": 12, "diamanti": 3}
print(risorse["ferro"])       # 12
risorse["diamanti"] = 5       # cambia un valore
risorse["oro"] = 7            # aggiunge una voce nuova
```

- Un dizionario si scrive tra parentesi graffe, con coppie `chiave: valore`. Le chiavi sono i nomi con cui cerchi (qui `"legno"`), i valori sono quello che ci trovi.
- Si cerca con le quadre e la chiave, non con la posizione: `risorse["ferro"]`.
- Se la chiave non esiste, Python risponde con un `KeyError`. Per cercare senza rischi si usa `risorse.get("oro", 0)`, che dà il valore oppure `0` se la chiave manca.
- `"ferro" in risorse` controlla se la chiave esiste.
- Ogni chiave compare una volta sola: assegnarla di nuovo cambia il valore.
- Con `for` si scorrono le chiavi:

```python
for nome in risorse:
    print(nome, ":", risorse[nome])
```

- **Lista o dizionario?** Lista quando conta l’ordine o la posizione (le note di una melodia, gli oggetti dello zaino). Dizionario quando vuoi trovare un valore dal suo nome (quanti diamanti ho, quanta vita ha il personaggio).

## 20. Funzioni: dare un nome a un pezzo di programma

```python
def saluta(nome):
    print("Ciao", nome)

saluta("Steve")
saluta("Alex")
```

Scrive due saluti. `def` **definisce** la funzione ma non la esegue: il codice parte solo quando la **chiami**, scrivendo il nome seguito dalle parentesi.

- La riga `def` finisce con i due punti e il corpo ha il rientro, come per `if` e `for`.
- I **parametri** sono i nomi tra parentesi nella definizione (`nome`), gli **argomenti** sono i valori che passi quando chiami (`"Steve"`). Se ne dai di meno o di più di quelli richiesti, arriva un `TypeError`.
- **`return`** restituisce un risultato a chi ha chiamato la funzione:

```python
def stack_pieni(blocchi):
    return blocchi // 64

stack = stack_pieni(200)
print(stack)    # 3
```

- **`print` e `return` non sono la stessa cosa.** `print` scrive sullo schermo, ma il valore poi è perso. `return` lo consegna, e puoi usarlo dopo, in un calcolo o in una variabile. Una funzione senza `return` restituisce `None` («niente»): è il bug silenzioso più frequente.
- Una funzione deve essere definita **prima** di essere chiamata: se la chiami più in alto nel file, arriva un `NameError`.
- Le variabili create dentro una funzione esistono solo lì dentro.
- Una funzione può chiamarne un’altra e può ricevere una lista:

```python
def melodia(note, durata):
    for frequenza in note:
        suona(frequenza, durata)
```

- Si scrivono funzioni per non copiare lo stesso codice, per dare nomi chiari alle cose e per provare un pezzo alla volta. Se ti accorgi di aver incollato lo stesso gruppo di righe due volte, è il momento di scrivere una funzione.

## 21. Nuovi errori e come riconoscerli

- `IndexError`: hai chiesto una posizione che non esiste in una lista. Ricorda che si parte da 0.
- `KeyError`: hai cercato in un dizionario una chiave che non c’è.
- **Ciclo infinito**: il programma non finisce e continua a scrivere. Premi Stop, poi controlla che dentro il `while` qualcosa cambi la condizione.
- `NameError` con una funzione: o hai sbagliato il nome, o l’hai chiamata prima di definirla.
- `TypeError` con «missing required argument»: hai chiamato una funzione senza tutti i valori che chiede.
- `None` nell’output: la funzione non ha il `return`.
- **Errori silenziosi**: a volte il programma gira senza errori ma il risultato è sbagliato, come prendere `zaino[1]` credendo che sia il primo oggetto. Per trovarli, stampa i valori con `print` nei punti sospetti e confrontali con quello che ti aspettavi.

## 22. Altre parole utili

- **Contatore**: variabile che aumenta a ogni giro. **Ciclo infinito**: ciclo che non si ferma mai.
- **Lista** e **indice**: un elenco ordinato di valori, e la posizione di un elemento (si parte da 0).
- **Dizionario** e **chiave**: una raccolta di coppie nome-valore, e il nome con cui si cerca.
- **Funzione**: un pezzo di programma con un nome. **Parametro**: il nome che riceve il valore. **Argomento**: il valore che passi. **Valore di ritorno**: ciò che restituisce `return`.

## 23. Domande per controllare (parte 2)

Ecco tre piccoli programmi, che chiamiamo A, B e C.

Programma A:

```python
n = 3
while n > 0:
    print(n)
    n = n - 1
```

Programma B:

```python
n = 3
while n > 0:
    print(n)
```

Programma C:

```python
def doppio(x):
    return x * 2

print(doppio(4) + 1)
```

1. Cosa stampa il programma A?
2. Perché il programma B non finisce mai? Come lo correggi?
3. Cosa stampa il programma C?
4. Data `lettere = ["a", "b", "c"]`, cosa fa `print(lettere[1])`? E `print(lettere[3])`?
5. Dato `d = {"vita": 20}`, come porti la vita a 15? Cosa succede con `d["fame"]`?
6. Qual è la differenza tra `print` e `return` dentro una funzione?

### Soluzioni (per chi fa da copilota)

1. Stampa 3, 2 e 1, uno per riga.
2. Dentro il ciclo `n` non cambia mai, quindi `n > 0` resta sempre vera. Manca la riga `n = n - 1`.
3. Stampa `9`: `doppio(4)` dà 8, più 1.
4. `print(lettere[1])` stampa `b`, perché le posizioni partono da 0. `lettere[3]` dà un `IndexError`, perché le posizioni esistenti sono 0, 1 e 2.
5. Con `d["vita"] = 15`. `d["fame"]` dà un `KeyError` perché la chiave non esiste (con `d.get("fame", 0)` darebbe invece 0).
6. `print` scrive sullo schermo e il valore si perde, `return` restituisce il valore a chi ha chiamato la funzione, che lo può usare in un calcolo o salvare in una variabile.

## Parte 3: scrivere un programma da solo

Nelle Sfide nessuno ti dà il codice: lo costruisci tu. Il segreto non è scrivere in fretta, è pensare prima. Il PIANO in cima al file segue quattro domande.

### Il piano in quattro domande

1. **Cosa mi viene dato?** I dati di partenza: numeri chiesti con `input`, una lista ricevuta da una funzione, e così via.
2. **Cosa devo ottenere?** Il risultato: cosa stampare, oppure cosa restituire con `return`.
3. **Quali passi servono, in ordine?** Scrivili in italiano, come una ricetta, prima di scrivere codice.
4. **Quali casi particolari ci sono?** Cosa succede con zero, con un numero negativo, con una lista vuota, quando non basta qualcosa?

Un esempio di piano, senza codice. Problema: il cinema costa 8 euro, 5 per chi ha meno di 14 anni e 6 per chi ne ha più di 65.

- Dato: l’età.
- Da ottenere: il prezzo del biglietto.
- Passi: chiedo l’età e la trasformo in numero; se ha meno di 14 anni il prezzo è 5; altrimenti, se ne ha più di 65, il prezzo è 6; altrimenti è 8; stampo il prezzo.
- Casi particolari: esattamente 14 e esattamente 65 (a quale prezzo appartengono?), età 0, età negativa.

### Provare i casi al confine

Un programma che funziona per l’esempio non basta: deve funzionare per tutti i valori. Provane sempre tre tipi:

- il caso **più piccolo** (0, una lista vuota),
- i casi **al confine** (nell’esempio sopra, 13, 14, 65 e 66),
- un caso **normale**.

Per questo le Sfide hanno anche prove nascoste: servono a scoprire se la soluzione ragiona davvero o è scritta su misura per gli esempi.

### Scrivere a pezzi

- Scrivi un pezzo, premi Esegui e controlla, poi passa al pezzo dopo. Non scrivere trenta righe prima di provare.
- Stampa i valori intermedi con `print` per vedere cosa sta succedendo davvero.
- Se non sai da dove cominciare, risolvi a mano un esempio piccolo e scrivi cosa fai a ogni passo: quei passi sono il programma.

### Quando una prova non passa

- Leggi cosa si aspettava il computer e cosa hai ottenuto: la differenza è l’indizio.
- Spesso l’errore è «di uno»: un ciclo parte o si ferma un giro troppo presto o troppo tardi. Controlla dove inizia e dove finisce il `range`.
- Cambia una cosa sola e ricontrolla, come per gli errori di Python.

## Parte 4: esempi pratici

Ogni esempio rimanda ai capitoli della teoria. Riscrivilo a mano, eseguilo e poi cambialo: cambia un numero, aggiungi una riga, rompilo apposta e leggi l’errore. I risultati qui sotto sono quelli veri dell’esecuzione.

### Quanti giorni hai vissuto? (capitoli 1, 3, 5, 6, 8)

Chiede un nome e un’età, poi calcola i giorni con una moltiplicazione.

```python
nome = input("Come ti chiami? ")
anni = int(input("Quanti anni hai? "))
giorni = anni * 365
print(f"Ciao {nome}! Hai vissuto circa {giorni} giorni.")
```

Esempio di esecuzione:

```
Come ti chiami? Luca
Quanti anni hai? 12
Ciao Luca! Hai vissuto circa 4380 giorni.
```

`input` dà sempre testo, quindi `anni` passa da `int()` prima di essere moltiplicato. Prova a togliere `int()`: cosa stampa il programma, e perché? Poi aggiungi anche i mesi vissuti.

### Dividere il conto della pizza (capitoli 6, 7, 8)

```python
totale = float(input("Quanto avete speso in tutto? "))
amici = int(input("In quanti siete? "))
quota = totale / amici
print(f"Ognuno paga {quota} euro")
```

```
Quanto avete speso in tutto? 47
In quanti siete? 4
Ognuno paga 11.75 euro
```

Qui il totale si legge con `float()` perché i soldi possono avere i decimali, mentre le persone sono un numero intero. La divisione `/` dà sempre un decimale. Prova con 47 euro in 3 persone: esce un numero con moltissime cifre dopo la virgola. È normale: più avanti vedrai come si arrotonda. Per ora, sai già dire perché non esce un numero «bello»?

### Il biglietto del cinema (capitoli 9 e 10, Parte 3)

È il problema del piano nella Parte 3, ora scritto in codice: 8 euro, 5 sotto i 14 anni, 6 sopra i 65.

```python
eta = int(input("Quanti anni hai? "))
if eta < 14:
    prezzo = 5
elif eta > 65:
    prezzo = 6
else:
    prezzo = 8
print("Il biglietto costa", prezzo, "euro")
```

Tre esecuzioni, con 12, 14 e 70 anni:

```
Quanti anni hai? 12
Il biglietto costa 5 euro
```

```
Quanti anni hai? 14
Il biglietto costa 8 euro
```

```
Quanti anni hai? 70
Il biglietto costa 6 euro
```

Con 14 anni il biglietto costa 8, non 5: la condizione è `eta < 14`, quindi il 14 non è incluso. È un caso **al confine**. Se il cinema volesse il prezzo ridotto anche a 14 anni, basterebbe scrivere `<=`. Aggiungi una domanda «hai la tessera?» che porta lo sconto a 1 euro in meno, usando `and`.

### L’anno bisestile (capitoli 7, 9 e 10)

Un anno è bisestile se si divide per 4, ma non se si divide per 100, a meno che si divida anche per 400.

```python
anno = int(input("Che anno? "))
if (anno % 4 == 0 and anno % 100 != 0) or anno % 400 == 0:
    print(anno, "è bisestile")
else:
    print(anno, "non è bisestile")
```

```
Che anno? 2024
2024 è bisestile
```

```
Che anno? 1900
1900 non è bisestile
```

```
Che anno? 2000
2000 è bisestile
```

`and` e `or` sono mescolati, e le parentesi decidono cosa viene controllato per primo. Prima di eseguire, prevedi cosa dirà il programma per 2023 e per 2100, poi verifica.

### Il dado (capitolo 11)

```python
import random

dado = random.randint(1, 6)
print("È uscito", dado)
if dado == 6:
    print("Hai fatto sei! Tira ancora")
```

Ogni esecuzione può dare un numero diverso. In questa è uscito:

```
È uscito 2
```

Tira due dadi e somma i risultati. Se escono due numeri uguali, stampa anche «Doppio!».

### La tabellina (capitolo 12)

```python
n = int(input("Quale tabellina? "))
for i in range(1, 11):
    print(n, "x", i, "=", n * i)
```

```
Quale tabellina? 7
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

Il `range` finisce in 11 perché il numero di fine non è incluso. Cambia il programma in modo che stampi solo i risultati pari (ti serve `%`).

### Quanto risparmio in un anno? (capitolo 12)

Ricevi 5 euro a settimana. Quanto hai dopo un anno, cioè dopo 52 settimane?

```python
risparmi = 0
for settimana in range(1, 53):
    risparmi = risparmi + 5
print("Dopo un anno avrai", risparmi, "euro")
```

```
Dopo un anno avrai 260 euro
```

La riga `risparmi = risparmi + 5` è un **accumulatore**: una variabile che a ogni giro si arricchisce di qualcosa. Si crea **prima** del ciclo, partendo da 0, e si stampa **dopo**. È lo stesso schema del contatore `tentativi = tentativi + 1`, e serve ogni volta che vuoi un totale. Cosa cambia se, invece di 5, aggiungi il numero della settimana? Calcola a mano le prime tre settimane prima di provare.

### Il conto alla rovescia (capitolo 17)

```python
n = int(input("Da che numero parto? "))
while n > 0:
    print(n)
    n = n - 1
print("Via!")
```

```
Da che numero parto? 3
3
2
1
Via!
```

La condizione `n > 0` cambia perché dentro il ciclo c’è `n = n - 1`. Se cancelli quella riga, il programma non finisce più: è il momento di usare il pulsante Stop. E se parti da 0? Prevedi cosa succede prima di provare.

### La lista della spesa (capitolo 18)

```python
spesa = ["pane", "latte", "mele"]
spesa.append("pasta")
spesa.remove("latte")
print("Devo comprare", len(spesa), "cose:")
for cosa in spesa:
    print("-", cosa)
if "pane" in spesa:
    print("Il pane è nella lista")
```

```
Devo comprare 3 cose:
- pane
- mele
- pasta
Il pane è nella lista
```

Ho aggiunto la pasta e tolto il latte, quindi la lista è rimasta di tre elementi. Fai chiedere all’utente con `input` cosa aggiungere, e controlla con `in` che non sia già nella lista.

### I voti per materia (capitolo 19)

```python
voti = {"matematica": 8, "italiano": 7, "inglese": 9}
voti["storia"] = 6
voti["italiano"] = 8
for materia in voti:
    print(materia, ":", voti[materia])
print("In arte ho preso", voti.get("arte", "ancora niente"))
```

```
matematica : 8
italiano : 8
inglese : 9
storia : 6
In arte ho preso ancora niente
```

`voti["storia"] = 6` aggiunge una voce nuova, `voti["italiano"] = 8` ne cambia una che c’è già. Con `voti["arte"]` il programma si sarebbe fermato con un `KeyError`, ma `.get("arte", "ancora niente")` restituisce il testo di riserva. Aggiungi un voto che chiedi con `input` e stampa quante materie ci sono.

### Due piccole funzioni (capitolo 20)

```python
def celsius_a_fahrenheit(c):
    return c * 9 / 5 + 32

def e_pari(n):
    return n % 2 == 0

print(celsius_a_fahrenheit(0))
print(celsius_a_fahrenheit(20))
print(celsius_a_fahrenheit(100))
print(e_pari(10), e_pari(7))
```

```
32.0
68.0
212.0
True False
```

`e_pari` restituisce direttamente il risultato di un confronto, quindi è una funzione che risponde «vero» o «falso». Questo schema ti servirà nelle Sfide. Scrivi `e_multiplo_di_tre(n)` e provala con 9, 10 e 0.

## Parte 5: piccoli progetti completi

Qui i pezzi si mettono insieme. Per ogni progetto: leggi il programma, riscrivilo a mano, eseguilo e poi miglioralo con le idee in fondo.

### Il quiz delle tabelline

**Cosa mette insieme:** `random`, `for`, `input` e `int`, `if` ed `elif`, un contatore.

```python
import random

punti = 0
for domanda in range(5):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    risposta = int(input(f"Quanto fa {a} x {b}? "))
    if risposta == a * b:
        print("Giusto!")
        punti = punti + 1
    else:
        print("No, fa", a * b)

print(f"Hai totalizzato {punti} punti su 5")
if punti == 5:
    print("Perfetto!")
elif punti >= 3:
    print("Bravo!")
else:
    print("Ripassa le tabelline e riprova")
```

Una partita (le domande cambiano a ogni esecuzione):

```
Quanto fa 7 x 4? 28
Giusto!
Quanto fa 8 x 2? 16
Giusto!
Quanto fa 3 x 10? 31
No, fa 30
Quanto fa 3 x 7? 21
Giusto!
Quanto fa 2 x 10? 20
Giusto!
Hai totalizzato 4 punti su 5
Bravo!
```

**Come funziona:**

- Il `for` ripete cinque volte: a ogni giro due numeri a caso da 2 a 10 formano la domanda.
- La risposta viene confrontata con `a * b`: se è giusta, `punti` aumenta di 1.
- Alla fine una catena di `if` ed `elif` sceglie il messaggio. L’ordine conta: si controlla prima il caso più stretto (5 punti), poi quello più largo.

**Prova a modificarlo:**

- Fai scegliere all’utente quante domande vuole.
- Aggiungi domande di addizione e di sottrazione.
- Dopo una risposta sbagliata, dai una seconda possibilità.

### Il salvadanaio

**Cosa mette insieme:** `while True` con `break`, `if` / `elif` / `else`, variabili che cambiano, una lista di movimenti.

```python
saldo = 0
movimenti = []

while True:
    comando = input("Cosa vuoi fare? (versa, preleva, saldo, esci): ")
    if comando == "versa":
        importo = int(input("Quanto versi? "))
        saldo = saldo + importo
        movimenti.append("versati " + str(importo))
    elif comando == "preleva":
        importo = int(input("Quanto prelevi? "))
        if importo > saldo:
            print("Non hai abbastanza soldi")
        else:
            saldo = saldo - importo
            movimenti.append("prelevati " + str(importo))
    elif comando == "saldo":
        print("Nel salvadanaio ci sono", saldo, "euro")
    elif comando == "esci":
        break
    else:
        print("Non conosco questo comando")

print("Movimenti di oggi:")
for m in movimenti:
    print("-", m)
```

Una sessione:

```
Cosa vuoi fare? (versa, preleva, saldo, esci): versa
Quanto versi? 20
Cosa vuoi fare? (versa, preleva, saldo, esci): preleva
Quanto prelevi? 5
Cosa vuoi fare? (versa, preleva, saldo, esci): preleva
Quanto prelevi? 50
Non hai abbastanza soldi
Cosa vuoi fare? (versa, preleva, saldo, esci): saldo
Nel salvadanaio ci sono 15 euro
Cosa vuoi fare? (versa, preleva, saldo, esci): ciao
Non conosco questo comando
Cosa vuoi fare? (versa, preleva, saldo, esci): esci
Movimenti di oggi:
- versati 20
- prelevati 5
```

**Come funziona:**

- Il ciclo `while True` gira finché non si incontra `break`: qui succede quando scrivi `esci`.
- Ogni comando è un ramo della catena. L’`else` finale raccoglie tutto quello che non avevi previsto.
- Prima di prelevare, un `if` dentro il ramo controlla che i soldi bastino: è un caso particolare gestito.
- I movimenti finiscono in una lista con `append`, e si stampano alla fine con un `for`.

**Prova a modificarlo:**

- Aggiungi il comando `storia`, che stampa i movimenti senza uscire.
- Blocca i versamenti negativi o uguali a 0: che messaggio dai?
- Fai partire il salvadanaio con 10 euro già dentro.

### Il convertitore di temperature

**Cosa mette insieme:** funzioni con `return`, `input` e `float`, `if` / `elif` / `else`.

```python
def celsius_a_fahrenheit(c):
    return c * 9 / 5 + 32

def fahrenheit_a_celsius(f):
    return (f - 32) * 5 / 9

scelta = input("Da Celsius a Fahrenheit (1) o il contrario (2)? ")
if scelta == "1":
    gradi = float(input("Quanti gradi Celsius? "))
    print(gradi, "°C sono", celsius_a_fahrenheit(gradi), "°F")
elif scelta == "2":
    gradi = float(input("Quanti gradi Fahrenheit? "))
    print(gradi, "°F sono", fahrenheit_a_celsius(gradi), "°C")
else:
    print("Scelta non valida")
```

Tre esecuzioni:

```
Da Celsius a Fahrenheit (1) o il contrario (2)? 1
Quanti gradi Celsius? 25
25.0 °C sono 77.0 °F
```

```
Da Celsius a Fahrenheit (1) o il contrario (2)? 2
Quanti gradi Fahrenheit? 212
212.0 °F sono 100.0 °C
```

```
Da Celsius a Fahrenheit (1) o il contrario (2)? 3
Scelta non valida
```

**Come funziona:**

- Le due funzioni stanno in alto, perché vanno definite **prima** di essere chiamate.
- Le funzioni non stampano: **restituiscono** il risultato, e chi le usa decide cosa farne. Per questo si possono riutilizzare in altri programmi.
- Il programma principale è solo la scelta e la stampa.

**Prova a modificarlo:**

- Aggiungi la conversione tra chilometri e miglia (un miglio vale circa 1,61 chilometri).
- Se la temperatura in Celsius è sotto 10, stampa anche «Mettiti la giacca!».
- Scrivi una terza scelta che ripete la conversione finché non scrivi «basta».

### E adesso?

Dopo questi progetti, inventa il tuo: parti da un’idea piccola, scrivi il PIANO come nella Parte 3 e costruiscilo a pezzi. Un buon programma da cui partire è sempre un problema che hai davvero, per esempio i punti di una partita, le spese del mese o un quiz per i tuoi amici.
