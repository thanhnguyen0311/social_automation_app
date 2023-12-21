import tkinter as tk
from tkinter import ttk


class FBManager(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Facebook Service")
        self.geometry("800x600")
        self.is_open = True
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

        button_frame = tk.Frame(self)
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)
        button_add = tk.Button(button_frame, text="ADD", width=10, height=2)
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame, text="REFRESH", width=10, height=2)
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame, text="REMOVE", width=10, height=2)
        button_remove.grid(row=0, column=2, padx=5)
        button_action = tk.Button(button_frame, text="RUN TASK", width=10, height=2)
        button_action.grid(row=0, column=3, padx=5)

        self.fb_account_list = FBAccountsList(self)

    def on_close(self):
        self.destroy()
        self.is_open = False


class FBAccountsList(ttk.Treeview):
    def __init__(self, master=None):
        ttk.Treeview.__init__(self, master, columns=("Select", "ID", "email", "password", "device", "status", "action"),
                              show="headings", selectmode="extended")

        self._im_checked = tk.PhotoImage('checked',
                                         data=b'GIF89a\x0e\x00\x0e\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x0e\x00\x0e\x00\x00\x02#\x04\x82\xa9v\xc8\xef\xdc\x83k\x9ap\xe5\xc4\x99S\x96l^\x83qZ\xd7\x8d$\xa8\xae\x99\x15Zl#\xd3\xa9"\x15\x00;',
                                         master=self)
        self._im_unchecked = tk.PhotoImage('unchecked',
                                           data=b'GIF89a\x0e\x00\x0e\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x0e\x00\x0e\x00\x00\x02\x1e\x04\x82\xa9v\xc1\xdf"|i\xc2j\x19\xce\x06q\xed|\xd2\xe7\x89%yZ^J\x85\x8d\xb2\x00\x05\x00;',
                                           master=self)
        style = ttk.Style(self)
        style.configure("cb.Treeview.Heading", font=(None, 13))
        style.layout('cb.Treeview.Row',
                     [('Treeitem.row', {'sticky': 'nswe'}),
                      ('Treeitem.image', {'side': 'right', 'sticky': 'e'})])

        # use tags to set the checkbox state
        self.tag_configure('checked', image='checked')
        self.tag_configure('unchecked', image='unchecked')

        self.heading("Select", text="")
        self.heading("ID", text="ID")
        self.heading("email", text="Email")
        self.heading("password", text="Password")
        self.heading("device", text="Device")
        self.heading("status", text="Status")
        self.heading("action", text="Action")

        self.column("Select", width=5, anchor='center')
        self.column("ID", width=10, anchor='center')
        self.column("email", width=120, anchor='center')
        self.column("password", width=80, anchor='center')
        self.column("device", width=120, anchor='center')
        self.column("status", width=50, anchor='center')
        self.column("action", width=50, anchor='center')

        data = [
            ('', 0, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
            ('',1, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
            ('',2, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
        ]

        for i, (Select, ID, email, password, device, status) in enumerate(data):
            item_id = self.insert("", "end",
                                  values=(Select, ID, email, password, device, status))
            print(Select)

        self.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def tag_add(self, item, tags):
        new_tags = tuple(self.item(item, 'tags')) + tuple(tags)
        self.item(item, tags=new_tags)

    def tag_remove(self, item, tag):
        tags = list(self.item(item, 'tags'))
        tags.remove(tag)
        self.item(item, tags=tags)

    def insert(self, parent, index, iid=None, **kw):
        item = ttk.Treeview.insert(self, parent, index, iid, **kw)
        self.tag_add(item, (item, 'unchecked'))
        self.tag_bind(item, '<ButtonRelease-1>',
                      lambda event: self._on_click(event, item))

    def _on_click(self, event, item):
        """Handle click on items."""
        if self.identify_row(event.y) == item:
            if self.identify_column(event.x) == 'Select':  # click in 'Served' column\
                print("clicked")
                # toggle checkbox image
                if self.tag_has('checked', item):
                    self.tag_remove(item, 'checked')
                    self.tag_add(item, ('unchecked',))
                else:
                    self.tag_remove(item, 'unchecked')
                    self.tag_add(item, ('checked',))
