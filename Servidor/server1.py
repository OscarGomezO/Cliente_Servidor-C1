import zmq
import sys
import os.path
import tqdm

context = zmq.Context()
socket = context.socket(zmq.REP)
#host = '127.0.1.1' # Local IP
#port = 9000
#socket.bind((host, port))
socket.bind("tcp://*:5555")
#files = sys.argv[path_server]

while True:
    #path_server = os.listdir(path="/home/ozkar11/Desktop/Bloc/UTP 10mo Semestre/Arquitectura Cliente-Servidor/Talleres/C-S_Taller1/Servidor/Archivos")
    path_server = "/home/ozkar11/Desktop/Bloc/UTP 10mo Semestre/Arquitectura Cliente-Servidor/Talleres/C-S_Taller1/Servidor/Archivos"
    #client_recv = socket.recv(1024).decode()
    print("Servidor listo!")
    #print("Carpeta de archivos Server: ", path_server)

    accion, *m, fsize = socket.recv_multipart()
    print(">>> Acción del cliente: ", accion)
    print(">>> Nombre del Archivo: ", m[0])
    
    print("Tamaño del Archivo: ", fsize)
    if accion == b'1':
        
        #filename = open("Archivos/" + m[0].decode('utf-8'), "rb")
        #sRead = filename.read(1024)
        filename = path_server + '/' + m[0].decode('utf-8')
        with open(filename, 'wb') as f:
            f.write(m[1])
        socket.send_multipart([b'>>> Archivo guardado en Server'])
    else:
        print("Acción no conocidad".format(accion))
