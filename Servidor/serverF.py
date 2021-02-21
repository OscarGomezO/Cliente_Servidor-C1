import os
from os import path
import zmq
import sys
import socket
import tqdm


sockett = socket.socket()

host = '127.0.1.1' # Local IP
#host = '25.121.154.185' # Local REMOTA
port = 9000
sockett.bind((host, port))
sockett.listen(5)
print(f"Escuchando a traves de {host}:{'9000'}")

#Aceptar datos enviados por el cliente
client_socket, address = sockett.accept()

print(f"IP: {address} esta conectado...")

#Enviar 4KB 
Buffer_size = 1024 * 4

print("Validando Comparacion...")
client_recv = client_socket.recv(1024).decode('utf-8')
#equal_recv = client_recv.decode('utf-8')
print("Selección N°: ", client_recv)

path_server = os.listdir(path="/home/ozkar11/Desktop/Bloc/UTP 10mo Semestre/Arquitectura Cliente-Servidor/Talleres/C-S_Taller1/Servidor/Archivos")
files = sys.argv[path_server]
print("Carpeta del Servidor", files)

#--------------------------ENVIAR-------------------------------------
def menuServ():
    while True:
        
        if client_recv == "1":
            received = client_socket.recv(Buffer_size).decode()
            print(">>> ENVIO")
            #Recibir datos enviados por el cliente
            

            print("Recibido: " + received)
            fname, fsize = received.split(' ')

            fname = os.path.basename(fname)
            #fsize = sys.argv[0]

            print(">>> Nombre Archivo: " + fname)

            print(">>> Tamaño Archivo:" + fsize)
            fsize = int(fsize)
            print("****Iniciando servidor...")

            #----PATH----------------------
            
            with open(fname, "wb") as f:
                #Barra de progreso
                Bprogress = tqdm.tqdm(range(fsize), f"Recibiendo {fname}", unit="B", unit_scale=True, unit_divisor=1024)

                while True:
                    bytes_read = client_socket.recv(Buffer_size)

                    if not bytes_read:
                        break

                    #f.write(bytes_read)
                    bytes_read.write(path_server)
                    Bprogress.update(len(bytes_read))
            client_socket.close()
            sockett.close()
            print("Archivo recibido con Exito.")
        client_socket.close()
            
"""
        #--------------------------DESCARGAR-------------------------------------
        if equal_recv == "2":
            fname = client_socket.recv(Buffer_size).decode()
            print("filename:" + fname)
            fsize = os.stat(fname).st_size
            print("Size:" + str(fsize))
            Bprogress = tqdm.tqdm(range(fsize), f"Enviando {fname}", unit="B", unit_scale=True, unit_divisor=1024)
            client_socket.send(str(fsize).encode('utf-8'))
            
            with open(fname, "rb") as f:
                
                while True:
                    bytes_read = f.read(Buffer_size)

                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)
                    Bprogress.update(len(bytes_read))

            client_socket.close()
            sockett.close()

        #--------------------------LISTAR-------------------------------------
        if equal_recv == "3":
            path_server = os.listdir(path="/home/ozkar11/Desktop/Bloc/UTP 10mo Semestre/Arquitectura Cliente-Servidor/Talleres/C-S_Taller1/Servidor/Archivos")
            files = []

            for file in path_server:
                files.append(file)
            
            files_str = str(files)
            bytes_files = files_str.encode('utf-8')
            client_socket.sendall(bytes_files)
            print("Archivos listados...")

            client_socket.close()
            sockett.close()
"""

if __name__ == "__main__":
    menuServ()