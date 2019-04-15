import socket
import sys
import select
from trata_dados import ProcessaDadosURL


def nome_sem_diretorio(url):
    url = url.decode()
    try:
        p = url.index('www')
        i = 5
    except:
        i = 0

    nome = []
    while url[i] != '.':
        nome.append(url[i])
        i = i + 1
        if i >= len(url) - 1:
            break

    return 'Downloads/' + ''.join(nome) + '.html'


def nome_com_diretorio(path):
    path = path.decode()
    extensoes = ['.txt', '.mp3', '.pdf', '.html', '.jpg', '.png']
    path = path.split('/')
    for nome in path:
        if len(nome) > 4:
            if nome[-4:] in extensoes:
                return 'Downloads/' + nome

    return "Downloads/arquivo_generico"


def analisa_erro(response):
    erros = {"302": "302 Found",
             "404": "404 Not Found",
             "301": "301 Moved Permanently",
             "401": "401 Unauthorized",
             "400": "400 Bad Request",
             "403": "403 Forbidden",
             "500": "500 Internal Server Error",
             "504": "504 Gateway Timeout",
             "501": "501 Not Implemented",
             "502": "502 Bad Gateway",
             "503": "503 Service Unavailable"}

    if response in erros.keys():
        print(erros[response])
        exit(1)


def conecta_site(host, path, porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(porta)))
    host, path = host.encode(), path.encode()
    s.sendall(b'GET /%b HTTP/1.1\r\nHOST: %b\r\n\r\n' % (path, host))

    reply = b''

    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data:
            break
        reply += data
    print(reply)

    headers = reply.split(b'\r\n\r\n')[0]
    mensagem = reply[len(headers) + 4:]

    erro = headers.decode().split()
    analisa_erro(erro[1])

    if len(path) != 0:
        nome_arq = nome_com_diretorio(path)
        arq_saida = open(nome_arq, 'wb')
    else:
        nome_arq = nome_sem_diretorio(host)
        arq_saida = open(nome_arq, 'wb')

    arq_saida.write(mensagem)
    arq_saida.close()


def conecta_servidor(busca, porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(porta)))
    busca = busca.encode()

    s.sendall(b'GET /Downloads/%b HTTP/1.1\r\n' % (busca))

    reply = b''

    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data:
            break
        reply += data
    print(reply)

    headers = reply.split(b'\r\n\r\n')[0]

    erro = headers.decode().split()
    analisa_erro(erro[1])


if '__main__' == __name__:
    conexao = sys.argv[1]
    url = sys.argv[2]
    try:
        porta = sys.argv[3]
    except:
        porta = 80

    if conexao == 'navegador':
        host, path = ProcessaDadosURL(url).separa_nome_diretorio()
        conecta_site(host, path, porta)
    elif conexao == 'servidor':
        host, path = ProcessaDadosURL(url).separa_nome_diretorio()
        print(f'host: {host}, path: {path}')
        print(f'url: {url}')

        conecta_servidor(url, porta)

    else:
        print("Opção inválida!")
exit(404)