

def opcion():
    print("-----POR FAVOR SELECCIONE UN NUMERO-------\n 1. ------> Enviar archivos \n 2. ------> Descargar archivos \n 3. ------> Listar Archivos \n" )
    seleccion = input()

    if seleccion == "1":
        print("Hola haz seleccionado la opcion 1")
        return "ENVIAR"
    elif seleccion == "2":
        print("Hola haz seleccionado la opcion 2")
        enviar()
        return "DESCARGAR"
    elif seleccion == "3":
        print("Hola haz seleccionado la opcion 3")
        return "LISTAR"
    else:
        print("Por favor digite una opcion valida")

opcion()

