import socket

PORT = 8080
HOST = "localhost"
USERNAME = 'admin'
PASSWORD = '123'
HEADER_HTTP_200 = 'HTTP/1.1 200 OK\r\nContent-Type: ; charset: utf-8\r\n\r\n'
HEADER_HTTP_401 = 'HTTP/1.1 401 Unauthorized \r\nContent-Type: ; charset: utf-8\r\n\r\n'
HEADER_HTTP_404 = 'HTTP/1.1 404 Not Found \r\nContent-Type: ; charset: utf-8\r\n\r\n'

# Criando o socket do servidor | [IPV4 / TCP].
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def management(conn, addr):
    # Função responsável por gerenciar a conexão entre o cliente e o servidor.
    # Recebe uma requisição e retornando uma resposta.
    print("Cliente", addr, "conectado")
    print('\t')
    connected = True
    while connected:
        # Recebemos a requisição, a decodificamos e atribuímos a variável msg.
        # A partir do índice da porta obtemos a URL enviada na requisição.
        # Essa URL serve como parâmetro para que o servidor responda o cliente.
        msg = conn.recv(1024).decode()
        indice = msg.find('5000/')+6
        path = msg[indice:msg.find(' HTTP/1.1')]

        # Definimos os possíveis caminhos que o servidor ira responder.
        # GET com a URL vazia atribuiremos o caminho a tela de login.
        # POST com a '/' atribuimos a home.
        # path recebe o caminho para o arquivo solicitado baseando-se na URL.
        if path == "":
            path = "html/login.html"

        if path == "/":
            path = "html/home.html"

        try:
            # A partir do path tentamos abrir e manipular o arquivo solicitado.
            # Utilizando o HEADER do request definimos se foi um GET ou POST.
            if msg[0:3] == "GET":
                # Abrimos o arquivo solicitado, utilizando utf8 como encoding.
                # Atribuímos o arquivo e o HEADER de sucesso a variável data.
                # Fechamos o arquivo e enviamos a variável data ao cliente.
                file = open(path, encoding="utf8", errors='ignore')
                data = HEADER_HTTP_200
                data += file.read()
                file.close()
                conn.send(data.encode())

            if msg[0:4] == 'POST':
                print(msg)
                print('\t')

                # Obtemos o 'username' e 'password' através do POST.
                indexUsername = msg.find("username")
                username = msg[indexUsername+9:]
                username = username.partition('&')[0]

                indexPassword = msg.find("password")
                password = msg[indexPassword+9:]

                if username == USERNAME and password == PASSWORD:
                    # Mesmo procedimento do GET.
                    # Ocorrendo apenas quando as credências batem.
                    file = open(path, encoding="utf8", errors='ignore')
                    data = HEADER_HTTP_200
                    data += file.read()
                    file.close()
                    conn.send(data.encode())
                else:
                    # Caso as credenciais não sejam as mesmas.
                    # Sobrescrevemos a variável path, passando a tela de erro.
                    # Semelhante ao GET apenas mudando o cabeçalho.
                    path = "html/401.html"
                    file = open(path, encoding="utf8", errors='ignore')
                    data = HEADER_HTTP_401
                    data += file.read()
                    file.close()
                    conn.send(data.encode())

        except:
            # Ocorre quando não é possível abrir o arquivo solicitado.
            # Neste caso retornamos o arquivo referente ao 404.
            # Junto ao cabeçalho descrevendo o erro.
            path = "html/404.html"
            file = open(path, encoding="utf8", errors='ignore')
            data = HEADER_HTTP_404
            data += file.read()
            file.close()
            conn.send(data.encode())
        connected = False
    conn.close()


def run():
    # Função responsável por iniciar o servidor.
    # Aqui definimos em qual HOST e porta o servidor estará ouvindo.
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server: http://{HOST}:{PORT}")
    print("Shutdown: Ctrl + C")
    while True:
        # Essa laço infinito fara com que o servidor aceite todas as conexões.
        # Chamando a função management, passando o cliente e o endereço.
        conn, addr = server.accept()
        management(conn, addr)


print("Server is Running")
run()
