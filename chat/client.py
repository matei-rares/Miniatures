#conexiune cu socket
import socket
import threading
import sys

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def close(self):
        self.sock.close()
        sys.exit()

    def receive(self):
        return self.sock.recv(1024)

#using the socket, we connect to server and with threads we listen and send messages
#the client can send messages to the server and receive messages from the server
while True:
    try:
        client = Client('localhost', 10000)
    except KeyboardInterrupt:
        client.close()
        break
    except Exception as e:
        print(e)
        break
    except:
        break
    finally:
        client.close()
        break

