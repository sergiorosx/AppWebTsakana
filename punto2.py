import sys

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

abecedario = {
'A' : 1,
'B' : 2,
'C' : 3,
'D' : 4,
'E' : 5,
'F' : 6,
'G' : 7,
'H' : 8,
'I' : 9,
'J' : 10,
'K' : 11,
'L' : 12,
'M' : 13,
'N' : 14,
'Ñ' : 15,
'O' : 16,
'P' : 17,
'Q' : 18,
'R' : 19,
'S' : 20,
'T' : 21,
'U' : 22,
'V' : 23,
'W' : 24,
'X' : 25,
'Y' : 26,
'Z' : 27
}

#print(abecedario)

mensajecifrado = input("Ingrese el mensaje cifrado: ")

if mensajecifrado is None or mensajecifrado == '':
    print("Error: debe ingresar un mensaje cifrado")
    sys.exit()
elif not mensajecifrado.isalpha():
    print("Error: debe ingresar caracteres alfabeticos")
    sys.exit()

mensajecifrado = mensajecifrado.upper()

#print(mensajecifrado)

desplazamiento = input("Ingrese el desplazamiento: ")

if not is_integer(desplazamiento):
    print("Error: debe ingresar un valor entero")
    sys.exit()

signo = 1

if int(desplazamiento) < 0:
    signo = -1

desplazamiento = abs(int(desplazamiento))


nuevomensaje = ""
for letra in mensajecifrado:
    #print(letra)
    nextposition = abecedario[letra]

    for n in range(desplazamiento):
        nextposition = nextposition + 1*signo

        if nextposition == 0:
            nextposition = 27
        elif nextposition > 27:
            nextposition = 0
    
    #print(abecedario[letra])
    #print(nextposition)
    
    for key, value in abecedario.items():
        if value == nextposition:
            #print(key, '->', value)
            nuevomensaje = nuevomensaje + key

print(nuevomensaje)