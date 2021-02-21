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

    #accion, *m, fsize = socket.recv_multipart()
    accion = socket.recv()
    print(">>> Acción del cliente: ", accion)
    #print(">>> Nombre del Archivo: ", m[0])
    #print("Tamaño del Archivo: ", fsize)
    #fsize = int(fsize.decode('utf-8'))
    if accion == b'ENVIAR':
        socket.send_multipart([b'Proceso de CARGAR iniciado'])
        *m, fsize = socket.recv_multipart()
        #Bprogress = tqdm.tqdm(range(fsize), f"Recibiendo {m[0]}", unit="B", unit_scale=True, unit_divisor=1024)
        #filename = open("Archivos/" + m[0].decode('utf-8'), "rb")
        #sRead = filename.read(1024)
        filename = path_server + '/' + m[0].decode('utf-8')
        with open(filename, 'wb') as f:
            f.write(m[1])
        #Bprogress.update()
        socket.send_multipart([b'>>> Archivo guardado en Server'])
    if accion == b"DESCARGAR":
        print(">>> Descarga en Proceso...")
        filename = open("Archivos/" + m[0].decode('utf-8'))
        print("Nombre de Archivo solicitado por el Cliente: ", filename)
        #sRead = filename.read(1024)
        bytes = ''
        with open(filename, 'rb') as f:
            filename = open("ArchivosCliente/" + m[0].decode('utf-8'))
            bytes = filename.read(1024)
            #bytes = f.read(filename)
        socket.sned_multipart([filename.encode('utp-8'), bytes])
        print(">>> Archivo envia al Cliente...")
    else:
        print("Acción no conocidad".format(accion))
