from tkinter import *
from tkinter import messagebox

try:
    from Tools.Tool import Tool
    from Tools.ProgressBar import ProgressBar
except ImportError:
    from Tool import *
    from ProgressBar import  *
import threading
import subprocess
from time import sleep
import sqlite3

#TODO: 6/14/2017: add remove fav entry.
#TODO: 6/30/2017: check for existing entry in fav
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

        self.curPath = ''

        self.mainDB  = 'test.db'
        self.favDB = 'fav.db'

        self.db      = self.tool.readDB(self.dirPath + self.mainDB, self.tool.mainTableName)
        self.fav     = self.tool.readDB(self.dirPath + self.favDB, self.tool.favTableName)

        # Store searched list
        self.searchedList = []

        # Variables to show detail
        self.title   = StringVar()
        self.lang    = StringVar()
        self.size    = StringVar()
        self.page    = StringVar()
        self.ctime   = StringVar()
        self.visit   = StringVar()
        self.tags    = StringVar()
        self.cmt     = StringVar()
        self.cutTitle= StringVar()

        self.barVar  = StringVar()
        self.cmtVar  = StringVar()

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
        self.curPath = self.pathVar.get()
        pathList.bind("<Button-1>", lambda event: self.__threadCall(self.detectPathChange))

        # Seach box
        Button(frameInput, text = 'Search', fg = 'blue',
                    command = lambda: self.__threadCall(self.searchAndShow, self.nameVar.get(), self.selection)) \
                    .grid(column = 0, row = 1, sticky = NW)

        Button(frameInput, text = 'Load Comic', fg = 'blue',
                command = lambda: self.__threadCall(self.loadComic)) \
                .grid(column = 1, row = 1, sticky = NW)

        nameSearch = Entry(frameInput, textvariable = self.nameVar, width = 30)
        nameSearch.grid(column = 0, row = 2, columnspan = 3, sticky = NW, padx = 2)
        nameSearch.focus_set()
        nameSearch.bind("<Return>", lambda event: self.searchAndShow(self.nameVar.get(), self.selection))

        # Detail Info show
        #   Title: <name>
        #   Language: <Eng/Jap>
        #   Size:
        headerText = 'First Entry ' + ('-' * 45)
        Label(frameInput, text = headerText, fg = 'blue').grid(column = 0, row = 3, pady = 20, sticky = W, columnspan = 2)
        Label(frameInput, text = 'Title:').grid(column = 0, row = 4, sticky = W)
        Label(frameInput, textvariable = self.cutTitle, wraplength = 100, justify = CENTER).grid(column = 1, row = 4, sticky = W)

        Label(frameInput, text = 'Language:').grid(column = 0, row = 5, sticky = W)
        Label(frameInput, textvariable = self.lang).grid(column = 1, row = 5, sticky = W)

        Label(frameInput, text = 'Size:').grid(column = 0, row = 6, sticky = W)
        Label(frameInput, textvariable = self.size).grid(column = 1, row = 6, sticky = W)

        Label(frameInput, text = 'Pages:').grid(column = 0, row = 7, sticky = W)
        Label(frameInput, textvariable = self.page).grid(column = 1, row = 7, sticky = W)

        Label(frameInput, text = 'Create Date:').grid(column = 0, row = 8, sticky = W)
        Label(frameInput, textvariable = self.ctime).grid(column = 1, row = 8, sticky = W)

        Label(frameInput, text = 'Comment:').grid(column = 0, row = 9, sticky = W)
        Label(frameInput, textvariable = self.cmt, wraplength = 100, justify = LEFT).grid(column = 1, row = 9, sticky = W)

        Label(frameInput, text = 'Visit:').grid(column = 0, row = 10, sticky = W)
        Label(frameInput, textvariable = self.visit).grid(column = 1, row = 10, sticky = W)

        Label(frameInput, text = 'Tags:').grid(column = 0, row = 11, sticky = W)
        Label(frameInput, textvariable = self.tags).grid(column = 1, row = 11, sticky = W)

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
        self.selection = Listbox(frameOutput, height = 15, width = 160, exportselection = 0)
        self.selection.bind("<Double-Button-1>", self.__onDoubleClick)
        self.selection.grid(column = 0, row = 1, sticky = W)

        # Section for pop up menu
        self.popMenu = Menu(parent, tearoff = 0)
        self.popMenu.add_command(label = 'Add Fav', command = self.popupAddComment)
        self.popMenu.add_command(label = 'Remove Fav', command = self.popupWarning)
        self.popMenu.add_command(label = 'Open Location', command = self.popupWarning)

        self.selection.bind("<Button-3>", self.popupMenu)
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

        btnDownload = Button(frameBtn, text = 'Download',
                             command = self.popupDownload)

        btnCreateDB = Button(frameBtn, text = 'Create DB',
                             command = lambda: self.__threadCall(self.createDB))

        btnLoadDB   = Button(frameBtn, text = 'Load DB',
                             command = self.__loadDB)

        btnLoadFav = Button(frameBtn, text = 'Load Fav',
                           command = lambda : self.loadFavorite(self.selection))

        btnDelete   = Button(frameBtn, text = 'Remove',
                             command = self._delSelected)
        btnTest     = Button(frameBtn, text = 'Test',
                             command = lambda : self.__threadCall(self.popupPB, self.tool.getTotalFolder(self.pathVar.get())))

        # btnCompZip.pack(side = TOP, padx = 10)
        btnCompZip.grid(column = 0, row = 0, sticky = 'nsew')
        btnDownload.grid(column = 1, row = 0, sticky = 'nsew')
        btnCreateDB.grid(column = 0, row = 1, sticky = 'nsew')
        btnLoadDB.grid(column = 1, row = 1, sticky = 'nsew')
        btnLoadFav.grid(column = 2, row = 1, sticky = 'nsew')
        btnDelete.grid(column = 0, row = 2, sticky = 'nsew')
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

    def removeDuplicate(self, lTarget):
        '''
        Remove duplicate search result.
        :param lTarget: target list
        :return: list of unique result
        '''
        lRes = []
        for item in lTarget:
            if item not in lRes:
                lRes.append(item)
        return lRes

    def __loadDB(self):
        # function to load DB to self.db
        self.db = self.tool.readDB(self.pathVar.get() + self.mainDB, self.tool.mainTableName)

    def detectPathChange(self):
        # Function to load DB when detecting a change in path folder
        sleep(1)
        while(self.curPath != self.pathVar.get()):
            self.__loadDB()
            self.curPath = self.pathVar.get()

    def zipFolder(self, textField):
        self.__threadCall(self.popupPB, self.tool.getTotalFolder(self.pathVar.get()), 'zip')
        self.tool.compressSeparateFolder(self.pathVar.get(), textField)

    def searchAndShow(self, string, lboxWg):
        # Function to search for an input in database and show result on a list
        #TODO: try to find a way searching regardless case sensitive
        lstRes_caps = []
        if string == '':
            self.loadAll(lboxWg)
        else:
            lstRes_lower    = list(filter(lambda x: string.lower() in x, self.db.keys()))
            lstRes_title    = list(filter(lambda x: string.title() in x, self.db.keys()))
            lstRes_origin   = list(filter(lambda x: string in x, self.db.keys()))

            if len(string.split(' ')) > 1:
                lstRes_caps     = list(filter(lambda x: string.capitalize() in x, self.db.keys()))
            lstRes = lstRes_lower + lstRes_caps + lstRes_title + lstRes_origin
            lstRes = self.removeDuplicate(lstRes)

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
        if len(self.title.get()) > 50:
            self.cutTitle.set(self.title.get()[:50])
        else:
            self.cutTitle.set(self.title.get())

        if input == 'Not Found':
            self.lang.set('')
            self.size.set('')
            self.page.set('')
            self.ctime.set('')
            self.visit.set('')
            self.tags.set('')
            self.cmt.set('')
        else:
            self.lang.set(self.db[input]['lang'])
            self.size.set(self.db[input]['size'])
            self.page.set(self.db[input]['page'])
            self.ctime.set(self.db[input]['ctime'])
            self.visit.set(self.db[input]['visit'])
            self.tags.set(self.db[input]['tags'])
            try:
                self.cmt.set(self.fav[input]['cmt'])
            except KeyError:
                self.cmt.set('Not Added')

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
        visitCount = self.db[self.title.get()]['visit']
        visitCount += 1
        # Update to the current view
        self.db[self.title.get()]['visit'] = visitCount
        # Update to the main database
        self.tool.updateDatabase(self.pathVar.get() + self.mainDB, self.title.get(), visitCount, column = 'visit')

    def loadFavorite(self, lboxWg):
        self.fav = self.tool.readDB(self.pathVar.get() + self.favDB, self.tool.favTableName)
        self.searchedList = list(self.fav.keys())
        self.loadResult(self.searchedList, lboxWg)

    def saveToFavourite(self, lboxWg):
        '''
        Function to save current selected entry to favourite list.
        :param lboxWg: list where result is shown.
        :return: None
        '''
        dbFav = sqlite3.connect(self.pathVar.get() + self.favDB)

        selectFile = self.loadSelected(self.searchedList, lboxWg)
        tmpLang = self.db[selectFile]['lang']
        tmpSize = self.db[selectFile]['size']
        tmpPage = self.db[selectFile]['page']
        tmpCTime = self.db[selectFile]['ctime']
        tmpCmt = self.cmtVar.get()
        dbCursor = dbFav.execute('select * from favorite where title="%s"' % selectFile)
        checkData = dbCursor.fetchall()
        if len(checkData) != 0:
            dbFav.execute('update favorite \
                           set comment = "%s" \
                           where title = "%s"' % (self.cmtVar.get(), selectFile))
        else:
            dbFav.execute('insert into favorite (title, language, size, page, createtime, comment) \
                          values ("%s", "%s", %s, %s, "%s", "%s")' % (selectFile, tmpLang, tmpSize, tmpPage, tmpCTime, tmpCmt))
        dbFav.commit()
        dbFav.close()

        # Should I add reload fav db?
        self.fav = self.tool.readDB(self.pathVar.get() + self.favDB, self.tool.favTableName)

    def removeFromFavorite(self):
        '''
        Function to remove an entry from the list of favorite.
        Should remove from the stored file as well.
        :return:
        '''
        dbFav = sqlite3.connect(self.pathVar.get() + self.favDB)

        selectFile = self.loadSelected(self.searchedList, self.selection)
        dbCursor = dbFav.execute('select * from favorite where title="%s"' % selectFile)
        checkData = dbCursor.fetchall()
        if len(checkData) != 0:
            dbFav.execute('delete from favorite where title= "%s"' % selectFile)
            return 0
        else: # Not likely to happen since we select from fav list but just in case.
            self.popupWarning(title = 'Errrrr!', text = 'Entry is not added to Fav yet')
            return 1

    def createDB(self):
        # function to trigger generating database.
        if messagebox.askokcancel("Verify", "Are you sure?"):
            self.__threadCall(self.popupPB, self.tool.getTotalZip(self.pathVar.get()), 'db')
            self.tool.createMainDatabase(self.pathVar.get(), self.mainDB)
            # self.__threadCall(self.tool.createDatabase, self.pathVar.get(), self.dbName)

            # Load DB
            self.__loadDB()

    def downloadNewEntry(self, textWg):
        # textWg.delete('1.0', END)
        try:
            dataOutput = subprocess.Popen('gallery-dl "%s"' % self.linkVar.get(),
                                          stdout = subprocess.PIPE, universal_newlines = True)
            for line in dataOutput.stdout:
                textWg.insert(END, line)
                textWg.see(END)
        except:
            print("Something's wrong with cmd call")

    def popupWarning(self, title = None, text = None):
        title = 'Sorry !' if title is None else title
        text  = 'Not implemented yet. Contact NoVaci ASAP!!' if text is None else text

        self.win = Toplevel()
        self.win.title(title)
        sorLabel = Label(self.win, text = text, height = 5, width = 50)
        sorLabel.pack()

    def popupPB(self, *args):
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

    def popupDownload(self):
        self.downWin = Toplevel()
        self.downWin.title('Download New')
        self.downWin.config(width = 300)
        self.linkVar = StringVar()
        idLabel = Label(self.downWin, text = 'Gallery URL:')
        idEntry = Entry(self.downWin, textvariable = self.linkVar, width = 50)
        idLabel.grid(column = 0, row = 0, sticky = 'nsew')
        idEntry.grid(column = 1, row = 0, sticky = 'nsew')

        btnDL = Button(self.downWin, text = 'Start', command = lambda : self.__threadCall(self.downloadNewEntry, self.textGalleryProcess))
        btnDL.grid(column = 0, row = 1, sticky = 'nsew')

        self.textGalleryProcess = Text(self.downWin)
        self.textGalleryProcess.grid(column = 0, row = 2, columnspan = 2, sticky = 'nsew')

    def popupAddComment(self):
        '''
        Show a small window after clicking AddFav to add the note for the current entry.
        :return: None
        '''
        self.noteWin = Toplevel()
        self.noteWin.title('Comment')
        cmtEntry = Entry(self.noteWin, textvariable = self.cmtVar, width = 50)
        # cmtEntry.focus_set()
        cmtEntry.selection_range(0, END)

        btnDone   = Button(self.noteWin, text = 'Finish', command = self._saveAndDestroy)
        btnCancel = Button(self.noteWin, text = 'Cancel', command = self.noteWin.destroy)

        cmtEntry.grid(column = 0, row = 0, columnspan = 2, sticky = 'nsew')
        btnDone.grid(column = 0, row = 1, padx = 10)
        btnCancel.grid(column = 1, row = 1, padx = 10)

    def _saveAndDestroy(self):
        '''
        A combine function to save to fav db then close the window
        :return: 0 for success, 1 for failure
        '''
        self.saveToFavourite(self.selection)
        self.noteWin.destroy()

    def _delSelected(self):
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
