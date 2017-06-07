from tkinter import *
from Tool import Tool
import threading

class myGUI():
    def __init__(self, parent):
        self.parent = parent
        parent.title('My test GUI')
        self.tool = Tool()
        self.dirPath = (u"H:/Doujin-Manga/test/")
        self.pathVar = StringVar()
        self.threads = []

    def initializeGUI(self, parent):
        frameInput = Frame(parent)  # Test: input + button in 1 frame
        frameInput.grid(column = 0, row = 0, sticky = N)

        # ----------------------------------------------------
        # Top-left: path input
        # ----------------------------------------------------
        # Label(frameInput, text = 'Path', fg = 'red').grid(column = 0, row = 0, sticky = NW)
        Label(frameInput, text = 'Path', fg = 'red').pack(side = LEFT)
        pathEntry = Entry(frameInput, textvariable = self.pathVar)
        # pathEntry.grid(column = 0, row = 0, sticky = W)
        pathEntry.pack(side = LEFT, padx = 10)
        self.pathVar.set(u"%s" % self.dirPath)

        # ----------------------------------------------------
        # Right: output screen
        # ----------------------------------------------------
        frameOutput = Frame(parent)
        frameOutput.grid(column = 1, row = 0, rowspan = 2, sticky = E)

        Label(frameOutput, text = 'Output').grid(column = 1, row = 0, sticky = W)
        outVar = StringVar()
        textField = Text(frameOutput)
        textField.grid(column = 1, row = 1)

        #TODO: this will receive the output from console

        # ----------------------------------------------------
        # Bottom-left: set of buttons
        # ----------------------------------------------------
        frameBtn = Frame(parent)
        frameBtn.grid(column = 0, row = 1, sticky = W)

        #TODO: add the related function
        btnList = Button(frameBtn, text = 'List', command = self.tool.listCompressed(self.pathVar.get()))

        btnCompZip = Button(frameBtn, text = 'Zip Compress', command = lambda : self.tool.compressSeparateFolder(self.pathVar.get(), textField))

        btnDB      = Button(frameBtn, text = 'View DB', command = '')

        # btnTest    = Button(frameBtn, text = 'Test', command = lambda : self.test(self.pathVar.get(), textField))
        btnTest = Button(frameBtn, text = 'Test', command = lambda: self.threadCall(self.tool.compressSeparateFolder, self.pathVar.get(), textField))

        btnList.pack(side = LEFT) ; btnCompZip.pack(side = LEFT, padx = 10)
        btnDB.pack(side = LEFT, anchor = 'sw') ; btnTest.pack(side = LEFT, anchor = 'sw')
        #
        # # select = Listbox(frameOutput, y)
        # scroll = Scrollbar(frameOutput, orient = VERTICAL)
        # # scroll.config(command = sele)
        # # scroll.(side = RIGHT, fill = Y)

    def showOutput(self, sOutput, textWg):
        textWg.insert(END, sOutput + '\n')
        textWg.see(END)

    def test(self, sOutput, textWg):
        self.showOutput(sOutput, textWg)

    def threadCall(self, sFunc, *args):
        # tArg = ()
        # for arg in args:
        #     tArg += (arg,)
        qThread = threading.Thread(target = sFunc, args = args)
        self.threads.append(qThread)
        qThread.start()

if __name__ == '__main__':
    root = Tk()
    root.minsize(height = 300, width = 400)
    app = myGUI(root)
    app.initializeGUI(root)
    root.mainloop()
