import hashlib
import os
import socket
import sys
import threading
import time
import tkinter.filedialog
import tkinter.messagebox

import cv2
import face_recognition

import client_main_window
import client_start_window
import socket_tools

my_start_window = None
my_main_window = None
my_socket = None
recv_thread = None
my_username = ''
# nothing means broadcast session
current_session = ''
all_sessions = dict()
filename = ''
filename_short = ''
file_transfer_pending = False
# msg history variables
msg_history = []
msg_history_cursor = 0
# face recognition variables
my_face_encoding = []
face_added = False


def main():
    global my_start_window
    my_start_window = client_start_window.Toplevel()
    # UI init
    # server configurations
    my_start_window.ui_server_ip.set('127.0.0.1')
    my_start_window.ui_server_port.set('1030')
    # event binding
    my_start_window.win_closing_cb = socket_safe_close
    my_start_window.btn_login.configure(command=on_btn_login_click)
    my_start_window.btn_reg.configure(command=on_btn_reg_click)
    my_start_window.btn_chg.configure(command=on_btn_chg_click)
    my_start_window.btn_face_login.configure(command=on_btn_face_login_click)
    my_start_window.btn_face_reg.configure(command=on_btn_face_reg_click)
    my_start_window.ent_login_pwd.bind('<Return>', lambda event: on_btn_login_click())
    my_start_window.ent_reg_confirm.bind('<Return>', lambda event: on_btn_reg_click())
    my_start_window.ent_chg_confirm.bind('<Return>', lambda event: on_btn_chg_click())
    # enter main message loop and block
    my_start_window.show()


def socket_safe_close():
    global my_socket
    try:
        my_socket.shutdown(2)
        my_socket.close()
    except:
        # do not fire when exception occurs
        pass


def on_btn_login_click():
    global my_socket, my_start_window, my_main_window, my_username
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    try:
        if my_start_window.ui_server_ip.get() != '' and my_start_window.ui_server_port.get() != '' and my_start_window.ui_login_usr.get() != '' and my_start_window.ui_login_pwd != '':
            my_socket.connect((my_start_window.ui_server_ip.get(), int(my_start_window.ui_server_port.get())))
            socket_tools.send(my_socket, {'cmd': 'login', 'usr': my_start_window.ui_login_usr.get(),
                                          'pwd': hashlib.sha1(
                                              my_start_window.ui_login_pwd.get().encode('utf-8')).hexdigest()})
            server_response = socket_tools.recv(my_socket)
            if server_response['response'] == 'ok':
                my_username = my_start_window.ui_login_usr.get()
                enter_main_window()
            elif server_response['response'] == 'fail':
                tkinter.messagebox.showerror('PyChat', 'Login failed: ' + server_response['reason'])
                socket_safe_close()
        else:
            tkinter.messagebox.showerror('PyChat', 'Required fields cannot be empty')
    except socket.gaierror:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Address')
    except ValueError:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Port')
    except ConnectionRefusedError:
        tkinter.messagebox.showerror('PyChat', 'Cannot connect to server')
    except Exception as ex:
        tkinter.messagebox.showerror('PyChat', 'Unknown error: ' + str(ex))
    finally:
        my_start_window.ui_login_usr.set('')
        my_start_window.ui_login_pwd.set('')


def on_btn_face_login_click():
    global my_socket, my_start_window, my_username
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    try:
        my_socket.connect((my_start_window.ui_server_ip.get(), int(my_start_window.ui_server_port.get())))
        if my_start_window.ui_server_ip.get() != '' and my_start_window.ui_server_port.get() != '':
            face_enc = get_face_encoding()
            if face_enc:
                socket_tools.send(my_socket, {'cmd': 'face_login', 'face': face_enc})
                server_response = socket_tools.recv(my_socket)
                if server_response['response'] == 'ok':
                    my_username = server_response['username']
                    enter_main_window()
                else:
                    tkinter.messagebox.showerror('PyChat', 'Login failed: '+server_response['reason'])
                    socket_safe_close()
            else:
                tkinter.messagebox.showerror('PyChat', 'No face found')
    except socket.gaierror:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Address')
    except ValueError:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Port')
    except ConnectionRefusedError:
        tkinter.messagebox.showerror('PyChat', 'Cannot connect to server')
    except Exception as ex:
        tkinter.messagebox.showerror('PyChat', 'Unknown error: ' + str(ex))


def on_btn_reg_click():
    global my_socket, my_start_window, my_main_window, my_face_encoding, face_added
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    try:
        if my_start_window.ui_server_ip.get() != '' and my_start_window.ui_server_port.get() != '' and my_start_window.ui_reg_usr.get() != '' and my_start_window.ui_reg_pwd.get() != '' and my_start_window.ui_reg_pwd.get() == my_start_window.ui_reg_confirm.get():
            my_socket.connect((my_start_window.ui_server_ip.get(), int(my_start_window.ui_server_port.get())))
            socket_tools.send(my_socket, {'cmd': 'register', 'usr': my_start_window.ui_reg_usr.get(),
                                          'pwd': hashlib.sha1(
                                              my_start_window.ui_reg_pwd.get().encode('utf-8')).hexdigest(),
                                          'face': my_face_encoding})
            server_response = socket_tools.recv(my_socket)
            if server_response['response'] == 'ok':
                tkinter.messagebox.showinfo('PyChat', 'Register successfully')
            elif server_response['response'] == 'fail':
                tkinter.messagebox.showerror('PyChat', 'Register failed: ' + server_response['reason'])
        elif my_start_window.ui_reg_pwd.get() != my_start_window.ui_reg_confirm.get():
            tkinter.messagebox.showerror('PyChat', 'Two passwords entered are not consistent')
        else:
            tkinter.messagebox.showerror('PyChat', 'Required fields cannot be empty')
    except socket.gaierror:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Address')
    except ValueError:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Port')
    except ConnectionRefusedError:
        tkinter.messagebox.showerror('PyChat', 'Cannot connect to server')
    except Exception as ex:
        tkinter.messagebox.showerror('PyChat', 'Unknown error: ' + str(ex))
    finally:
        my_start_window.ui_reg_usr.set('')
        my_start_window.ui_reg_pwd.set('')
        my_start_window.ui_reg_confirm.set('')
        my_start_window.btn_face_reg.configure(text='''Add Face''')
        my_face_encoding = []
        face_added = False
        socket_safe_close()


def on_btn_face_reg_click():
    global my_face_encoding, face_added, my_start_window
    if not face_added:
        face_enc = get_face_encoding()
        if face_enc:
            my_face_encoding = face_enc
            face_added = True
            my_start_window.btn_face_reg.configure(text='''Del Face''')
    else:
        my_face_encoding = []
        face_added = False
        my_start_window.btn_face_reg.configure(text='''Add Face''')


def on_btn_chg_click():
    global my_socket, my_start_window, my_main_window
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    try:
        my_socket.connect((my_start_window.ui_server_ip.get(), int(my_start_window.ui_server_port.get())))
        if my_start_window.ui_server_ip.get() != '' and my_start_window.ui_server_port.get() != '' and my_start_window.ui_chg_usr.get() != '' and my_start_window.ui_chg_oldpwd.get() != '' and my_start_window.ui_chg_newpwd.get() != '' and my_start_window.ui_chg_newpwd.get() == my_start_window.ui_chg_confirm.get():
            socket_tools.send(my_socket,
                              {'cmd': 'chg_pwd', 'usr': my_start_window.ui_chg_usr.get(), 'old': hashlib.sha1(
                                  my_start_window.ui_chg_oldpwd.get().encode('utf-8')).hexdigest(), 'new': hashlib.sha1(
                                  my_start_window.ui_chg_newpwd.get().encode('utf-8')).hexdigest()})
            server_response = socket_tools.recv(my_socket)
            if server_response['response'] == 'ok':
                tkinter.messagebox.showinfo('PyChat', 'Changed password successfully')
            elif server_response['response'] == 'fail':
                tkinter.messagebox.showerror('PyChat', 'Change password failed: ' + server_response['reason'])
        elif my_start_window.ui_chg_newpwd.get() != my_start_window.ui_chg_confirm.get():
            tkinter.messagebox.showerror('PyChat', 'Two passwords entered are not consistent')
        else:
            tkinter.messagebox.showerror('PyChat', 'Required fields cannot be empty')
    except socket.gaierror:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Address')
    except ValueError:
        tkinter.messagebox.showerror('PyChat', 'Invalid Server Port')
    except ConnectionRefusedError:
        tkinter.messagebox.showerror('PyChat', 'Cannot connect to server')
    except Exception as ex:
        tkinter.messagebox.showerror('PyChat', 'Unknown error: ' + str(ex))
    finally:
        my_start_window.ui_chg_usr.set('')
        my_start_window.ui_chg_oldpwd.set('')
        my_start_window.ui_chg_newpwd.set('')
        my_start_window.ui_chg_confirm.set('')
        socket_safe_close()


def enter_main_window():
    global my_socket, my_start_window, my_main_window, my_username
    my_start_window.destroy()
    my_start_window = None
    my_main_window = client_main_window.Toplevel()
    my_main_window.win_closing_cb = on_main_window_closing
    my_main_window.top.title('%s - PyChat' % my_username)
    my_main_window.ui_nameshow.set('%s -> Global' % my_username)
    my_main_window.btn_file.configure(command=on_btn_file_click)
    my_main_window.btn_send.configure(command=on_btn_send_click)
    my_main_window.listSession.bind('<<ListboxSelect>>', on_session_select)
    my_main_window.entPresend.bind('<Return>', lambda event: on_btn_send_click())
    my_main_window.entPresend.bind('<Up>', lambda event: prev_msg())
    my_main_window.entPresend.bind('<Down>', lambda event: next_msg())
    request_user_list()
    request_session_history('')
    start_recv_thread()
    my_main_window.show()


def start_recv_thread():
    global recv_thread
    try:
        recv_thread = threading.Thread(target=recv_async, args=())
        recv_thread.setDaemon(True)
        recv_thread.start()
    except Exception as e:
        tkinter.messagebox.showerror('PyChat', 'Fatal Error: ' + str(e))
        sys.exit(1)


def recv_async():
    global my_socket, all_sessions, my_main_window, current_session, file_transfer_pending, filename_short, filename
    while True:
        try:
            data = socket_tools.recv(my_socket)
            if data['type'] == 'list_users':
                # update dictionary in memory
                all_sessions = dict()
                for session in [''] + data['data']:
                    all_sessions[session] = False
                # update UI
                refresh_session_list()
            elif data['type'] == 'get_history':
                if data['peer'] == current_session:
                    # clear textbox
                    my_main_window.scrolledHistory['state'] = 'normal'
                    my_main_window.scrolledHistory.delete('1.0', 'end')
                    my_main_window.scrolledHistory['state'] = 'disabled'
                    # append entries
                    for entry in data['data']:
                        append_txtHistory(entry[0], entry[1], entry[2])
            elif data['type'] == 'peer_joined':
                # add to the dictionary
                all_sessions[data['peer']] = False
                # update UI
                refresh_session_list()
            elif data['type'] == 'peer_left':
                # remove from dictionary
                if data['peer'] in all_sessions.keys():
                    del all_sessions[data['peer']]
                if data['peer'] == current_session:
                    # swithch current display to global
                    current_session = ''
                    my_main_window.btn_file.configure(state='disabled')
                    my_main_window.ui_nameshow.set('%s -> Global' % my_username)
                    all_sessions[''] = False
                    refresh_session_list()
                    request_session_history('')
                # update UI
                refresh_session_list()
            elif data['type'] == 'message':
                if data['peer'] == current_session:
                    append_txtHistory(data['peer'], time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                                      data['msg'])
                else:
                    all_sessions[data['peer']] = True
                    refresh_session_list()
            elif data['type'] == 'broadcast':
                if current_session == '':
                    append_txtHistory(data['peer'], time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                                      data['msg'])
                else:
                    all_sessions[''] = True
                    refresh_session_list()
            elif data['type'] == 'file_request':
                if tkinter.messagebox.askyesno('PyChat',
                                               '%s wants to send you a file\nFilename: %s\nSize: %s\nAccept it?' % (
                                                       data['peer'], data['filename'], data['size'])):
                    socket_tools.send(my_socket, {'cmd': 'file_accept', 'peer': data['peer']})
                    try:
                        # recv file
                        total_bytes = 0
                        addr = ('0.0.0.0', 1031)
                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server.bind(addr)
                        server.listen(5)
                        client_socket, addr = server.accept()
                        starttime = time.time()
                        with open(data['filename'], "wb") as f:
                            while True:
                                fdata = client_socket.recv(1024)
                                total_bytes += len(fdata)
                                if not fdata:
                                    break
                                f.write(fdata)
                        f.close()
                        client_socket.close()
                        server.close()
                        # record end time
                        endtime = time.time()
                        # check md5 checksum
                        received_md5 = get_file_md5(data['filename'])
                        if received_md5 == data['md5']:
                            tkinter.messagebox.showinfo('PyChat', 'Received file successfully\nMD5 Checksum Passed')
                        else:
                            tkinter.messagebox.showwarning('PyChat', 'File received was broken\nMD5 Checksum Error')
                        my_main_window.scrolledHistory['state'] = 'normal'
                        my_main_window.scrolledHistory.insert('end', 'Received %s bytes from %s in %s seconds\n\n' % (
                            total_bytes, data['peer'], format(endtime - starttime, '.2f')), 'hint')
                        my_main_window.scrolledHistory.see('end')
                        my_main_window.scrolledHistory['state'] = 'disabled'
                    except:
                        pass
                else:
                    socket_tools.send(my_socket, {'cmd': 'file_deny', 'peer': data['peer']})
            elif data['type'] == 'file_deny':
                my_main_window.btn_file.configure(text='''Send File...''')
                if current_session == '':
                    my_main_window.btn_file.configure(state='disabled')
                else:
                    my_main_window.btn_file.configure(state='normal')
                tkinter.messagebox.showinfo('PyChat', 'Your peer refused to receive the file')
            elif data['type'] == 'file_accept':
                # peer accepted, send data
                try:
                    total_bytes = 0
                    starttime = time.time()
                    addr = (data['ip'], 1031)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(addr)
                    with open(filename, 'rb') as f:
                        while True:
                            fdata = f.read(1024)
                            if not fdata:
                                break
                            total_bytes += len(fdata)
                            client.send(fdata)
                    f.close()
                    client.close()
                    endtime = time.time()
                    my_main_window.scrolledHistory['state'] = 'normal'
                    my_main_window.scrolledHistory.insert('end', 'Sent %s bytes in %s seconds\n\n' % (
                        total_bytes, format(endtime - starttime, '.2f')), 'hint')
                    my_main_window.scrolledHistory.see('end')
                    my_main_window.scrolledHistory['state'] = 'disabled'
                except Exception as e:
                    tkinter.messagebox.showerror('PyChat',
                                                 'Exception occured while attempting to send file to peer: ' + str(e))
                finally:
                    # reset relevant variables for security concerns
                    filename = ''
                    filename_short = ''
                    file_transfer_pending = False
                my_main_window.btn_file.configure(text='''Send File...''')
                if current_session == '':
                    my_main_window.btn_file.configure(state='disabled')
                else:
                    my_main_window.btn_file.configure(state='normal')
                tkinter.messagebox.showinfo('PyChat', 'File sent successfully')
        except ConnectionResetError:
            tkinter.messagebox.showerror('PyChat', 'Server closed')
            os._exit(1)
            break
        except Exception as e:
            tkinter.messagebox.showerror('PyChat', 'Fatal error when receiving async: ' + str(e))
            os._exit(1)
            break


def refresh_session_list():
    global my_main_window, all_sessions
    my_main_window.listSession.delete(0, 'end')
    for i in all_sessions.keys():
        name = ''
        if i == '':
            name = 'Global'
        else:
            name = i
        if all_sessions[i]:
            name += ' (NEW)'
        my_main_window.listSession.insert('end', name)


def request_user_list():
    global my_socket
    socket_tools.send(my_socket, {'cmd': 'list_users'})


def request_session_history(session_name):
    global my_socket
    socket_tools.send(my_socket, {'cmd': 'get_history', 'peer': session_name})


def append_txtHistory(sender, time, msg):
    global my_username
    my_main_window.scrolledHistory['state'] = 'normal'
    if sender == my_username:
        my_main_window.scrolledHistory.insert('end', '%s - %s\n' % (sender, time), 'send')
        my_main_window.scrolledHistory.insert('end', msg + '\n\n', 'text')
    else:
        my_main_window.scrolledHistory.insert('end', '%s - %s\n' % (sender, time), 'recv')
        my_main_window.scrolledHistory.insert('end', msg + '\n\n', 'text')
    my_main_window.scrolledHistory.see('end')
    my_main_window.scrolledHistory['state'] = 'disabled'


def on_btn_file_click():
    global my_socket, my_main_window, filename, filename_short, file_transfer_pending
    try:
        # here the name is full path
        filename = tkinter.filedialog.askopenfilename()
        # in case user closes the window
        if filename == '': return
        # get the short name
        filename_short = ''
        if len(filename.split('/')) < len(filename.split('\\')):
            filename_short = filename.split('\\')[-1]
        else:
            filename_short = filename.split('/')[-1]
        size = os.path.getsize(filename)
        # get a friendly size
        count = 0
        while not 1 < size < 1024 and count < 6:
            size /= 1024
            count += 1
        size = str(format(size, '.2f')) + ['B', 'KB', 'MB', 'GB', 'TB', 'PB'][count]
        md5_checksum = get_file_md5(filename)
        socket_tools.send(my_socket,
                          {'cmd': 'file_request', 'peer': current_session, 'filename': filename_short, 'size': size,
                           'md5': md5_checksum})
        # no parallel file transfer allowed, disable the button
        my_main_window.btn_file.configure(text='''Waiting''')
        my_main_window.btn_file.configure(state='disabled')
        file_transfer_pending = True
    except Exception as e:
        tkinter.messagebox.showerror('PyChat', 'Fatal Error: ' + str(e))
        sys.exit(1)


def on_btn_send_click():
    global my_socket, my_username, current_session, my_main_window, msg_history, msg_history_cursor
    try:
        if my_main_window.ui_msg.get() != '':
            socket_tools.send(my_socket, {'cmd': 'chat', 'peer': current_session, 'msg': my_main_window.ui_msg.get()})
            append_txtHistory(my_username, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())),
                              my_main_window.ui_msg.get())
            # update msg history
            msg_history.append(my_main_window.ui_msg.get())
            msg_history_cursor += 1
            my_main_window.ui_msg.set('')
        else:
            tkinter.messagebox.showinfo('PyChat', 'You cannot send empty message')
    except Exception as e:
        tkinter.messagebox.showerror('PyChat', 'Fatal Error: ' + str(e))
        sys.exit(1)


def on_session_select(evt):
    global current_session, my_main_window, my_username, all_sessions, file_transfer_pending
    w = evt.widget
    changed = False
    if len(w.curselection()) != 0:
        index = int(w.curselection()[0])
        if index != 0:
            # normal session
            if current_session != w.get(index).rstrip(' (NEW)'):
                changed = True
                current_session = w.get(index).rstrip(' (NEW)')
                # activate file transfer
                if not file_transfer_pending:
                    my_main_window.btn_file.configure(state='normal')
                # change top label
                my_main_window.ui_nameshow.set('%s -> %s' % (my_username, current_session))
                # reset the unread tag
                all_sessions[current_session] = False
                refresh_session_list()
        elif index == 0:
            # broadcast session
            if current_session != '':
                changed = True
                current_session = ''
                # disable file transfer
                my_main_window.btn_file.configure(state='disabled')
                # change top label
                my_main_window.ui_nameshow.set('%s -> Global' % my_username)
                # reset the unread tag
                all_sessions[''] = False
                refresh_session_list()
        if changed:
            request_session_history(current_session)


def on_main_window_closing():
    socket_safe_close()


def prev_msg():
    global msg_history, msg_history_cursor, my_main_window
    total = len(msg_history)
    if total == 0:
        # no history
        return
    elif msg_history_cursor == 0 or msg_history_cursor != total and my_main_window.ui_msg.get() != msg_history[
        msg_history_cursor]:
        # need reset or call but modified the history
        msg_history_cursor = total - 1
        my_main_window.ui_msg.set(msg_history[msg_history_cursor])
    else:
        msg_history_cursor -= 1
        my_main_window.ui_msg.set(msg_history[msg_history_cursor])


def next_msg():
    global msg_history, msg_history_cursor, my_main_window
    total = len(msg_history)
    if total == 0:
        # no history
        return
    elif msg_history_cursor == total - 1 or msg_history_cursor != total and my_main_window.ui_msg.get() != msg_history[
        msg_history_cursor]:
        # need reset or call but modified the history
        msg_history_cursor = 0
        my_main_window.ui_msg.set(msg_history[msg_history_cursor])
    else:
        msg_history_cursor += 1
        my_main_window.ui_msg.set(msg_history[msg_history_cursor])


def get_file_md5(filepath):
    md5obj = hashlib.md5()
    maxbuf = 8192
    f = open(filepath, 'rb')
    while True:
        buf = f.read(maxbuf)
        if not buf:
            break
        md5obj.update(buf)
    f.close()
    hash = md5obj.hexdigest()
    return str(hash).upper()


def get_face_encoding():
    # open video device for capture
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    process_this_frame = True
    last_top = 0
    last_bottom = 0
    last_left = 0
    last_right = 0

    frame_delay = 0

    result = None

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (43, 43, 206), 2)

        # Check data stability
        if len(face_locations) == 1:
            frame_delay+=1
            top, right, bottom, left = face_locations[0]
            delta = abs(last_top - top) + abs(last_bottom - bottom) + abs(last_left - left) + abs(last_right - right)
            last_top, last_bottom, last_left, last_right = top, bottom, left, right
            if delta < 20 and frame_delay>15:
                result = face_recognition.face_encodings(rgb_small_frame, face_locations)[0].tolist()
                break
        else:
            frame_delay = 0
        # Display the resulting image
        cv2.imshow('''Detect Face (Press 'q' to quit)''', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return result


if __name__ == '__main__':
    main()
