import argparse
import socketserver
import threading
import time

import session_manager
import socket_tools
import user_manager


class ChatRequestHandler(socketserver.BaseRequestHandler):
    # 静态字典，以username为键，以对应ChatRequestHandler类的指针为值
    # 不需要追踪未登陆的客户端，所以这里只存储已完成登陆的客户端
    All_Auth_Clients = dict()

    def setup(self):
        # 由父级类在接受新传入连接时执行
        self.authed = False
        self.username = ''
        self.file_peer = ''
        self.log('Accept new connection')
        # instance state flag: is_authenticated

    def handle(self):
        while True:
            try:
                data = socket_tools.recv(self.request)
                if not self.authed:
                    # client not authed
                    if data['cmd'] == 'login':
                        r = user_manager.validate(data['usr'], data['pwd'])
                        self.username = data['usr']
                        if r == 0 and data['usr'] not in ChatRequestHandler.All_Auth_Clients.keys():
                            socket_tools.send(self.request, {'response': 'ok'})
                            self.authed = True
                            for username in ChatRequestHandler.All_Auth_Clients.keys():
                                socket_tools.send(ChatRequestHandler.All_Auth_Clients[username].request,
                                                  {'type': 'peer_joined', 'peer': self.username})
                            ChatRequestHandler.All_Auth_Clients[self.username] = self
                            self.log('Authenticated successfully')
                        elif data['usr'] in ChatRequestHandler.All_Auth_Clients.keys():
                            socket_tools.send(self.request, {'response': 'fail', 'reason': 'User is already online'})
                            self.log('Authenticated failed: user is already online')
                        elif r == 1:
                            socket_tools.send(self.request,
                                              {'response': 'fail', 'reason': 'Invalid username or password'})
                            self.log('Authenticated failed: invalid password')
                        elif r == 2:
                            socket_tools.send(self.request,
                                              {'response': 'fail', 'reason': 'Invalid username or password'})
                            self.log('Authenticated failed: user not exists')
                    elif data['cmd'] == 'face_login':
                        self.username = user_manager.get_name_from_face(data['face'])
                        if self.username != '' and self.username not in ChatRequestHandler.All_Auth_Clients.keys():
                            self.authed = True
                            for username in ChatRequestHandler.All_Auth_Clients.keys():
                                socket_tools.send(ChatRequestHandler.All_Auth_Clients[username].request,
                                                  {'type': 'peer_joined', 'peer': self.username})
                            ChatRequestHandler.All_Auth_Clients[self.username] = self
                            socket_tools.send(self.request, {'response': 'ok', 'username': self.username})
                            self.log('Face recognized successfully')
                        elif self.username == '':
                            socket_tools.send(self.request, {'response': 'fail', 'reason': 'Cannot recognize face'})
                            self.log('Face recognition failed: face not exists')
                        else:
                            socket_tools.send(self.request, {'response': 'fail', 'reason': 'User already online'})
                            self.log('Face recognition failed: user already online')
                    elif data['cmd'] == 'register':
                        r = user_manager.register(data['usr'], data['pwd'], data['face'])
                        self.username = data['usr']
                        if r == 0:
                            socket_tools.send(self.request, {'response': 'ok'})
                            self.log('Register successfully')
                        elif r == 1:
                            socket_tools.send(self.request, {'response': 'fail', 'reason': 'User already exists'})
                            self.log('Authenticated failed: user exists')
                    elif data['cmd'] == 'chg_pwd':
                        r = user_manager.change_pwd(data['usr'], data['old'], data['new'])
                        self.username = data['usr']
                        if r == 0:
                            socket_tools.send(self.request, {'response': 'ok'})
                            self.log('Change password successfully')
                        elif r == 1:
                            socket_tools.send(self.request,
                                              {'response': 'fail', 'reason': 'Invalid username or password'})
                            self.log('Changed password failed: invalid password')
                        elif r == 2:
                            socket_tools.send(self.request,
                                              {'response': 'fail', 'reason': 'Invalid username or password'})
                            self.log('Change password failed: user not exists')
                    else:
                        raise socket_tools.ProtocolException
                else:
                    if data['cmd'] == 'list_users':
                        users = []
                        for u in ChatRequestHandler.All_Auth_Clients.keys():
                            if u != self.username:
                                users.append(u)
                        socket_tools.send(self.request, {'type': 'list_users', 'data': users})
                    elif data['cmd'] == 'get_history':
                        socket_tools.send(self.request, {'type': 'get_history', 'peer': data['peer'],
                                                         'data': session_manager.get_history(self.username,
                                                                                             data['peer'])})
                    elif data['cmd'] == 'chat' and data['peer'] != '':
                        # normal chat
                        if data['peer'] in ChatRequestHandler.All_Auth_Clients.keys():
                            # peer exists
                            socket_tools.send(ChatRequestHandler.All_Auth_Clients[data['peer']].request,
                                              {'type': 'message', 'peer': self.username, 'msg': data['msg']})
                            session_manager.append_history(self.username, data['peer'], data['msg'])
                            self.log('Messaged to %s: %s' % (data['peer'], data['msg']))
                    elif data['cmd'] == 'chat' and data['peer'] == '':
                        # broadcast
                        for username in ChatRequestHandler.All_Auth_Clients.keys():
                            if username != self.username:
                                socket_tools.send(ChatRequestHandler.All_Auth_Clients[username].request,
                                                  {'type': 'broadcast', 'peer': self.username, 'msg': data['msg']})
                        session_manager.append_history(self.username, '', data['msg'])
                        self.log('Broadcasted: %s' % data['msg'])
                    elif data['cmd'] == 'file_request':
                        if data['peer'] in ChatRequestHandler.All_Auth_Clients.keys():
                            # peer exists
                            ChatRequestHandler.All_Auth_Clients[data['peer']].file_peer = self.username
                            socket_tools.send(ChatRequestHandler.All_Auth_Clients[data['peer']].request,
                                              {'type': 'file_request', 'peer': self.username,
                                               'filename': data['filename'], 'size': data['size'], 'md5': data['md5']})
                            self.log(
                                'Request to send a %s file %s to %s' % (data['size'], data['filename'], data['peer']))
                    elif data['cmd'] == 'file_deny' and data['peer'] == self.file_peer:
                        self.file_peer = ''
                        if data['peer'] in ChatRequestHandler.All_Auth_Clients.keys():
                            # peer exists
                            socket_tools.send(ChatRequestHandler.All_Auth_Clients[data['peer']].request,
                                              {'type': 'file_deny', 'peer': self.username})
                            self.log('Denied file from ' + data['peer'])
                    elif data['cmd'] == 'file_accept' and data['peer'] == self.file_peer:
                        self.file_peer = ''
                        if data['peer'] in ChatRequestHandler.All_Auth_Clients.keys():
                            # peer exists
                            self.log(ChatRequestHandler.All_Auth_Clients[data['peer']].request)
                            socket_tools.send(ChatRequestHandler.All_Auth_Clients[data['peer']].request,
                                              {'type': 'file_accept',
                                               'ip': self.client_address[
                                                   0]})
                            self.log('Accepted file from ' + data['peer'])
                    else:
                        raise socket_tools.ProtocolException
            except socket_tools.DisconnectException:
                break
            except socket_tools.ProtocolException:
                self.log("Client is not compatible with protocol", 2)
                break
            except Exception as e:
                self.log(
                    'Exception occurs while handling incoming data:\n%s' % str(e), 3)
                break

    def finish(self):
        # 由父级类在连接断开时执行，不需要手工检测连接状态或调用此方法
        if self.authed:
            del ChatRequestHandler.All_Auth_Clients[self.username]
            for username in ChatRequestHandler.All_Auth_Clients.keys():
                socket_tools.send(ChatRequestHandler.All_Auth_Clients[username].request,
                                  {'type': 'peer_left', 'peer': self.username})
        self.log('Client disconnected')

    def log(self, msg, level=1):
        level_table = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
        if self.username == '':
            print(
                '[%s][%s][%s][%s] %s' % (
                    hash(threading.current_thread()), time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                    level_table[level], self.client_address[0] + ":" + str(self.client_address[1]),
                    msg))
        else:
            print(
                '[%s][%s][%s][%s] %s' % (
                    hash(threading.current_thread()), time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                    level_table[level], self.username, msg))


def log(msg, level=1):
    level_table = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
    print(
        '[%s][%s][%s][SYSTEM] %s' % (
            hash(threading.current_thread()), time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
            level_table[level], msg))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--purge', help='Purge data', type=str, choices=['user', 'chat', 'all'])
        args = parser.parse_args()
        if args.purge == 'user':
            user_manager.purge_all()
            log('Purge user data')
        elif args.purge == 'chat':
            session_manager.purge_all()
            log('Purge chat history')
        elif args.purge == 'all':
            user_manager.purge_all()
            session_manager.purge_all()
            log('Purged all data')
        log('Loading data')
        user_manager.load_from_file()
        session_manager.load_from_file()
        log('Start to listen')
        app = socketserver.ThreadingTCPServer(('0.0.0.0', 1030), ChatRequestHandler)
        app.serve_forever()
    except OSError:
        log('Port is occupied', 4)
    except Exception as e:
        log('Unknown error: ' + str(e), 4)
