import socket
import random
from threading import Thread
import threading
import time

stop_thread = threading.Event()

class gossip_protocol:
    infected_nodes = []
    
    def __init__(node_current, port, connected_nodes):
        
        # uma instância do socket
        # usar SOCK_DGRAM para estabelecer protocolo sem conexão
        
        node_current.node = socket.socket(type=socket.SOCK_DGRAM)
        
        # defina o endereço
        node_current.hostname = socket.gethostname()
        node_current.port = port
        node_current.node.bind((node_current.hostname, node_current.port))       
        node_current.node_available = connected_nodes
        print("Nó A iniciado na porta {0}".format(node_current.port))
        print("Nós possiveis: ", node_current.node_available)
        # executando as thread
        Thread(target=node_current.digitando_mensagem).start()
        Thread(target=node_current.recebendo_mensagem).start()

    def digitando_mensagem(node_current):
        while True:
            # recebe a msg que o usuario digitar
            message_to_send = input("Digite uma mensagem para enviar:\n")
            message_to_send = message_to_send + '\n' + str(node_current.port)         
            node_current.transmitindo_mensagem(message_to_send.encode('utf-8'))

    def recebendo_mensagem(node_current):
        while True:
            # definindo o tamanho do buffer que deve aceitar, utilizando udp
            message_to_forward, address = node_current.node.recvfrom(1024)
            initial_port = int(message_to_forward.splitlines()[1])
            
            # node_current.node_available.remove(address[1])
            # gossip_protocol.infected_nodes.append(address[1])
            
            # definindo um intervalo de 3s            
            time.sleep(3)
            
            if node_current.port == initial_port:
                print('Ciclo finalizado')
                for thread in threading.enumerate(): 
                    thread.join()
                    # print(thread.name)
                    # Corrigir
                break

            # recebe a mensagem do outro nó
            print("Recebendo mensagem...\n")          
            print("\nA mensagem recebida é: {0}.\n Recebido Em [{1}] a partir de [{2}]\n".format(message_to_forward.decode('utf-8').splitlines()[0], time.ctime(time.time()), address[1]))
            node_current.transmitindo_mensagem(message_to_forward)

    def transmitindo_mensagem(node_current, message):
        while node_current.node_available:
            # sorteia e escolhe uma porta dos nó disponiveis para enviar a msg
            selected_port = random.choice(node_current.node_available)
            print("\n")
            print("=/="*19)
            print("\n")
            print("Nós possiveis: ", node_current.node_available)
            print("Nós infectados: ", gossip_protocol.infected_nodes)
            print("A porta selecionada é [{0}]".format(selected_port))
            # envia os dados da msg atraves do metodo sendto
            node_current.node.sendto(message, (node_current.hostname, selected_port))
            # node_current.node_available.remove(address[1])
            # gossip_protocol.infected_nodes.append(address[1])

            print(f"A mensagem '{message.decode('utf-8').splitlines()[0]}' está sendo enviada para [{selected_port}].")
            print("\n")
            print("=/="*19)
            time.sleep(3)
            print("\n")

    
class inicializandoOsValores:
     gossip_protocol
     port = int(input('Porta: '))
     vizinho = int(input('Porta - Vizinho: '))
     print('\n')
     connected_nodes = []
     connected_nodes.append(vizinho)
     node = gossip_protocol(port, connected_nodes)
