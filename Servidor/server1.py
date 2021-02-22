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
    accion, m = socket.recv_multipart()
    print(">>> Acción del cliente: ", accion)
    print(">>> Nombre Archivo: ", m)
    #print(">>> Nombre del Archivo: ", m[0])
    #print("Tamaño del Archivo: ", fsize)
    #fsize = int(fsize.decode('utf-8'))
    if accion == b'ENVIAR':
        socket.send_multipart([b'Proceso de CARGA iniciado'])
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
        m = str(m)
        m = m.replace("'","")[1:]
        #filename = socket.recv_multipart(int(m))
        #print(">>> Nombre del Archivo: ", m)
        #fsize = os.stat(filename).st_size
        #print("Size:" + str(fsize))
        #Bprogress = tqdm.tqdm(range(fsize), f"Enviando {fname}", unit="B", unit_scale=True, unit_divisor=1024)
        #socket.send(str(fsize).encode('utf-8'))

        #socket.send_string("Proceso de Descarga Iniciado..")
        #filename =  m
        #m = socket.recv_multipart()
        #print("Nombre de Archivo solicitado por el Cliente: ", filename)
        #sRead = filename.read(1024)
        #filename = m.decode('utf-8')
        bytes = ''
        with open(m, 'rb') as f:
            #file = open("Archivos/" + m.decode('utf-8'))
            bytes = f.read(1024)
            #bytes = f.read(filename)
        fsize = os.stat(m).st_size
        fsize = str(fsize)
        print("Tamaño del archivo: ", fsize)
        socket.send_multipart([m.encode('utf-8'), bytes, fsize.encode('utf-8')])
        print(">>> Archivo enviado al Cliente...", m)
else:
    print("Acción no conocidada".format(accion))
