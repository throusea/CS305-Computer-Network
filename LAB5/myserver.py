from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')

while True:
    msg, clientAddr = serverSocket.recvfrom(2048)
    modifiedMessage = msg.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddr)
    