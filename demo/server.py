import socketserver
import threading
import time


class ChatServer(socketserver.BaseRequestHandler):
    # static variable, do not visit directly
    all_clients = []

    def setup(self):
        ChatServer.all_clients.append(self.request)
        ChatServer.broadcast('Client joined: %s' % str(self.client_address))

    def handle(self):
        self.log('Handle new connection from %s' % str(self.client_address))
        while True:
            try:
                data = self.request.recv(1024)
                if data != b'':
                    self.log('Received from %s: %s' % (str(self.client_address), data))
                    ChatServer.broadcast('%s: %s' % (str(self.client_address), data))
                else:
                    raise Exception
            except Exception as e:
                raise(e)
                break

    def finish(self):
        if self.request in ChatServer.all_clients:
            ChatServer.all_clients.remove(self.request)
            ChatServer.broadcast('Client left: %s' % str(self.client_address))

    @staticmethod
    def broadcast(msg):
        try:
            if ChatServer.all_clients:
                for socket in ChatServer.all_clients:
                    try:
                        socket.send(msg.encode('utf-8'))
                    except:
                        pass
        except:
            pass

    @staticmethod
    def log(msg, level=1):
        level_table = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
        print(
            '[%s][%s][%s] %s' % (
                hash(threading.current_thread()), time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                level_table[level], msg))


if __name__ == '__main__':
    try:
        print('[%s][%s][%s] %s' % (
            hash(threading.current_thread()), time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
            'INFO', 'Initiating server...'))
        app = socketserver.ThreadingTCPServer(('0.0.0.0', 1030), ChatServer)
        app.serve_forever()
    except OSError:
        ChatServer.log('Port occupied', 4)
    except:
        ChatServer.log('Unexpected error', 4)
