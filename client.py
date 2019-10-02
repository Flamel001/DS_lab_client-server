import socket
import struct
import sys


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip,port))

    def send(self, filename):
        name = struct.pack('>I',len(filename)) + filename.encode() #struct.pack because we need container to send file
        self.socket.send(name) #send filename
        file = open(filename, 'rb')
        length = len(file.read())
        file.close()
        with open(filename, 'rb') as file:
            toSend = struct.pack('>I', length)
            self.socket.send(toSend) #send filelength
            counter = 0
            while True:
                chunk = file.read(1024)
                if not chunk: #when we meet end of file
                    break
                self.socket.send(chunk) #finally send file
                counter = counter + 1
                percentage = counter*100*1024/length
                print('Progress:',percentage if percentage<100 else 100,'%')

if __name__ == "__main__":
    client = Client(sys.argv[2], int(sys.argv[3]))
    client.send(sys.argv[1])
