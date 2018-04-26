# w=10000
# h=10000
# m=500
# import tkinter
#
# root = tkinter.Tk()
#
# canvas=tkinter.Canvas(root, width=400,height=400,bg='white',scrollregion=[0,0,w,h])
#
# vscrollbar = tkinter.Scrollbar(root,orient="vertical")
# canvas.config(yscrollcommand=vscrollbar.set)
# vscrollbar.config(command=canvas.yview)
#
# hscrollbar = tkinter.Scrollbar(root,orient="horizontal")
# canvas.config(xscrollcommand=hscrollbar.set)
# hscrollbar.config(command=canvas.xview)
#
# hscrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
# vscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# canvas.pack(side=tkinter.LEFT, fill="both", expand=True)
#
# root.mainloop()

# import tkinter as tk
#
# def populate(frame):
#     '''Put in some fake data'''
#     for row in range(100):
#         tk.Label(frame, text="%s" % row, width=3, borderwidth="1",
#                  relief="solid").grid(row=row, column=0)
#         t="this is the second column for row %s" %row
#         tk.Label(frame, text=t).grid(row=row, column=1)
#
# def onFrameConfigure(canvas):
#     '''Reset the scroll region to encompass the inner frame'''
#     canvas.configure(scrollregion=canvas.bbox("all"))
#
# root = tk.Tk()
# canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
# frame = tk.Frame(canvas, background="#ffffff")
# vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
# canvas.configure(yscrollcommand=vsb.set)
#
# vsb.pack(side="right", fill="y")
# canvas.pack(side="left", fill="both", expand=True)
# canvas.create_window((4,4), window=frame, anchor="nw")
#
# frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
#
# populate(frame)
#
# root.mainloop()
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
koniec=Toplevel()
koniec.minsize(width=200, height=250)
koniec.title("Vítaz!")
canvas = Canvas(koniec, width=200, height=200)
canvas.pack()
tmp = Image.open('girl01.jpg')
img=ImageTk.PhotoImage(tmp)
canvas.create_image(100,100,image=img)
root.mainloop()
