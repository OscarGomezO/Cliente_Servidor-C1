import zmq
import sys
import os

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#accion = sys.argv[1]

path_client = "/home/ozkar11/Desktop/Bloc/UTP 10mo Semestre/Arquitectura Cliente-Servidor/Talleres/C-S_Taller1/Cliente/ArchivosCliente"

def upload(action):    
    filename = input("Ingrese nombre del archivo: ")
    print("Subir archivo : {}".format(filename))
    fsize = os.stat(filename).st_size
    print(">>> Nombre del Archivo: ", filename)
    print(">>> Tamaño del Archivo: ", fsize)
    print("Proceso a realizar ", action)
    fsize = str(fsize)
    #mensaje = [filename, fsize]
    bytes = ''
    with open (filename, 'rb') as f:
        bytes = f.read()
    #socket.send_multipart([b'1', f"{mensaje[0]}{mensaje[1]}".encode('utf-8'), bytes])
    socket.send_multipart([action.encode('utf-8'),filename.encode()])
    resp = socket.recv_multipart()
    socket.send_multipart([filename.encode('utf-8'), bytes, fsize.encode('utf-8')])
    #socket.send_multipart([fsize])
    #socket.send_multipart([b'1', filename.encode('utf-8'), bytes])
    resp = socket.recv_multipart()
    print(resp)
    print("Archivo subido correctamente")

def download(action):
    #socket.send(action.encode('utf-8'))
    filename = input("Ingrese el nombre del Archivo a descargar: ")
    print(">>> Nombre del Archivo a Descargar: ", filename)
    action = str(action)
    print("Acción realizada: ", action)
    
    socket.send_multipart([action.encode(),filename.encode('utf-8')])

    #resp = socket.recv_multipart()
    
    #socket.send_multipart([b'DESCARGAR', filename.encode('utf-8')])
    #filenameR = path_client + '/' + m[0].decode('utf-8')
    #print("Descargar Archivo: {}".format(filename))
    *m, fsize = socket.recv_multipart()
    file = path_client + '/' + m[0].decode('utf-8')
    print("Archivo del server: ", m[0])
    with open(file, 'wb') as f:
        f.write(m[0])

    print(">>> Archivo Descargado con Exito...")


def menu():
    print(""" ---------------------------------MENÚ-------------------------------)
    1) ENVIAR Archivo
    2) DESCARGAR Archivo
    3) LISTAR Archivos
    """)
    KEY = input("Elija una Opción: \t")
    if KEY == '1':
        upload("ENVIAR")
    elif KEY == '2':
        download("DESCARGAR")
    else:
        print("No se reconoce la canción")
menu()