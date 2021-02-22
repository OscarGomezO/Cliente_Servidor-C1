import socket
import zmq
import sys
import tqdm
import os

sockett = socket.socket()


host = '127.0.1.1' #Local IP
#host = '25.121.154.185' # Local REMOTA HAMACHI
#host = '25.121.168.83' #REMOTA DIMAS

sockett.connect((host, 9000))
#socket.connect("tcp://25.1.254.151:5555")

#Que desea hacer el usuario
#equal = input("Ingrese la palabra ENVIAR, DESCARGAR ó LISTAR: ")

#sockett.send(equal.encode('utf-8'))

#Enviar 4KB 
Buffer_size = 1024 * 4


def menu():
    print(""" ---------------------------------MENÚ-------------------------------)
    1) ENVIAR Archivo
    2) DESCARGAR Archivo
    3) LISTAR Archivos
    """)
    KEY = input("Elija una Opción: \t")
    sockett.send(KEY.encode('utf-8'))
    while True:

        #--------------------------ENVIAR-------------------------------------
        if  KEY== "1":
            fname = input("Ingrese nombre del archivo: ")
            
            print("Archivo enviado {}".format(fname))
            #Obtenemos el tamao del archivo
            fsize = os.stat(fname).st_size
            #print("Nombre Archivo: " + fname)
            #print("Size:" + str(fsize))
            mensaje = [fname, fsize]
            #Enviar el archivo
            #sockett.send(f"{mensaje[0]} {mensaje[1]}".encode())
            sockett.send(f"{mensaje[0]} {mensaje[1]}".encode('utf-8'))
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
        if KEY == "2":
            fname = input("Ingrese nombre del archivo: ")
            print("File to upload {}".format(fname))

            sockett.send(fname.encode('utf-8'))


            fsize = sockett.recv(Buffer_size).decode()
            fsize = int(fsize)
            #sockett.send(f"{fname}".encode())
            Bprogress = tqdm.tqdm(range(fsize), f"Recibiendo {fname}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(fname, "wb") as f:
                while True:
                    bytes_read = sockett.recv(Buffer_size)

                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    Bprogress.update(len(bytes_read))
            sockett.close()

        #--------------------------LISTAR-------------------------------------
        if KEY == "3":
            print("\n---------------ARCHIVOS LISTADOS-------------------\n")
            list = sockett.recv(Buffer_size).decode()
            list_str = str(list)
            print(list[1:-1])
            print("\n---------------------------------------------------\n")
    

if __name__ == "__main__":
    print("\n")
    print("\n")
    menu()




#GIT
#https://github.com/RizAhmed/tcp-filetransfer/blob/master/client_tcp.py
