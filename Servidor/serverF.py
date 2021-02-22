import socket
import tqdm
import os

sockett = socket.socket()

#Direccion IP OSCAR: 
#LOCAL HOST: 25.121.168.83
#host = '25.121.168.83'

host = "127.0.0.1"

sockett.bind((host, 5757))
sockett.listen(1)
print(f"Escuchando a traves de {'127.0.0.1'}:{'5757'}")

#Aceptar datos enviados por el cliente
client_socket, address = sockett.accept()

print(f"IP: {address} esta conectado...")

#Enviar 4KB 
Buffer_size = 1024 * 4

print("Validando Comparacion...")
client_recv = client_socket.recv(1024)
equal_recv = client_recv.decode('utf-8')
print(equal_recv)


#--------------------------ENVIAR-------------------------------------

if equal_recv == "ENVIAR":
    
    #Recibir datos enviados por el cliente
    received = client_socket.recv(Buffer_size).decode()

    print("Recibido: " + received)
    fname, fsize = received.split(' ')

    fname = os.path.basename(fname)
    #fsize = sys.argv[0]

    print("Nombre: " + fname)

    print("Tamaño:" + fsize)
    fsize = int(fsize)
    print(fsize)
    print("Iniciando servidor...")
    
    #Barra de progreso
    Bprogress = tqdm.tqdm(range(fsize), f"Recibiendo {fname}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(fname, "wb") as f:
        while True:
            bytes_read = client_socket.recv(Buffer_size)

            if not bytes_read:
                break

            f.write(bytes_read)
            Bprogress.update(len(bytes_read))

    client_socket.close()
    sockett.close()


#--------------------------DESCARGAR-------------------------------------
if equal_recv == "DESCARGAR":
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
if equal_recv == "LISTAR":
    path_server = os.listdir(path="/home/dimas/Escritorio/ClienteServidor/Cliente_Servidor-C1/Servidor")
    files = []

    for file in path_server:
        files.append(file)
    
    files_str = str(files)
    bytes_files = files_str.encode('utf-8')
    client_socket.sendall(bytes_files)
    print("Archivos listados...")

    client_socket.close()
    sockett.close()
