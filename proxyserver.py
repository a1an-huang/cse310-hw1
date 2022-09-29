from socket import *

port = 8888

serverSocket = socket(AF_INET, SOCK_STREAM)  # client server socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)

print(f'web server active on port {port}')

while True:

    print("connection established")
    connectionSocket, addr = serverSocket.accept()

    sentence = connectionSocket.recv(4096)
    filename = sentence.decode().split()[1][1:]
    cacheExist = 1

    try:
        f = open(filename + ".txt", "r")  
        output = f.readlines()  
        cacheExist = 0
        connectionSocket.send(("HTTP/1.1 200 OK\r\n").encode())  
        connectionSocket.send(("Content-Type:text/html\r\n").encode())
        for line in output:  
            connectionSocket.send(line.encode())
        print('Read from cache')

    except IOError:
        if cacheExist == 1:
            print('does not exist')
            proxySocket = socket(AF_INET, SOCK_STREAM)  

            try:
               
                proxySocket.connect((gethostbyname(filename), 80))
                proxySocket.send(('GET /' + filename.partition('/')[2] + ' HTTP/1.1\nHost: ' + filename.partition(
                    '/')[0] + ' \n\n').encode())  
                reply = proxySocket.recv(4096) 
                reply = (reply.decode().partition('<')[
                         1] + reply.decode().partition('<')[2]) 
                tmpFile = open(filename + ".txt", "w")  
                for line in reply.splitlines():  
                    tmpFile.write(line + "\n")
                tmpFile.close()
                tmpFile = open(filename + ".txt", "r")
                buffer = tmpFile.read()
                tmpFile.close()
                connectionSocket.send(buffer.enocde())  

            except:
                print("Illegal request")

        else:
            # 404 error if not found
            connectionSocket.send("HTTP/1.0 404 sendErrorErrorError\r\n")
            connectionSocket.send("Content-Type:text/html\r\n")
            connectionSocket.send("\r\n")
            connectionSocket.close()
            serverSocket.close()
