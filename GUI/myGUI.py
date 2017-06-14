from tkinter import *
from tkinter import messagebox

from Tools.Tool import Tool
import threading
import subprocess
from Tools.ProgressBar import ProgressBar
from time import sleep

class myGUI():
    def __init__(self, parent):
        self.parent = parent
        parent.title('My test GUI')

        self.tool = Tool()
        self.dirPath = (u"I:\H-Colle\\")
        self.PATHLIST = (
            u"I:\H-Colle\\",
            u"H:\Doujin-Manga\\",
            u"H:\Doujin-Manga\\test\\"
        )

        self.pathVar = StringVar()
        self.nameVar = StringVar()
        self.threads = []

        self.dbName  = 'test.txt'
        self.favFile = 'fav.txt'

        self.db      = self.tool.readDB(self.dirPath + self.dbName)
        self.fav     = {} # self.tool.readDB(self.dirPath + self.favFile)

        # Store searched list
        self.searchedList = []

        # Variables to show detail
        self.title   = StringVar()
        self.lang    = StringVar()
        self.size    = StringVar()
        self.page    = StringVar()
        self.ctime   = StringVar()

        self.barVar  = StringVar()

    def initializeGUI(self, parent):
        frameInput = Frame(parent)  # Test: input + button in 1 frame
        frameInput.grid(column = 0, row = 0, sticky = N)

        # ----------------------------------------------------
        # Top-left: path input
        # ----------------------------------------------------
        Label(frameInput, text = 'Path', fg = 'red').grid(column = 0, row = 0, sticky = NW)
        self.pathVar.set(self.PATHLIST[0])
        pathList  = OptionMenu(frameInput, self.pathVar, *self.PATHLIST)
        pathList.grid(column = 1, row = 0, columnspan = 3, sticky = NW)

        # Seach box
        Button(frameInput, text = 'Search', fg = 'blue',
                    command = lambda: self.__threadCall(self.searchAndShow, self.nameVar.get(), selection)) \
                    .grid(column = 0, row = 1, sticky = NW)

        Button(frameInput, text = 'Load Comic', fg = 'blue',
                command = lambda: self.__threadCall(self.loadComic)) \
                .grid(column = 1, row = 1, sticky = NW)

        nameSearch = Entry(frameInput, textvariable = self.nameVar, width = 30)
        nameSearch.grid(column = 0, row = 2, columnspan = 3, sticky = NW, padx = 2)
        nameSearch.focus_set()
        nameSearch.bind("<Return>", lambda event: self.searchAndShow(self.nameVar.get(), selection))

        # Detail Info show
        #   Title: <name>
        #   Language: <Eng/Jap>
        #   Size:
        headerText = 'First Entry ' + ('-' * 45)
        Label(frameInput, text = headerText, fg = 'blue').grid(column = 0, row = 3, pady = 20, sticky = W, columnspan = 2)
        Label(frameInput, text = 'Title:').grid(column = 0, row = 4, sticky = W)
        Label(frameInput, textvariable = self.title, wraplength = 100, justify = CENTER).grid(column = 1, row = 4, sticky = W)

        Label(frameInput, text = 'Language:').grid(column = 0, row = 5, sticky = W)
        Label(frameInput, textvariable = self.lang).grid(column = 1, row = 5, sticky = W)

        Label(frameInput, text = 'Size:').grid(column = 0, row = 6, sticky = W)
        Label(frameInput, textvariable = self.size).grid(column = 1, row = 6, sticky = W)

        Label(frameInput, text = 'Pages:').grid(column = 0, row = 7, sticky = W)
        Label(frameInput, textvariable = self.page).grid(column = 1, row = 7, sticky = W)

        Label(frameInput, text = 'Create Date:').grid(column = 0, row = 8, sticky = W)
        Label(frameInput, textvariable = self.ctime).grid(column = 1, row = 8, sticky = W)

        # ----------------------------------------------------
        # Right: output screen
        # Consist of
        # ----------------------------------------------------

        frameOutput = Frame(parent)
        frameOutput.grid(column = 1, row = 0, rowspan = 2, sticky = W)

        Label(frameOutput, text = 'Output').grid(column = 0, row = 2, sticky = W)
        # this will receive the output from console
        textField = Text(frameOutput)
        textField.grid(column = 0, row = 3, sticky = N+S+E+W)
        textField.grid_columnconfigure(0, weight = 1)

        Label(frameOutput, text = 'Result').grid(column = 0, row = 0, sticky = W)
        selection = Listbox(frameOutput, height = 15, width = 160)
        selection.bind("<Double-Button-1>", self.__onDoubleClick)
        selection.grid(column = 0, row = 1, sticky = W)

        # Section for pop up menu
        self.popMenu = Menu(parent, tearoff = 0)
        self.popMenu.add_command(label = 'Add Fav', command = lambda : self.saveToFavourite(selection))
        self.popMenu.add_command(label = 'Open Location', command = '')

        selection.bind("<Button-3>", self.popupMenu)
        # # Try to do resize. Wrong -> Hanging
        # selection.grid_columnconfigure(0, weight = 1)
        # selection.bind('<Configure>', self.__resize)

        # ----------------------------------------------------
        # Bottom-left: set of buttons
        # ----------------------------------------------------
        frameBtn = Frame(parent)
        frameBtn.grid(column = 0, row = 1, sticky = W)

        btnCompZip  = Button(frameBtn, text = 'Zip Compress',
                             command = lambda : self.__threadCall(self.zipFolder, textField))

        btnCreateDB = Button(frameBtn, text = 'Create DB',
                             command = lambda: self.__threadCall(self.createDB))

        btnLoadDB   = Button(frameBtn, text = 'Load DB',
                             command = self.__loadDB)

        btnLoadFav = Button(frameBtn, text = 'Load Fav',
                           command = lambda : self.loadFavorite(selection))

        btnDelete   = Button(frameBtn, text = 'Remove',
                             command = self.__delSelected)
        btnTest     = Button(frameBtn, text = 'Test',
                             command = lambda : self.__threadCall(self.popUpPB, self.tool.getTotalFolder(self.pathVar.get())))

        # btnCompZip.pack(side = TOP, padx = 10)
        btnCompZip.grid(column = 0, row = 0, sticky = 'nsew')
        btnCreateDB.grid(column = 1, row = 0, sticky = 'nsew')
        btnLoadDB.grid(column = 2, row = 0, sticky = 'nsew')
        btnLoadFav.grid(column = 3, row = 0, sticky = 'nsew')
        btnDelete.grid(column = 0, row = 1, sticky = 'nsew')
        # btnTest.grid(column = 0, row = 1, sticky = 'nsew')

    def __getCurrentEntry(self):
        # Return the file path of current selected entry
        ext = '.pdf' if self.page.get() == '0' else '.zip'
        path = self.pathVar.get() + self.title.get() + ext
        path.replace('\\', r'\\')
        return path

    def __threadCall(self, sFunc, *args):
        qThread = threading.Thread(target = sFunc, args = args)
        self.threads.append(qThread)
        qThread.start()

    def __onDoubleClick(self, event):
        # Double click to load search result to listbox
        widget = event.widget
        value  = self.loadSelected(self.searchedList, widget)
        self.loadEntry(value)

    def __loadDB(self):
        # function to load DB to self.db
        self.db = self.tool.readDB(self.pathVar.get() + self.dbName)

    def zipFolder(self, textField):
        self.__threadCall(self.popUpPB, self.tool.getTotalFolder(self.pathVar.get()), 'zip')
        self.tool.compressSeparateFolder(self.pathVar.get(), textField)

    def searchAndShow(self, string, lboxWg):
        # Function to search for an input in database and show result on a list
        #TODO: try to find a way searching regardless case sensitive
        if string == '':
            self.loadAll(lboxWg)
        else:
            lstRes_lower    = list(filter(lambda x: string.lower() in x, self.db.keys()))
            lstRes_title   = list(filter(lambda x: string.title() in x, self.db.keys()))
            lstRes_caps     = list(filter(lambda x: string.capitalize() in x, self.db.keys()))
            lstRes = lstRes_lower + lstRes_caps + lstRes_title

            lstRes.sort()

            if len(lstRes) > 0:
                firstEntry = lstRes[0]
                self.searchedList = lstRes
            else:
                firstEntry = 'Not Found'

            self.loadResult(lstRes, lboxWg)
            self.loadEntry(firstEntry)

    def whichSelected(self, lboxWg) :
        return int(lboxWg.curselection()[0])

    def loadEntry(self, input):
        self.title.set(input)
        if input == 'Not Found':
            self.lang.set('')
            self.size.set('')
            self.page.set('')
            self.ctime.set('')
        else:
            self.lang.set(self.db[input]['lang'])
            self.size.set(self.db[input]['size'])
            self.page.set(self.db[input]['page'])
            self.ctime.set(self.db[input]['ctime'])

    def loadAll(self, lboxWg):
        # Function to load all title and show in listbox
        lstAll = list(self.db.keys())
        lstAll.sort()
        self.searchedList = lstAll
        self.loadResult(lstAll, lboxWg)

    def loadResult(self, lstSearch, lboxWg):
        # Function to load the list of search result to listbox
        lstSearch.sort()
        lboxWg.delete(0, END)

        for title in lstSearch:
            lboxWg.insert(END, title)

    def loadSelected(self, lst, lboxWg):
        return lst[self.whichSelected(lboxWg)]

    def loadComic(self):
        # Function to open up CDisplayex and load the current selected entry
        # For manual test:
        # subprocess.call('C:\\Program Files\\CDisplayEx\\CDisplayEx.exe "H:\\Doujin-Manga\\<>.zip"'
        tail = '.pdf' if self.page.get() == '0' else '.zip'
        pathToFile = self.pathVar.get() + self.title.get() + tail
        pathToFile.replace('\\', r'\\')
        subprocess.call('C:\\Program Files\\CDisplayEx\\CDisplayEx.exe "%s"' % pathToFile)

    def loadFavorite(self, lboxWg):
        self.fav = self.tool.readDB(self.pathVar.get() + self.favFile)
        self.searchedList = list(self.fav.keys())
        self.loadResult(self.searchedList, lboxWg)

    def saveToFavourite(self, lboxWg):
        # Function to save current selected entry to favourite list.
        with open(self.pathVar.get() + self.favFile, mode = 'ab') as fWrite:
            selectFile = self.loadSelected(self.searchedList, lboxWg)
            tmpLang = self.db[selectFile]['lang']
            tmpSize = self.db[selectFile]['size']
            tmpPage = self.db[selectFile]['page']
            tmpCTime = self.db[selectFile]['ctime']
            selectFile += '#' + tmpLang + '#' + tmpSize + '#' + tmpPage + '#' + tmpCTime + '\r\n'
            selectFile = selectFile.encode('utf-8')
            fWrite.write(selectFile)

    def createDB(self):
        # function to trigger generating database.
        if messagebox.askokcancel("Verify", "Are you sure?"):
            self.__threadCall(self.popUpPB, self.tool.getTotalZip(self.pathVar.get()), 'db')
            self.tool.createDatabase(self.pathVar.get(), self.dbName)
            # self.__threadCall(self.tool.createDatabase, self.pathVar.get(), self.dbName)

            # Load DB
            self.__loadDB()

    def popUpPB(self, *args):
        # Fucntion to open a popup when a task is running, progress bar is included
        # param args:
        #       1. total
        #       2. current progress
        self.newWin = Toplevel()
        self.newWin.title('Processing...')
        pbarLabel = Label(self.newWin, textvariable = self.barVar, height = 5, width = 70)
        pbarLabel.pack()

        pbar   = ProgressBar(args[0], fmt = ProgressBar.FULL)
        while pbar.current < pbar.total:
            pbar.current = self.tool.getCurrentZip() if args[1] == 'zip' else self.tool.getCurrentDB()
            self.barVar.set(pbar())
            sleep(0.1)
        self.barVar.set(pbar.done())

    def popupMenu(self, event):
        self.popMenu.post(event.x_root, event.y_root)

    # def __resize(self, event):
    #     widg = event.widget
    #     width, height = event.width - 100, event.height - 100
    #     widg.config(width = width, height = height)

    def __delSelected(self):
        if messagebox.askyesnocancel('Are you sure?', 'This will delete the file completely.'):
            self.tool.removeIfExist(self.__getCurrentEntry())
            # Remove from DB
            try:
                del self.db[self.title.get()]
                messagebox.showinfo('Complete', "DB needs to be re-created.")
            except KeyError:
                messagebox.showwarning('Warning', 'Entry %s not exist.' % self.title.get())

if __name__ == '__main__':
    root = Tk()
    root.minsize(height = 300, width = 400)
    root.resizable(True, True)
    app = myGUI(root)
    app.initializeGUI(root)
    root.mainloop()
