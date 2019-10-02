import socket
import struct
from threading import Thread
import os.path

clients = []

class Server(Thread):
    def __init__(self, socket):
        super().__init__(daemon=True)
        self.socket = socket

    def run(self): #overwriting standart method to what we need
        while True:
            self.recv_msg()

    def new_filename(self, filename):
        if os.path.isfile(filename):
            i = 0
            new_filename = filename
            while os.path.isfile(new_filename):#dealing with duplicates
                i += 1
                new_filename = filename.split('.')[-2] + "_copy" + str(i) + '.' + filename.split('.')[-1]
            filename = new_filename
        filename = open( filename, 'wb')
        return filename

#sps internet that I can sleep tonight
    def recv_msg(self):
        raw_msglen = self.recvall(4) #receiving filename length
        if not raw_msglen:
            return None
        print('Receiving new file')
        filenamelength = struct.unpack('>I', raw_msglen)[0]
        filename = self.recvall(filenamelength).decode()
        f = self.new_filename(filename)
        raw_msglen = self.recvall(4)#receiving file length
        if not raw_msglen:
            return None
        filelength = struct.unpack('>I', raw_msglen)[0]
        reclen = 0
        while reclen < filelength:
            f.write(self.recvall(1024))
            reclen += 1024
        f.close()

    def recvall(self, n):
        data = b'' #binary string
        while len(data) < n: #iterating over file
            packet = self.socket.recv(n - len(data))
            if not packet:
                return data
            data += packet
        return data


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()
    while True:
        con, addr = sock.accept()
        clients.append(con)
        Server(con).start()
