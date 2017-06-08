from tkinter import *
from Tools.Tool import Tool
import threading

class myGUI():
    def __init__(self, parent):
        self.parent = parent
        parent.title('My test GUI')
        self.tool = Tool()
        self.dirPath = (u"H:/Doujin-Manga/test/")
        self.pathVar = StringVar()
        self.nameVar = StringVar()
        self.threads = []

        self.dbName  = 'mainDB.txt'

        # self.db      = self.tool.readDB(self.dirPath + self.dbName)

    def initializeGUI(self, parent):
        frameInput = Frame(parent)  # Test: input + button in 1 frame
        frameInput.grid(column = 0, row = 0, sticky = N)

        # ----------------------------------------------------
        # Top-left: path input
        # ----------------------------------------------------
        Label(frameInput, text = 'Path', fg = 'red').grid(column = 0, row = 0, sticky = NW)
        # Label(frameInput, text = 'Path', fg = 'red').pack(side = LEFT)
        pathEntry = Entry(frameInput, textvariable = self.pathVar)
        pathEntry.grid(column = 1, row = 0, columnspan = 2, sticky = NW)
        # pathEntry.pack(side = LEFT, padx = 10)
        self.pathVar.set(u"%s" % self.dirPath)

        # Seach box
        Button(frameInput, text = 'Search', fg = 'blue', command = lambda: self.searchAndShow(self.nameVar.get())) \
                    .grid(column = 0, row = 1, sticky = NW)
        nameSearch = Entry(frameInput, textvariable = self.nameVar, width = 30)
        nameSearch.grid(column = 0, row = 2, columnspan = 3, sticky = NW, padx = 2)

        # Detail Info show
        Label(frameInput, text = 'First Entry--------------', fg = 'blue').grid(column = 0, row = 3, pady = 20, sticky = W)
        Label(frameInput, text = 'Language:').grid(column = 0, row = 4, sticky = W)
        Label(frameInput, text = 'Size:').grid(column = 0, row = 5, sticky = W)

        # ----------------------------------------------------
        # Right: output screen
        # Consist of
        # ----------------------------------------------------

        frameOutput = Frame(parent)
        frameOutput.grid(column = 1, row = 0, rowspan = 2, sticky = E)

        Label(frameOutput, text = 'Output').grid(column = 0, row = 2, sticky = W)
        # this will receive the output from console
        textField = Text(frameOutput)
        textField.grid(column = 0, row = 3)

        Label(frameOutput, text = 'Result').grid(column = 0, row = 0, sticky = W)
        scrollRes = Scrollbar(frameOutput, orient = VERTICAL)
        selection = Listbox(frameOutput, yscrollcommand = scrollRes.set, height = 15, width = 107)
        scrollRes.config(command = selection.yview)
        scrollRes.grid(column = 1, row = 1, sticky = E)
        selection.grid(column = 0, row = 1, sticky = W)

        # framePad = Frame(parent)
        # framePad.grid(column = 0, row = 2)
        # ----------------------------------------------------
        # Bottom-left: set of buttons
        # ----------------------------------------------------
        frameBtn = Frame(parent)
        frameBtn.grid(column = 0, row = 1, sticky = W)

        btnCompZip = Button(frameBtn, text = 'Zip Compress', command = lambda : self.tool.compressSeparateFolder(self.pathVar.get(), textField))

        btnDB      = Button(frameBtn, text = 'View DB', command = '')

        # btnTest    = Button(frameBtn, text = 'Test', command = lambda : self.test(self.pathVar.get(), textField))
        btnTest = Button(frameBtn, text = 'Test', command = lambda: self.threadCall(self.tool.compressSeparateFolder, self.pathVar.get(), textField))

        # btnCompZip.pack(side = TOP, padx = 10)
        btnCompZip.grid(column = 0, row = 0, sticky = 'nsew')


    def showOutput(self, sOutput, textWg):
        textWg.insert(END, sOutput + '\n')
        textWg.see(END)

    def test(self, sOutput, textWg):
        self.showOutput(sOutput, textWg)

    def searchAndShow(self, string):
        if string in self.db.keys():
            #TODO: return the  value into appropriate fields
            pass

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
