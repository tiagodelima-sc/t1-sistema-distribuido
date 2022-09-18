import socket
import random
from threading import Thread
import time

class gossip_protocol:
    infected_nodes = []

    def __init__(node_current, port, connected_nodes):
        node_current.node = socket.socket(type=socket.SOCK_DGRAM)
        node_current.hostname = socket.gethostname()
        node_current.port = port
        node_current.node.bind((node_current.hostname, node_current.port))       
        node_current.node_available = connected_nodes
        print("Nó A iniciado na porta {0}".format(node_current.port))
        print("Nós possiveis: ", node_current.node_available)

        Thread(target=node_current.digitando_mensagem, name='digitando', daemon=False).start()
        Thread(target=node_current.recebendo_mensagem, name='recebendo', daemon=False).start()

    def digitando_mensagem(node_current):
        while True:
            message_to_send = input("Digite uma mensagem para enviar:\n")
            message_to_send = message_to_send + '\n' + str(node_current.port)       
            node_current.transmitindo_mensagem(message_to_send.encode('utf-8'))

    def recebendo_mensagem(node_current):
        global running
        while True:
            message_to_forward, address = node_current.node.recvfrom(1024)
            if message_to_forward.decode('utf-8') == '@;09Y7b#5^U^zF!':
                pass
            else:
                initial_port = int(message_to_forward.splitlines()[1])
                if node_current.port == initial_port:
                    message_flag = '@;09Y7b#5^U^zF!'
                    message_flag = message_flag.encode()
                    message_to_forward = message_flag
                else:
                    print("Recebendo mensagem...\n")
                    time.sleep(3)    
                    print("\nA mensagem recebida é: {0}.\n Recebido Em [{1}] a partir de [{2}]\n".format(message_to_forward.decode('utf-8').splitlines()[0], time.ctime(time.time()), address[1]))
                node_current.transmitindo_mensagem(message_to_forward)

    def transmitindo_mensagem(node_current, message):
        if not message.decode('utf-8') == '@;09Y7b#5^U^zF!':
            selected_port = random.choice(node_current.node_available)
            print("\n")
            print("=/="*19)
            print("\n")
            print("Nós possiveis: ", node_current.node_available)
            print("Nós infectados: ", gossip_protocol.infected_nodes)
            print("A porta selecionada é [{0}]".format(selected_port))

            node_current.node.sendto(message, (node_current.hostname, selected_port))
            #node_current.node_available.remove(selected_port)
            gossip_protocol.infected_nodes.append(selected_port)

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
