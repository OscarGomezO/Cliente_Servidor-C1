from errno import EEXIST
import socket
import tqdm
import os
#import errno

sockett = socket.socket()

#Direccion IP OSCAR: 25.121.168.83
#LOCAL HOST: 127.0.0.1

#--------------------------------------------------------------------
#host = '25.121.154.185'
host = '127.0.0.1'
sockett.connect((host, 5757))

#Enviar 4KB 
Buffer_size = 1024 * 4
#path_route = "/home/dimas/Escritorio/ClienteServidor/Cliente_Servidor-C1/Cliente/images"
#--------------------------ENVIAR-------------------------------------
def enviar(accion):
    sockett.send(accion.encode('utf-8'))
    fname = input("Ingrese nombre del archivo: ")
    print("Archivo enviado {}".format(fname))
    #Obtenemos el tamao del archivo
    fsize = os.stat(fname).st_size
    #print("Nombre Archivo: " + fname)
    #print("Size:" + str(fsize))

    mensaje = [fname, fsize]

    #Enviar el archivo
    sockett.send(f"{mensaje[0]} {mensaje[1]}".encode())
    
    #Barra de progreso
    Bprogress = tqdm.tqdm(range(mensaje[1]), f"Enviando {mensaje[0]}", unit="B", unit_scale=True, unit_divisor=1024)


    with open(fname, "rb") as f:
        while True:
            bytes = f.read(Buffer_size)
            
            if not bytes:
                break
            sockett.sendall(bytes)
            Bprogress.update(len(bytes))

    sockett.close()

#--------------------------DESCARGAR-------------------------------------
def descargar(accion):

    #Crear un directorio
    try:
        os.mkdir('filesC')
    except OSError as e:
        if e.errno != EEXIST:
            raise

    
    sockett.send(accion.encode('utf-8'))
    
    fname = input("Ingrese nombre del archivo: ")
    
    print("File to upload {}".format(fname))

    sockett.send(fname.encode('utf-8'))


    fsize = sockett.recv(Buffer_size).decode()
    fsize = int(fsize)
    #sockett.send(f"{fname}".encode())
    Bprogress = tqdm.tqdm(range(fsize), f"Recibiendo {fname}", unit="B", unit_scale=True, unit_divisor=1024)
    os.path("/filesC" + fname)
    with open(fname, "wb") as f:
        while True:
            bytes_read = sockett.recv(Buffer_size)

            if not bytes_read:
                break
            
            f.write(bytes_read)
            Bprogress.update(len(bytes_read))
    sockett.close()

#--------------------------LISTAR-------------------------------------
def listar(accion):
    sockett.send(accion.encode('utf-8'))
    print("\n---------------ARCHIVOS LISTADOS-------------------\n")
    list = sockett.recv(Buffer_size).decode()
    print(list[1:-1])
    print("\n---------------------------------------------------\n")



def menu():
    print("-----POR FAVOR SELECCIONE UN NUMERO-------\n 1. ------> Enviar archivos \n 2. ------> Descargar archivos \n 3. ------> Listar Archivos \n" )
    seleccion = input()

    if seleccion == "1":
        print("Seleccionaste la opcion de enviar archivo")
        enviar("ENVIAR")
    elif seleccion == "2":
        print("Seleccionaste la opcion de descargar archivo")
        descargar("DESCARGAR")
    elif seleccion == "3":
        print("Seleccionaste la opcion Listar")
        listar("LISTAR")
    else:
        print("Por favor digite una opcion valida")
    
menu()
