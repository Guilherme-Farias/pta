from socket import *
from os import path, listdir

#preparação de ambiente
users = [line.strip() for line in open("D:/Biblioteca/Desktop/pta/pta-server/users.txt", 'r')]

#Criando conexão com o client
server = socket(AF_INET, SOCK_STREAM)
server.bind(('', 11550))
server.listen(1)

#Inicializando o server sem nenhum usuário conectado
authenticated = False


while True:
    if(not authenticated):
        connection, addr = server.accept()

    msg = connection.recv(1024).decode('ascii')
    code = msg.split()
    try:
        if(code[1] == 'CUMP'):
            if(code[2] in users):
                returnMsg = 'OK'
                authenticated = True
            else:
                returnMsg = 'NOK'

        elif(code[1] == 'LIST'):
            try:
                files = listdir(f'{path.dirname(__file__)}/files')
                returnMsg = "ARQS " + f'{(len(files))} ' + ','.join(files)
            except:
                returnMsg = 'NOK'

        elif(code[1] == 'TERM'):
            try:
                returnMsg = 'OK'
                authenticated = False
            except:
                returnMsg = 'NOK'

        elif(code[1] == 'PEGA'):
            try:
                data = ""
                file_path = f'{path.dirname(__file__)}/files/{code[2]}'
                file = open(file_path, 'r')
                for line in file.readlines():
                    data += line.strip('\n')
                file.close()
                returnMsg = f'ARQ {len(data)} {data}'
            except:
                returnMsg = 'NOK'
        else:
            returnMsg = 'NOK'


        connection.send(f'{code[0]} {returnMsg}'.encode())
    except(KeyboardInterrupt, SystemExit):
        break
connection.shutdown(SHUT_RDWR)
connection.close()