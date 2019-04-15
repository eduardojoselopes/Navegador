import socket
import sys
import threading


def handle_client_connection(connection):
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')

    method = string_list[0]
    requesting_file = string_list[1]

    print('Client request ', requesting_file)

    myfile = requesting_file.split('?')[0]
    print(myfile)
    myfile = myfile.lstrip('/')
    if myfile == '':
        myfile = '/index.html'

    try:
        file = open(myfile, 'rb')
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        if myfile.endswith(".jpg"):
            mimetype = 'image/jpg'
        elif myfile.endswith(".png"):
            mimetype = 'image/png'
        elif myfile.endswith(".txt"):
            mimetype = 'text/txt'
        elif myfile.endswith(".mp3"):
            mimetype = 'music/mp3'
        elif myfile.endswith(".pdf"):
            mimetype = 'text/pdf'
        elif myfile.endswith(".css"):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'
        print(header)

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode(
            'utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()


def conecta_servidor(porta, caminho):
    bind_ip = '0.0.0.0'
    bind_port = int(porta)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    print('Listening on {}:{}'.format(bind_ip, bind_port))
    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()


if __name__ == "__main__":
    try:
        caminho = sys.argv[1]
    except:
        print("Não foi adicionado um caminho")
        exit()

    try:
        porta = sys.argv[2]
    except:
        porta = 8080

    if caminho[len(caminho) - 1] != '/':
        caminho = caminho + '/'

conecta_servidor(porta, caminho)