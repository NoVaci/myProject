# Simple enough, just import everything from tkinter.
from tkinter import *

# download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk
import os
from time import sleep
# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master = None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master
        self.rootPath = "./"
        self.imgNum = 0
        # Array of Images
        self.arrImg = []

        # Coordinates
        self.x = 0
        self.y = 0

        # Size
        self.width = 0
        self.height = 300
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill = BOTH, expand = 1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu = menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label = "Exit", command = self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label = "File", menu = file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label = "Show Img", command = self.loadImg)

        # added "file" to our menu
        menu.add_cascade(label = "Edit", menu = edit)

        self.master.bind("<Button-1>", self.onClick)

    def loadImg(self):
        for file in os.listdir(self.rootPath):
            if file[-3:] in ['jpg']:
                self.image = Image.open(self.rootPath + file)
                self.image = self.image.resize((300, 300), Image.ANTIALIAS)
                self.showImg(self.rootPath + file)
                self.imgNum += 1
                self.width += 300

    def showImg(self, path):
        render = ImageTk.PhotoImage(self.image)

        # labels can be text or images
        lbl = Label(self, image = render, text = path)
        lbl.image = render
        self.arrImg.append(lbl)
        lbl.grid(column = self.imgNum, row = 0)
        lbl.bind("<Button-1>", self.zoomImage)
    #     self.lbl.bind("<Button-1>", self.zoomImage)
    #     self.lbl.bind("<Button-3>", self.unZoomImage)
    #
    def onClick(self, event):
        x = event.x
        self.x  = int(x / 300)
        print('coor: {}, index: {}'.format(x,self.x))

    def motion(self, event):
        x, y = event.x, event.y
        print('{},{}'.format(x,y))

    def zoomImage(self, event):
        imgWin = Toplevel()
        imgWin.title('Full Size')
        imgFull = Image.open(self.arrImg[self.x].cget('text'))
        self.imgFull = ImageTk.PhotoImage(imgFull)
        imgWin.config(height = self.imgFull.height(), width = self.imgFull.width())
        # container = Canvas(imgWin)
        # container.pack(side = TOP, fill = BOTH, expand = True)
        container = Label(imgWin, image = self.imgFull)
        container.config(height = self.imgFull.height(), width = self.imgFull.width())
        container.pack()
        # container.create_image(300, 300, image = self.imgFull)
        imgWin.bind("<Button-3>", imgWin.destroy)

    def unZoomImage(self, event):
        self.lbl.config(image = '')
        self.image = Image.open("Fox&Ice.jpg")
        self.image = self.image.resize((300, 300), Image.ANTIALIAS)
        self.showImg()

    def client_exit(self):
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

# creation of an instance
app = Window(root)
root.config(height = app.height, width = app.width)
# mainloop

root.mainloop()

