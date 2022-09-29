from socket import *

port = 6789

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(1)

print(f'web server active on port {port}')

while True:

    print('connection established')
    connectionSocket, address = serverSocket.accept()

    try:

        message = connectionSocket.recv(1024)

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        connectionSocket.send('\nHTTP 200 OK\n\n'.encode())
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        connectionSocket.send("\nHTTP 404 Not Found\n\n".encode())
        connectionSocket.close()

serverSocket.close()
