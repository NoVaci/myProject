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

from tkinter import *

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

root = Tk()

height = 5
width = 5
for i in range(height): #Rows
    for j in range(width): #Columns
        b = Entry(root, text="")
        b.grid(row=i, column=j)

mainloop()