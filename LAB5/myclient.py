from pydoc import cli
from socket import *
serverName = '10.24.181.129'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
msg = input('Input lowercase sentence:')
clientSocket.sendto(msg.encode(), (serverName, serverPort))
modifiedMessage, serverAddr = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()