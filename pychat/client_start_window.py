import sys
import tkinter as tk
import tkinter.ttk as ttk


class Toplevel:
    def show(self):
        self.top.mainloop()

    def destroy(self):
        self.top.destroy()

    def __init__(self):
        self.top = tk.Tk()
        # variables for entry widgets
        self.ui_login_usr = tk.StringVar()
        self.ui_login_pwd = tk.StringVar()
        self.ui_reg_usr = tk.StringVar()
        self.ui_reg_pwd = tk.StringVar()
        self.ui_reg_confirm = tk.StringVar()
        self.ui_chg_usr = tk.StringVar()
        self.ui_chg_oldpwd = tk.StringVar()
        self.ui_chg_newpwd = tk.StringVar()
        self.ui_chg_confirm = tk.StringVar()
        self.ui_server_ip = tk.StringVar()
        self.ui_server_port = tk.StringVar()
        '''This class configures and populates the toplevel window.
           top is the self.toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {System} -size 11 -weight normal -slant roman " \
                "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        self.top.geometry("368x359+500+150")
        self.top.title("Start - PyChat")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")
        self.top.resizable(width=False, height=False)

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
        [('selected', _compcolor), ('active', _ana2color)])
        self.TNotebook1 = ttk.Notebook(self.top)
        self.TNotebook1.place(relx=0.027, rely=0.265, relheight=0.713
                              , relwidth=0.962)
        self.TNotebook1.configure(width=354)
        self.TNotebook1.configure(takefocus="")
        self.TNotebook1_t0 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t0, padding=3)
        self.TNotebook1.tab(0, text="Login", compound="left", underline="-1", )
        self.TNotebook1_t0.configure(background="#d9d9d9")
        self.TNotebook1_t0.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t0.configure(highlightcolor="black")
        self.TNotebook1_t1 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(1, text="Register", compound="left", underline="-1", )
        self.TNotebook1_t1.configure(background="#d9d9d9")
        self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t1.configure(highlightcolor="black")
        self.TNotebook1_t2 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t2, padding=3)
        self.TNotebook1.tab(2, text="Change Password", compound="none"
                            , underline="-1", )
        self.TNotebook1_t2.configure(background="#d9d9d9")
        self.TNotebook1_t2.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t2.configure(highlightcolor="black")

        self.Label3 = tk.Label(self.TNotebook1_t0)
        self.Label3.place(relx=0.086, rely=0.091, height=31, width=89)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(justify='right')
        self.Label3.configure(text='''Username:''')

        self.Label4 = tk.Label(self.TNotebook1_t0)
        self.Label4.place(relx=0.086, rely=0.273, height=31, width=86)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(justify='right')
        self.Label4.configure(text='''Password:''')

        self.ent_login_usr = tk.Entry(self.TNotebook1_t0)
        self.ent_login_usr.place(relx=0.371, rely=0.091, height=26
                                 , relwidth=0.554)
        self.ent_login_usr.configure(background="white")
        self.ent_login_usr.configure(disabledforeground="#a3a3a3")
        self.ent_login_usr.configure(font=font9)
        self.ent_login_usr.configure(foreground="#000000")
        self.ent_login_usr.configure(highlightbackground="#d9d9d9")
        self.ent_login_usr.configure(highlightcolor="black")
        self.ent_login_usr.configure(insertbackground="black")
        self.ent_login_usr.configure(selectbackground="#c4c4c4")
        self.ent_login_usr.configure(selectforeground="black")
        self.ent_login_usr.configure(textvariable=self.ui_login_usr)

        self.ent_login_pwd = tk.Entry(self.TNotebook1_t0)
        self.ent_login_pwd.place(relx=0.371, rely=0.273, height=26
                                 , relwidth=0.554)
        self.ent_login_pwd.configure(background="white")
        self.ent_login_pwd.configure(disabledforeground="#a3a3a3")
        self.ent_login_pwd.configure(font=font9)
        self.ent_login_pwd.configure(foreground="#000000")
        self.ent_login_pwd.configure(highlightbackground="#d9d9d9")
        self.ent_login_pwd.configure(highlightcolor="black")
        self.ent_login_pwd.configure(insertbackground="black")
        self.ent_login_pwd.configure(selectbackground="#c4c4c4")
        self.ent_login_pwd.configure(selectforeground="black")
        self.ent_login_pwd.configure(show="*")
        self.ent_login_pwd.configure(textvariable=self.ui_login_pwd)

        self.btn_login = tk.Button(self.TNotebook1_t0)
        self.btn_login.place(relx=0.714, rely=0.555, height=32, width=88)
        self.btn_login.configure(activebackground="#ececec")
        self.btn_login.configure(activeforeground="#000000")
        self.btn_login.configure(background="#d9d9d9")
        self.btn_login.configure(disabledforeground="#a3a3a3")
        self.btn_login.configure(foreground="#000000")
        self.btn_login.configure(highlightbackground="#d9d9d9")
        self.btn_login.configure(highlightcolor="black")
        self.btn_login.configure(pady="0")
        self.btn_login.configure(text='''Login''')

        self.btn_face_login = tk.Button(self.TNotebook1_t0)
        self.btn_face_login.place(relx=0.029, rely=0.545, height=32, width=78)
        self.btn_face_login.configure(activebackground="#ececec")
        self.btn_face_login.configure(activeforeground="#000000")
        self.btn_face_login.configure(background="#d9d9d9")
        self.btn_face_login.configure(disabledforeground="#a3a3a3")
        self.btn_face_login.configure(foreground="#000000")
        self.btn_face_login.configure(highlightbackground="#d9d9d9")
        self.btn_face_login.configure(highlightcolor="black")
        self.btn_face_login.configure(pady="0")
        self.btn_face_login.configure(text='''Face Login''')
        self.btn_face_login.configure(width=99)

        self.Label5 = tk.Label(self.TNotebook1_t1)
        self.Label5.place(relx=0.086, rely=0.091, height=31, width=89)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(justify='right')
        self.Label5.configure(text='''Username:''')

        self.Label6 = tk.Label(self.TNotebook1_t1)
        self.Label6.place(relx=0.086, rely=0.273, height=31, width=86)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(justify='right')
        self.Label6.configure(text='''Password:''')

        self.Label7 = tk.Label(self.TNotebook1_t1)
        self.Label7.place(relx=0.114, rely=0.455, height=31, width=74)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(justify='right')
        self.Label7.configure(text='''Confirm:''')

        self.ent_reg_usr = tk.Entry(self.TNotebook1_t1)
        self.ent_reg_usr.place(relx=0.371, rely=0.091, height=24, relwidth=0.554)

        self.ent_reg_usr.configure(background="white")
        self.ent_reg_usr.configure(disabledforeground="#a3a3a3")
        self.ent_reg_usr.configure(font=font9)
        self.ent_reg_usr.configure(foreground="#000000")
        self.ent_reg_usr.configure(highlightbackground="#d9d9d9")
        self.ent_reg_usr.configure(highlightcolor="black")
        self.ent_reg_usr.configure(insertbackground="black")
        self.ent_reg_usr.configure(selectbackground="#c4c4c4")
        self.ent_reg_usr.configure(selectforeground="black")
        self.ent_reg_usr.configure(textvariable=self.ui_reg_usr)

        self.ent_reg_pwd = tk.Entry(self.TNotebook1_t1)
        self.ent_reg_pwd.place(relx=0.371, rely=0.273, height=24, relwidth=0.554)

        self.ent_reg_pwd.configure(background="white")
        self.ent_reg_pwd.configure(disabledforeground="#a3a3a3")
        self.ent_reg_pwd.configure(font=font9)
        self.ent_reg_pwd.configure(foreground="#000000")
        self.ent_reg_pwd.configure(highlightbackground="#d9d9d9")
        self.ent_reg_pwd.configure(highlightcolor="black")
        self.ent_reg_pwd.configure(insertbackground="black")
        self.ent_reg_pwd.configure(selectbackground="#c4c4c4")
        self.ent_reg_pwd.configure(selectforeground="black")
        self.ent_reg_pwd.configure(show="*")
        self.ent_reg_pwd.configure(textvariable=self.ui_reg_pwd)

        self.ent_reg_confirm = tk.Entry(self.TNotebook1_t1)
        self.ent_reg_confirm.place(relx=0.371, rely=0.455, height=24
                                   , relwidth=0.554)
        self.ent_reg_confirm.configure(background="white")
        self.ent_reg_confirm.configure(disabledforeground="#a3a3a3")
        self.ent_reg_confirm.configure(font=font9)
        self.ent_reg_confirm.configure(foreground="#000000")
        self.ent_reg_confirm.configure(highlightbackground="#d9d9d9")
        self.ent_reg_confirm.configure(highlightcolor="black")
        self.ent_reg_confirm.configure(insertbackground="black")
        self.ent_reg_confirm.configure(selectbackground="#c4c4c4")
        self.ent_reg_confirm.configure(selectforeground="black")
        self.ent_reg_confirm.configure(show="*")
        self.ent_reg_confirm.configure(textvariable=self.ui_reg_confirm)

        self.btn_reg = tk.Button(self.TNotebook1_t1)
        self.btn_reg.place(relx=0.714, rely=0.636, height=32, width=88)
        self.btn_reg.configure(activebackground="#ececec")
        self.btn_reg.configure(activeforeground="#000000")
        self.btn_reg.configure(background="#d9d9d9")
        self.btn_reg.configure(disabledforeground="#a3a3a3")
        self.btn_reg.configure(foreground="#000000")
        self.btn_reg.configure(highlightbackground="#d9d9d9")
        self.btn_reg.configure(highlightcolor="black")
        self.btn_reg.configure(pady="0")
        self.btn_reg.configure(text='''Register''')

        self.btn_face_reg = tk.Button(self.TNotebook1_t1)
        self.btn_face_reg.place(relx=0.029, rely=0.636, height=32, width=78)
        self.btn_face_reg.configure(activebackground="#ececec")
        self.btn_face_reg.configure(activeforeground="#000000")
        self.btn_face_reg.configure(background="#d9d9d9")
        self.btn_face_reg.configure(disabledforeground="#a3a3a3")
        self.btn_face_reg.configure(foreground="#000000")
        self.btn_face_reg.configure(highlightbackground="#d9d9d9")
        self.btn_face_reg.configure(highlightcolor="black")
        self.btn_face_reg.configure(pady="0")
        self.btn_face_reg.configure(text='''Add Face''')
        self.btn_face_reg.configure(width=78)

        self.Label8 = tk.Label(self.TNotebook1_t2)
        self.Label8.place(relx=0.086, rely=0.091, height=31, width=89)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(activeforeground="black")
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(disabledforeground="#a3a3a3")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#d9d9d9")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(justify='right')
        self.Label8.configure(text='''Username:''')

        self.Label9 = tk.Label(self.TNotebook1_t2)
        self.Label9.place(relx=0.1, rely=0.273, height=31, width=79)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(disabledforeground="#a3a3a3")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(justify='right')
        self.Label9.configure(text='''Old pwd:''')

        self.Label10 = tk.Label(self.TNotebook1_t2)
        self.Label10.place(relx=0.086, rely=0.455, height=31, width=85)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(justify='right')
        self.Label10.configure(text='''New pwd:''')

        self.Label11 = tk.Label(self.TNotebook1_t2)
        self.Label11.place(relx=0.114, rely=0.636, height=31, width=74)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(activeforeground="black")
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#d9d9d9")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(justify='right')
        self.Label11.configure(text='''Confirm:''')

        self.ent_chg_usr = tk.Entry(self.TNotebook1_t2)
        self.ent_chg_usr.place(relx=0.371, rely=0.091, height=24, relwidth=0.554)

        self.ent_chg_usr.configure(background="white")
        self.ent_chg_usr.configure(disabledforeground="#a3a3a3")
        self.ent_chg_usr.configure(font=font9)
        self.ent_chg_usr.configure(foreground="#000000")
        self.ent_chg_usr.configure(highlightbackground="#d9d9d9")
        self.ent_chg_usr.configure(highlightcolor="black")
        self.ent_chg_usr.configure(insertbackground="black")
        self.ent_chg_usr.configure(selectbackground="#c4c4c4")
        self.ent_chg_usr.configure(selectforeground="black")
        self.ent_chg_usr.configure(textvariable=self.ui_chg_usr)

        self.ent_chg_oldpwd = tk.Entry(self.TNotebook1_t2)
        self.ent_chg_oldpwd.place(relx=0.371, rely=0.273, height=24
                                  , relwidth=0.554)
        self.ent_chg_oldpwd.configure(background="white")
        self.ent_chg_oldpwd.configure(disabledforeground="#a3a3a3")
        self.ent_chg_oldpwd.configure(font=font9)
        self.ent_chg_oldpwd.configure(foreground="#000000")
        self.ent_chg_oldpwd.configure(highlightbackground="#d9d9d9")
        self.ent_chg_oldpwd.configure(highlightcolor="black")
        self.ent_chg_oldpwd.configure(insertbackground="black")
        self.ent_chg_oldpwd.configure(selectbackground="#c4c4c4")
        self.ent_chg_oldpwd.configure(selectforeground="black")
        self.ent_chg_oldpwd.configure(show="*")
        self.ent_chg_oldpwd.configure(textvariable=self.ui_chg_oldpwd)

        self.ent_chg_newpwd = tk.Entry(self.TNotebook1_t2)
        self.ent_chg_newpwd.place(relx=0.371, rely=0.455, height=24
                                  , relwidth=0.554)
        self.ent_chg_newpwd.configure(background="white")
        self.ent_chg_newpwd.configure(disabledforeground="#a3a3a3")
        self.ent_chg_newpwd.configure(font=font9)
        self.ent_chg_newpwd.configure(foreground="#000000")
        self.ent_chg_newpwd.configure(highlightbackground="#d9d9d9")
        self.ent_chg_newpwd.configure(highlightcolor="black")
        self.ent_chg_newpwd.configure(insertbackground="black")
        self.ent_chg_newpwd.configure(selectbackground="#c4c4c4")
        self.ent_chg_newpwd.configure(selectforeground="black")
        self.ent_chg_newpwd.configure(show="*")
        self.ent_chg_newpwd.configure(textvariable=self.ui_chg_newpwd)

        self.ent_chg_confirm = tk.Entry(self.TNotebook1_t2)
        self.ent_chg_confirm.place(relx=0.371, rely=0.636, height=24
                                   , relwidth=0.554)
        self.ent_chg_confirm.configure(background="white")
        self.ent_chg_confirm.configure(disabledforeground="#a3a3a3")
        self.ent_chg_confirm.configure(font=font9)
        self.ent_chg_confirm.configure(foreground="#000000")
        self.ent_chg_confirm.configure(highlightbackground="#d9d9d9")
        self.ent_chg_confirm.configure(highlightcolor="black")
        self.ent_chg_confirm.configure(insertbackground="black")
        self.ent_chg_confirm.configure(selectbackground="#c4c4c4")
        self.ent_chg_confirm.configure(selectforeground="black")
        self.ent_chg_confirm.configure(show="*")
        self.ent_chg_confirm.configure(textvariable=self.ui_chg_confirm)

        self.btn_chg = tk.Button(self.TNotebook1_t2)
        self.btn_chg.place(relx=0.714, rely=0.818, height=32, width=88)
        self.btn_chg.configure(activebackground="#ececec")
        self.btn_chg.configure(activeforeground="#000000")
        self.btn_chg.configure(background="#d9d9d9")
        self.btn_chg.configure(disabledforeground="#a3a3a3")
        self.btn_chg.configure(foreground="#000000")
        self.btn_chg.configure(highlightbackground="#d9d9d9")
        self.btn_chg.configure(highlightcolor="black")
        self.btn_chg.configure(pady="0")
        self.btn_chg.configure(text='''Apply''')
        self.btn_chg.configure(width=98)

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.082, rely=0.042, height=31, width=79)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Server IP:''')

        self.Label2 = tk.Label(self.top)
        self.Label2.place(relx=0.177, rely=0.153, height=31, width=43)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Port:''')

        self.ent_server_ip = tk.Entry(self.top)
        self.ent_server_ip.place(relx=0.326, rely=0.056, height=24
                                 , relwidth=0.554)
        self.ent_server_ip.configure(background="white")
        self.ent_server_ip.configure(disabledforeground="#a3a3a3")
        self.ent_server_ip.configure(font=font9)
        self.ent_server_ip.configure(foreground="#000000")
        self.ent_server_ip.configure(highlightbackground="#d9d9d9")
        self.ent_server_ip.configure(highlightcolor="black")
        self.ent_server_ip.configure(insertbackground="black")
        self.ent_server_ip.configure(selectbackground="#c4c4c4")
        self.ent_server_ip.configure(selectforeground="black")
        self.ent_server_ip.configure(textvariable=self.ui_server_ip)

        self.ent_server_port = tk.Entry(self.top)
        self.ent_server_port.place(relx=0.326, rely=0.167, height=24
                                   , relwidth=0.554)
        self.ent_server_port.configure(background="white")
        self.ent_server_port.configure(disabledforeground="#a3a3a3")
        self.ent_server_port.configure(font=font9)
        self.ent_server_port.configure(foreground="#000000")
        self.ent_server_port.configure(highlightbackground="#d9d9d9")
        self.ent_server_port.configure(highlightcolor="black")
        self.ent_server_port.configure(insertbackground="black")
        self.ent_server_port.configure(selectbackground="#c4c4c4")
        self.ent_server_port.configure(selectforeground="black")
        self.ent_server_port.configure(textvariable=self.ui_server_port)


if __name__ == '__main__':
    start_window = Toplevel()
    start_window.win_closing_cb = lambda: print("Closing...")
    start_window.show()
