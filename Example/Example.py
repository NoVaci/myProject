# import tkinter as tk
#
# counter = 0
#
#
# def counter_label(label):
#     def count():
#         global counter
#         counter += 1
#         label.config(text = str(counter))
#         label.after(1000, count)
#
#     count()
#
#
# root = tk.Tk()
# root.title("Counting Seconds")
# label = tk.Label(root, fg = "green")
# label.pack()
# counter_label(label)
# button = tk.Button(root, text = 'Stop', width = 25, command = root.destroy)
# button.pack()
# root.mainloop()

# from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
#
# class Calculator:
#
#     def __init__(self, master):
#         self.master = master
#         master.title("Calculator")
#
#         self.total = 0
#         self.entered_number = 0
#
#         self.total_label_text = IntVar()
#         self.total_label_text.set(self.total)
#         self.total_label = Label(master, textvariable=self.total_label_text)
#
#         self.label = Label(master, text="Total:")
#
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
#
#         self.add_button = Button(master, text="+", command=lambda: self.update("add"))
#         self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
#         self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))
#
#         # LAYOUT
#
#         self.label.grid(row=0, column=0, sticky=W)
#         self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
#
#         self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
#
#         self.add_button.grid(row=2, column=0)
#         self.subtract_button.grid(row=2, column=1)
#         self.reset_button.grid(row=2, column=2, sticky=W+E)
#
#     def validate(self, new_text):
#         if not new_text: # the field is being cleared
#             self.entered_number = 0
#             return True
#
#         try:
#             self.entered_number = int(new_text)
#             return True
#         except ValueError:
#             return False
#
#     def update(self, method):
#         if method == "add":
#             self.total += self.entered_number
#         elif method == "subtract":
#             self.total -= self.entered_number
#         else: # reset
#             self.total = 0
#
#         self.total_label_text.set(self.total)
#         self.entry.delete(0, END)
#
# root = Tk()
# my_gui = Calculator(root)
# root.mainloop()

# #!/usr/bin/env python
# import tkinter as tk
#
# def cbc(id, tex):
#     return lambda : callback(id, tex)
#
# def callback(id, tex):
#     s = 'At {} f is {}\n'.format(id, id**id/0.987)
#     tex.insert(tk.END, s)
#     tex.see(tk.END)             # Scroll if necessary
#
# top = tk.Tk()
# tex = tk.Text(master=top)
# tex.pack(side=tk.RIGHT)
# bop = tk.Frame()
# bop.pack(side=tk.LEFT)
# for k in range(1,10):
#     tv = 'Say {}'.format(k)
#     b = tk.Button(bop, text=tv, command=cbc(k, tex))
#     b.pack()
#
# tk.Button(bop, text='Exit', command=top.destroy).pack()
# top.mainloop()

# import tkinter as tk

# class ExampleApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         t = SimpleTable(self, 10,2)
#         t.pack(side="top", fill="x")
#         t.set(0,0,"Hello, world")
#
# class SimpleTable(tk.Frame):
#     def __init__(self, parent, rows=10, columns=2):
#         # use black background so it "peeks through" to
#         # form grid lines
#         tk.Frame.__init__(self, parent, background="black")
#         self._widgets = []
#         for row in range(rows):
#             current_row = []
#             for column in range(columns):
#                 label = tk.Label(self, text="%s/%s" % (row, column),
#                                  borderwidth=0, width=10)
#                 label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
#                 current_row.append(label)
#             self._widgets.append(current_row)
#
#         for column in range(columns):
#             self.grid_columnconfigure(column, weight=1)
#
#
#     def set(self, row, column, value):
#         widget = self._widgets[row][column]
#         widget.configure(text=value)
#
# if __name__ == "__main__":
#     app = ExampleApp()
#     app.mainloop()

# class SampleApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         lb = tk.Listbox(self)
#         lb.insert("end", "one")
#         lb.insert("end", "two")
#         lb.insert("end", "three")
#         lb.bind("<Double-Button-1>", self.OnDouble)
#         lb.pack(side="top", fill="both", expand=True)
#
#     def OnDouble(self, event):
#         widget = event.widget
#         selection=widget.curselection()
#         value = widget.get(selection[0])
#         print("selection:", selection, ": '%s'" % value)
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()

# from tkinter import *
# from tkinter import messagebox
#
# def answer():
#     messagebox.showerror("Answer", "Sorry, no answer available")
#
# def callback():
#     if messagebox.askokcancel('Verify', 'Really quit?'):
#         messagebox.showwarning('Yes', 'Not yet implemented')
#     # else:
#     #     messagebox.showinfo('No', 'Quit has been cancelled')
#
# Button(text='Quit', command=callback).pack(fill=X)
# Button(text='Answer', command=answer).pack(fill=X)
# mainloop()

#========================================================================
# Progress bar displays in different direction.
# try:
#   import Tkinter              # Python 2
#   import ttk
# except ImportError:
#   import tkinter as Tkinter   # Python 3
#   import tkinter.ttk as ttk
#   import sys


# def main():
#
#   root = Tkinter.Tk()
#
#   ft = ttk.Frame()
#   fb = ttk.Frame()
#
#   ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
#   fb.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
#
#   pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
#   pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
#   pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
#   pb_vD = ttk.Progressbar(fb, orient='vertical', mode='indeterminate')
#
#   pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
#   pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
#   pb_vd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
#   pb_vD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.LEFT)
#
#   pb_hd.start(50)
#   pb_hD.start(50)
#   pb_vd.start(50)
#   pb_vD.start(50)
#
#   root.mainloop()
#
#
# if __name__ == '__main__':
#   main()

# from tkinter import *
# # import sys
# # ABOUT_TEXT = """About
# #
# # SPIES will search your chosen directory for photographs containing
# # GPS information. SPIES will then plot the co-ordinates on Google
# # maps so you can see where each photograph was taken."""
# #
# # DISCLAIMER = """
# # Disclaimer
# #
# # Simon's Portable iPhone Exif-extraction Software (SPIES)
# # software was made by Simon. This software
# # comes with no guarantee. Use at your own risk"""
# #
# # def clickAbout():
# #     toplevel = Toplevel()
# #     label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
# #     label1.pack()
# #     label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
# #     label2.pack()
# #
# #
# # app = Tk()
# # app.title("SPIES")
# # app.geometry("500x300+200+200")
# #
# # label = Label(app, text="Please browse to the directory you wish to scan", height=0, width=100)
# # b = Button(app, text="Quit", width=20, command=app.destroy)
# # button1 = Button(app, text="About SPIES", width=20, command=clickAbout)
# # label.pack()
# # b.pack(side='bottom',padx=0,pady=0)
# # button1.pack(side='bottom',padx=5,pady=5)
# #
# # app.mainloop()
#
# from tkinter import * # Tkinter -> tkinter in Python 3
#
# root = Tk()
#
# def hello():
#     print("hello!")
#
# # create a popup menu
# menu = Menu(root, tearoff=0)
# menu.add_command(label="Undo", command=hello)
# menu.add_command(label="Redo", command=hello)
#
# # create a frame
# frame = Frame(root, width=512, height=512)
# frame.pack()
#
# def popup(event):
#     menu.post(event.x_root, event.y_root)
#
# # attach popup to frame
# frame.bind("<Button-3>", popup)
#
# root.mainloop()
# CREATE VIEW COMPANY_VIEW AS
# SELECT ID, NAME, AGE
# FROM  COMPANY;
import sqlite3

conn = sqlite3.connect('test.db')
# conn.execute('''CREATE TABLE COMPANY
#          (ID       INT PRIMARY KEY        NOT NULL,
#          NAME      TEXT                   NOT NULL,
#          AGE       INT                    NOT NULL,
#          ADDRESS   CHAR(50),
#          SALARY    REAL);''')
# conn.execute("INSERT INTO COMPANY (ID, NAME, AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")
# conn.execute('INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \ '
#              'VALUES (4, "PAllen", 25, "Texas", 15000.00 )')
# conn.commit()
# conn.execute("UPDATE COMPANY set SALARY = %s where ID = 1" % 3000)
# name = "i've done it"       # \\'ve
# # name = name.replace('\'', '\\\'')
# conn.execute('UPDATE COMPANY set NAME = "%s" where ID = 1' % name)
# conn.execute('create view paul as \
#               select id, name, age \
#               from company')

# cursor = conn.execute('select name from sqlite_master where type="table" and name = "company"')
# data = cursor.fetchall()

# conn.commit()
cursor = conn.execute('select * from company')
data = cursor.fetchall()
print(type(data))
print(data)
for row in cursor:
   print("title = ", row[0])
   print("lang = ", row[1])
   print('size = ', row[2])
   print('page = ', row[3])
   print('time = ', row[4])
   print('cmt = ', row[5])

conn.close()