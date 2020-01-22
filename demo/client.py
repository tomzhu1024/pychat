import socket
import threading
import time
from tkinter import *


class MainWindow(object):
    def __init__(self):
        # create window frame
        self.__root = Tk()
        self.__root.title('PyChat Client')
        self.__root.geometry('360x450+200+100')
        self.__root.resizable(width=False, height=True)
        self.__root.minsize(360, 400)
        self.__root.maxsize(360, 1000)

        # public event callback handles
        self.on_connection_cb = None
        self.on_send_cb = None
        self.on_closing_cb = None

        # register on closing event handle
        self.__root.protocol('WM_DELETE_WINDOW', self.__on_closing)

        # public properties
        self.server_addr = StringVar()
        self.server_port = StringVar()
        self.msg_to_send = StringVar()
        self.msg_history = []
        self.msg_history_cursor = 0

        # frame layout
        self.__frame_root = Frame(self.__root)
        self.__frame_root.pack(fill=BOTH)
        self.__frame_msg = Frame(self.__frame_root)
        self.__frame_control = Frame(self.__frame_root)
        self.__frame_input = Frame(self.__frame_root)
        self.__frame_last = Frame(self.__frame_root)
        self.__frame_control.pack(side=TOP, fill=X, expand=YES)
        self.__frame_input.pack(side=BOTTOM, fill=X, expand=YES, anchor=S)
        self.__frame_msg.pack(side=TOP, fill=BOTH, expand=YES)

        # hint label
        Label(self.__frame_control, text='Server: ').pack(side=LEFT)

        # create server address entry
        self.__addr_entry = Entry(self.__frame_control, font=('Century', 12), width=16, textvariable=self.server_addr)
        self.__addr_entry.bind('<Return>', func=lambda event: self.on_connection_cb(event) if self.__connection_button[
                                                                                                  'state'] == 'normal' else ())
        self.__addr_entry.pack(side=LEFT, fill=Y, expand=NO)
        self.server_addr.set('127.0.0.1')

        # create colon between address and port
        Label(self.__frame_control, text=':').pack(side=LEFT)

        # create server port entry
        self.__port_entry = Entry(self.__frame_control, font=('Century', 12), width=7,
                                  textvariable=self.server_port)
        self.__port_entry.bind('<Return>', func=lambda event: self.on_connection_cb(event) if self.__connection_button[
                                                                                                  'state'] == 'normal' else ())
        self.__port_entry.pack(side=LEFT, fill=Y)
        self.server_port.set('1030')

        # create connection button
        self.__connection_button = Button(self.__frame_control, text='Connect', width=35)
        self.__connection_button.bind('<Button-1>',
                                      func=lambda event: self.on_connection_cb(event) if self.__connection_button[
                                                                                             'state'] == 'normal' else ())
        self.__connection_button.pack(side=RIGHT)

        # create messages text and scrollbar
        self.__msg_text = Text(self.__frame_root, height=100)
        self.__msg_scrollbar = Scrollbar(self.__frame_root)
        self.__msg_text.configure(state='disabled')
        self.__msg_text.bind('<1>', lambda event: self.__msg_text.focus_set())
        self.__msg_text.config(yscrollcommand=self.__msg_scrollbar.set)
        self.__msg_scrollbar.pack(side=RIGHT, fill=Y)
        self.__msg_text.pack(side=LEFT)
        self.__msg_scrollbar.config(command=self.__msg_text.yview)
        # configure format tags
        self.__msg_text.tag_configure('client', foreground='#3bc63d', font=('Century', 10))
        self.__msg_text.tag_configure('server', foreground='#ba1e16', font=('Century', 10))
        self.__msg_text.tag_configure('system', foreground='#969696', font=('Century', 10))

        # create input entry
        self.__msg_entry = Entry(self.__frame_input, font=('Century', 12), textvariable=self.msg_to_send)
        self.__msg_entry.bind('<Return>', func=lambda event: self.on_send_cb(event) if self.__connection_button[
                                                                                           'state'] == 'normal' else ())
        self.__msg_entry.bind('<Up>',
                              func=self.__prev_msg if self.__connection_button['state'] == 'normal' else ())
        self.__msg_entry.bind('<Down>',
                              func=self.__next_msg if self.__connection_button['state'] == 'normal' else ())
        self.__msg_entry.pack(side=LEFT, fill=BOTH, expand=YES)

        # create send button
        self.__send_button = Button(self.__frame_input, text='Send', width=8)
        self.__send_button.bind('<Button-1>', func=lambda event: self.on_send_cb(event) if self.__connection_button[
                                                                                               'state'] == 'normal' else ())
        self.__send_button.pack(side=LEFT)

        # create clear button
        self.__clear_button = Button(self.__frame_input, text='Clear', width=8)
        self.__clear_button.bind('<Button-1>', func=lambda event: self.msg_history_clear() if self.__clear_button[
                                                                                                  'state'] == 'normal' else ())
        self.__clear_button.pack(side=RIGHT)

    def __on_closing(self):
        self.on_closing_cb()
        self.__root.destroy()

    def update_msg_history(self, msg):
        self.msg_history.append(msg)
        self.msg_history_cursor = len(self.msg_history)

    def __prev_msg(self, event):
        total = len(self.msg_history)
        if total == 0:
            # no history
            return
        elif (self.msg_history_cursor == 0) or (self.msg_history_cursor != total) and (
                self.msg_to_send.get() != self.msg_history[self.msg_history_cursor]):
            # need reset or view and modify
            self.msg_history_cursor = total - 1
            self.msg_to_send.set(self.msg_history[self.msg_history_cursor])
        else:
            self.msg_history_cursor -= 1
            self.msg_to_send.set(self.msg_history[self.msg_history_cursor])

    def __next_msg(self, event):
        total = len(self.msg_history)
        if total == 0:
            # no history
            return
        elif (self.msg_history_cursor == total - 1) or (self.msg_history_cursor != total) and (
                self.msg_to_send.get() != self.msg_history[self.msg_history_cursor]):
            # need reset or view and modify
            self.msg_history_cursor = 0
            self.msg_to_send.set(self.msg_history[self.msg_history_cursor])
        else:
            self.msg_history_cursor += 1
            self.msg_to_send.set(self.msg_history[self.msg_history_cursor])

    # public methods
    def show_window(self):
        self.__root.mainloop()

    def set_ui_to_disconnected(self):
        self.__root.title('PyChat Client [Disconnected]')
        self.__msg_entry['state'] = 'disabled'
        self.__send_button['state'] = 'disabled'
        self.__addr_entry['state'] = 'normal'
        self.__port_entry['state'] = 'normal'
        self.__connection_button['state'] = 'normal'
        self.__connection_button['text'] = 'Connect'
        self.__addr_entry.focus()
        self.__addr_entry.icursor(len(self.server_addr.get()))

    def set_ui_to_connecting(self):
        self.__root.title('PyChat Client [Please wait...]')
        self.__msg_entry['state'] = 'disabled'
        self.__send_button['state'] = 'disabled'
        self.__addr_entry['state'] = 'disabled'
        self.__port_entry['state'] = 'disabled'
        self.__connection_button['state'] = 'disabled'

    def set_ui_to_connected(self):
        self.__root.title('PyChat Client [Connected]')
        self.__msg_entry['state'] = 'normal'
        self.__send_button['state'] = 'normal'
        self.__addr_entry['state'] = 'disabled'
        self.__port_entry['state'] = 'disabled'
        self.__connection_button['state'] = 'normal'
        self.__connection_button['text'] = 'Disconnect'
        self.__msg_entry.focus()

    def msg_history_clear(self):
        # clear text
        self.__msg_text['state'] = 'normal'
        self.__msg_text.delete('1.0', END)
        self.__msg_text.see(END)
        self.__msg_text['state'] = 'disabled'
        # clear input entry
        self.msg_to_send.set('')
        # clear msg history
        self.msg_history.clear()
        self.msg_history_cursor = 0

    def append_text_send(self, msg):
        self.__msg_text['state'] = 'normal'
        self.__msg_text.insert(END, '[%s] Send: %s\n' % (
            time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), msg), 'client')
        self.__msg_text.see(END)
        self.__msg_text['state'] = 'disabled'

    def append_text_recv(self, msg):
        self.__msg_text['state'] = 'normal'
        self.__msg_text.insert(END, '[%s] Recv: %s\n' % (
            time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), msg), 'server')
        self.__msg_text.see(END)
        self.__msg_text['state'] = 'disabled'

    def append_text_local(self, msg):
        self.__msg_text['state'] = 'normal'
        self.__msg_text.insert(END, '[%s] Local: %s\n' % (
            time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), msg), 'system')
        self.__msg_text.see(END)
        self.__msg_text['state'] = 'disabled'


class ChatClient(object):
    def __init__(self):
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.__conn.settimeout(5)
        self.is_connected = False
        # create window instance
        self.window = MainWindow()
        # init ui status
        self.window.set_ui_to_disconnected()
        # register callback
        self.window.on_connection_cb = self.connection
        self.window.on_send_cb = self.send
        self.window.on_closing_cb = self.__disconnect

    def run(self):
        # start main message loop
        self.window.show_window()

    def __connect(self):
        try:
            # re-init socket
            self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.window.set_ui_to_connecting()
            self.__conn.connect((self.window.server_addr.get(), int(self.window.server_port.get())))
            self.is_connected = True
            self.__start_recv()
            self.window.set_ui_to_connected()
            self.window.append_text_local('Connected to server')
        except:
            self.window.set_ui_to_disconnected()
            self.window.append_text_local('Connection failed')

    def __disconnect(self):
        try:
            self.__conn.close()
        finally:
            self.is_connected = False
            self.window.set_ui_to_disconnected()
            self.window.append_text_local('Disconnected from server')

    def connection(self, event):
        if self.is_connected:
            self.__disconnect()
        else:
            self.__connect()

    def send(self, event):
        if self.is_connected:
            if self.window.msg_to_send.get() != '':
                try:
                    self.__conn.send(self.window.msg_to_send.get().encode('utf-8'))
                    self.window.append_text_send(self.window.msg_to_send.get())
                    self.window.update_msg_history(self.window.msg_to_send.get())
                    self.window.msg_to_send.set('')
                except:
                    self.window.append_text_local('Failed to send message')
                    self.__disconnect()
            else:
                self.window.append_text_local('Message cannot be empty')

    def __start_recv(self):
        try:
            self.__th_recv = threading.Thread(target=self.__recv, args=())
            self.__th_recv.start()
        except:
            self.window.append_text_local("Failed to start receiving thread")

    def __recv(self):
        while self.is_connected:
            try:
                data = self.__conn.recv(1024)
                if data == b'':
                    self.__disconnect()
                    break
                self.window.append_text_recv(data.decode('utf-8'))
            except Exception as e:
                raise(e)
                break


if __name__ == '__main__':
    app = ChatClient()
    # start application instance
    app.run()
