import sys
import tkinter as tk
import tkinter.ttk as ttk


class Toplevel:
    # window closing callback
    win_closing_cb = None

    def show(self):
        self.top.mainloop()

    def destroy(self):
        try:
            self.win_closing_cb()
        except:
            pass
        self.top.destroy()

    def __init__(self):
        self.top = tk.Tk()
        # windows event callbacks
        self.top.protocol('WM_DELETE_WINDOW', self.destroy)
        # tk string variables
        self.ui_msg = tk.StringVar()
        self.ui_nameshow = tk.StringVar()
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Segoe UI} -size 12 -weight bold -slant roman" \
                " -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        self.top.geometry("510x530+400+50")
        self.top.title("Chat - PyChat")
        self.top.configure(background="#d9d9d9")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")
        self.top.resizable(width=False,height=False)

        self.listSession = tk.Listbox(self.top)
        self.listSession.place(relx=0.02, rely=0.151, relheight=0.751
                               , relwidth=0.224)
        self.listSession.configure(background="white")
        self.listSession.configure(disabledforeground="#a3a3a3")
        self.listSession.configure(font="TkFixedFont")
        self.listSession.configure(foreground="#000000")
        self.listSession.configure(highlightbackground="#d9d9d9")
        self.listSession.configure(highlightcolor="black")
        self.listSession.configure(selectbackground="#c4c4c4")
        self.listSession.configure(selectforeground="black")
        self.listSession.configure(width=114)
        self.listSession.configure(font="-family {Courier New} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")

        self.scrolledHistory = ScrolledText(self.top)
        self.scrolledHistory.place(relx=0.275, rely=0.019, relheight=0.885
                                   , relwidth=0.706)
        self.scrolledHistory.configure(background="white")
        self.scrolledHistory.configure(font="TkTextFont")
        self.scrolledHistory.configure(foreground="black")
        self.scrolledHistory.configure(highlightbackground="#d9d9d9")
        self.scrolledHistory.configure(highlightcolor="black")
        self.scrolledHistory.configure(insertbackground="black")
        self.scrolledHistory.configure(insertborderwidth="3")
        self.scrolledHistory.configure(selectbackground="#c4c4c4")
        self.scrolledHistory.configure(selectforeground="black")
        self.scrolledHistory.configure(width=10)
        self.scrolledHistory.configure(wrap='none')
        self.scrolledHistory.configure(state='disabled')
        self.scrolledHistory.tag_configure('recv', foreground='#007709', font=('Century', 10))
        self.scrolledHistory.tag_configure('send', foreground='#771300', font=('Century', 10))
        self.scrolledHistory.tag_configure('text', foreground='#444444', font=('Century', 12, 'bold'))
        self.scrolledHistory.tag_configure('hint', foreground='#a0a0a0', font=('Century', 10))

        self.entPresend = tk.Entry(self.top)
        self.entPresend.place(relx=0.275, rely=0.925, height=24, relwidth=0.596)
        self.entPresend.configure(background="white")
        self.entPresend.configure(disabledforeground="#a3a3a3")
        self.entPresend.configure(font="TkFixedFont")
        self.entPresend.configure(foreground="#000000")
        self.entPresend.configure(highlightbackground="#d9d9d9")
        self.entPresend.configure(highlightcolor="black")
        self.entPresend.configure(insertbackground="black")
        self.entPresend.configure(selectbackground="#c4c4c4")
        self.entPresend.configure(selectforeground="black")
        self.entPresend.configure(textvariable=self.ui_msg)

        self.btn_send = tk.Button(self.top)
        self.btn_send.place(relx=0.892, rely=0.920, height=32, width=45)
        self.btn_send.configure(activebackground="#ececec")
        self.btn_send.configure(activeforeground="#000000")
        self.btn_send.configure(background="#d9d9d9")
        self.btn_send.configure(disabledforeground="#a3a3a3")
        self.btn_send.configure(foreground="#000000")
        self.btn_send.configure(highlightbackground="#d9d9d9")
        self.btn_send.configure(highlightcolor="black")
        self.btn_send.configure(pady="0")
        self.btn_send.configure(text='''Send''')

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.0, rely=0.104, height=21, width=101)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(justify='left')
        self.Label1.configure(text='''Session List:''')

        self.btn_file = tk.Button(self.top)
        self.btn_file.place(relx=0.029, rely=0.920, height=32, width=108)
        self.btn_file.configure(activebackground="#ececec")
        self.btn_file.configure(activeforeground="#000000")
        self.btn_file.configure(background="#d9d9d9")
        self.btn_file.configure(disabledforeground="#a3a3a3")
        self.btn_file.configure(foreground="#000000")
        self.btn_file.configure(highlightbackground="#d9d9d9")
        self.btn_file.configure(highlightcolor="black")
        self.btn_file.configure(pady="0")
        self.btn_file.configure(text='''Send File...''')
        self.btn_file.configure(state='disabled')

        self.labelGreet = tk.Label(self.top)
        self.labelGreet.place(relx=0.0, rely=0.0, height=57, width=140)
        self.labelGreet.configure(activebackground="#f9f9f9")
        self.labelGreet.configure(activeforeground="black")
        self.labelGreet.configure(background="#d9d9d9")
        self.labelGreet.configure(disabledforeground="#a3a3a3")
        self.labelGreet.configure(font=font9)
        self.labelGreet.configure(foreground="#000000")
        self.labelGreet.configure(highlightbackground="#d9d9d9")
        self.labelGreet.configure(highlightcolor="black")
        self.labelGreet.configure(justify='left')
        self.labelGreet.configure(text='''''')
        self.labelGreet.configure(textvariable=self.ui_nameshow)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
            | tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''

    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


import platform


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    mywin=Toplevel()
    mywin.ui_nameshow.set("Hi\nDeveloper")
    mywin.show()
