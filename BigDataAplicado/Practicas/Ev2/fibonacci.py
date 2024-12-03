# Dado un numero pasado por pantalla, calcular el digito cuya posicion es el numero pasado por pantalla

def main():
    try:
        numero = 0
        condicion= True
        posicion = int(input("Ingrese un numero: "))
        while condicion:
            for i in range(0, posicion + 1):
                #####
                
                #####
                if posicion == i:
                    print(f"El numero en la posicion {posicion} es: {(numero)}")
                    condicion = False
            
    except ValueError:
        print("Error al ingresar el numero")
        return

if __name__ == "__main__":
    main()