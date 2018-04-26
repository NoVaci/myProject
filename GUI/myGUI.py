from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
try:
    from Tools.Tool import Tool
    from Tools.ProgressBar import ProgressBar
except ImportError:
    from Tool import *
    from ProgressBar import  *
import threading
import subprocess
from time import sleep
import time
import sqlite3
import zipfile
import random
import re

#TODO: 6/14/2017: add remove fav entry.
#TODO: 6/30/2017: check for existing entry in fav
class myGUI():
    def __init__(self, parent):
        self.parent = parent
        parent.title('My test GUI')

        self.tool = Tool()
        self.dirPath = (u"I:\H-Colle\\")
        self.PATHLIST = [
            u"I:\H-Colle\\",
            u"H:\Doujin-Manga\\",
            u"H:\Doujin-Manga\\test\\"
        ]
        self.HISTORY = ['History']

        self.pathVar = StringVar()
        self.nameVar = StringVar()
        self.threads = []

        self.curPath = ''

        self.mainDB  = 'test.db'

        self.debug = False

        if not self.debug:
            self.db      = self.tool.readDB(self.dirPath + self.mainDB, self.tool.mainTableName)
            self.createSearchDict()
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
        self.fav   = StringVar()
        self.cutTitle= StringVar()

        self.barVar  = StringVar()
        self.cmtVar  = StringVar()
        self.tagVar  = StringVar()
        self.titleVar = StringVar()

        # List stores thumbnail images.
        self.arrImg   = []

        # Offset for navigating search index
        self.offSet   = 0

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

        self.histList = OptionMenu(frameInput, self.nameVar, *self.HISTORY)
        self.histList.grid(column = 0, row = 3, sticky = NW, pady = 1)

        nameSearch = Entry(frameInput, textvariable = self.nameVar, width = 30)
        nameSearch.grid(column = 0, row = 2, columnspan = 3, sticky = NW)
        nameSearch.focus_set()
        nameSearch.bind("<Return>", lambda event: self.searchAndShow(self.nameVar.get(), self.selection))

        '''Detail Info show
           Title: <name>
           Language: <Eng/Jap>
           Size:'''
        # headerText = 'First Entry ' + ('-' * 45)
        # Label(frameInput, text = headerText, fg = 'blue').grid(column = 0, row = 3, pady = 20, sticky = W, columnspan = 2)
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

        Label(frameInput, text = 'Favorite?:').grid(column = 0, row = 12, sticky = W)
        Label(frameInput, textvariable = self.fav).grid(column = 1, row = 12, sticky = W)

        # ----------------------------------------------------
        # Right: output screen
        # Consist of
        # ----------------------------------------------------

        frameOutput = Frame(parent)
        frameOutput.grid(column = 1, row = 0, rowspan = 2, sticky = E)

        Button(frameOutput, text = 'ThumbNail', command = self.loadThumbNail).grid(column = 0, row = 2, sticky = N)

        self.lblThumb1 = Label(frameOutput)
        self.lblThumb1.grid(column = 0, row = 3, sticky = W)
        self.lblThumb2 = Label(frameOutput)
        self.lblThumb2.grid(column = 1, row = 3, sticky = W)
        self.lblThumb3 = Label(frameOutput)
        self.lblThumb3.grid(column = 2, row = 3, sticky = W)
        self.lblThumb4 = Label(frameOutput)
        self.lblThumb4.grid(column = 3, row = 3, sticky = W)

        scroll = Scrollbar(frameOutput, orient = VERTICAL)
        # canvasContainer.configure(yscrollcommand = scroll.set)
        # canvasContainer.create_window((40,160), window = frameOutput, anchor = NW)
        # frameOutput.bind("<Configure>", self.onFrameConfigure)

        # Placement
        # canvasContainer.grid(column = 1, row = 0, rowspan = 2)
        # scroll.pack(side = RIGHT, fill = Y)
        scroll.grid(column = 4, row = 0, rowspan = 2, sticky = N+S)
        self.selection = Listbox(frameOutput, height = 30, width = 160, exportselection = 0, yscrollcommand = scroll.set)
        self.selection.bind("<Double-Button-1>", self.__onDoubleClick)
        self.selection.grid(column = 0, row = 0, columnspan = 4, sticky = W)
        # self.selection.pack(side = LEFT, fill = Y)
        scroll.config(command = self.selection.yview, orient = VERTICAL)

        # Paging button
        Button(frameOutput, text = '>', width = 3, command = lambda: self.loadNextPage('forward'))\
                    .grid(column = 1, row = 1, padx = 1, sticky = W)
        Button(frameOutput, text = '<', width = 3, command = lambda: self.loadNextPage('backward'))\
                    .grid(column = 0, row = 1, padx = 1, sticky = E)
        # Section for pop up menu
        self.popMenu = Menu(parent, tearoff = 0)
        self.popMenu.add_command(label = 'Add Fav', command = self.saveToFavourite)
        self.popMenu.add_command(label = 'Remove Fav', command = self.removeFromFavorite)
        self.popMenu.add_command(label = 'Add info', command = self.popupAddInfo)

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

        btnDownload = Button(frameBtn, text = 'Download', command = self.popupDownload)

        btnTransfer = Button(frameBtn, text = 'Transfer', command = self.popupTransfer)

        btnCreateDB = Button(frameBtn, text = 'Create DB',
                             command = lambda: self.__threadCall(self.createDB))

        btnLoadDB   = Button(frameBtn, text = 'Load DB', command = self.__loadDB)

        btnLoadFav  = Button(frameBtn, text = 'Load Fav', command = self.loadFavorite)

        btnLoadJap  = Button(frameBtn, text = 'Load Jap Only', command = self.loadJapEntries)

        btnDelete   = Button(frameBtn, text = 'Remove', command = self._delSelected)

        btnLatest = Button(frameBtn, text = 'Latest Entries', command = lambda: self.__threadCall(self.loadLatest))

        btnReadLater = Button(frameBtn, text = 'Read Later', command = lambda : self.__threadCall(self.loadReadLater))
        
        btnSurprise = Button(frameBtn, text = 'Surprise Me', command = lambda : self.__threadCall(self.loadSurprise))
        if self.debug:
            btnDebug    = Button(frameBtn, text = 'Test update time',
                                 command = self.updateTime)
            btnDebug.grid(column = 1, row = 3, sticky = 'nsew')
        # btnCompZip.pack(side = TOP, padx = 10)
        btnCompZip.grid(column = 0, row = 0, sticky = W)
        btnDownload.grid(column = 1, row = 0, sticky = W)
        btnCreateDB.grid(column = 0, row = 1, sticky = W)
        btnLoadDB.grid(column = 1, row = 1, sticky = W)
        btnTransfer.grid(column = 2, row = 1, sticky = W)
        btnLoadFav.grid(column = 0, row = 2, sticky = W)
        btnLoadJap.grid(column = 1, row = 2, sticky = W)
        btnLatest.grid(column = 0, row = 3, sticky = W, pady = 5)
        btnReadLater.grid(column = 1, row = 3, sticky = W, padx = 5)
        btnSurprise.grid(column = 2, row = 3, sticky = W)
        btnDelete.grid(column = 0, row = 4, sticky = W)
        # btnTest.grid(column = 0, row = 1, sticky = W)

    def __getCurrentEntry(self):
        # Return the file path of current selected entry
        ext = '.pdf' if self.page.get() == '0' else '.zip'
        path = self.pathVar.get() + self.title.get() + ext
        path.replace('\\', r'\\')
        return path

    def __threadCall(self, sFunc, *args, bWaitFinish = False):
        qThread = threading.Thread(target = sFunc, args = args)
        self.threads.append(qThread)
        qThread.start()
        if bWaitFinish:
            qThread.join()

    def __onDoubleClick(self, event):
        # Double click to load search result to listbox
        widget = event.widget
        value  = self.loadSelected(self.searchedList, widget)
        self.loadEntry(value)

        if self.debug:
            print(value)

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

        self.createSearchDict()

    def detectPathChange(self):
        # Function to load DB when detecting a change in path folder
        sleep(1)
        while(self.curPath != self.pathVar.get()):
            self.__loadDB()
            self.curPath = self.pathVar.get()

    def zipFolder(self, textField):
        self.__threadCall(self.popupPB, self.tool.getTotalFolder(self.pathVar.get()))
        self.tool.compressSeparateFolder(self.pathVar.get(), textField)

    def createSearchDict(self):
        '''
        Create an all lower case list for searching
        :return: list of all lower case
        '''
        self.lowerDict = {}
        for name in self.db.keys():
            self.lowerDict.update({name.lower(): name})
        return self.lowerDict

    def updateHistoryList(self):
        '''
        Update the history Option menu with new item from self.HISTORY
        :return: None
        '''
        menu = self.histList['menu']
        menu.delete(0, END)
        for item in self.HISTORY:
            menu.add_command(label = item, command = lambda value = item: self.nameVar.set(value))

    def searchAndShow(self, string, lboxWg, tags = ''):
        # Function to search for an input in database and show result on a list
        lstRst = []
        if string == '':
            self.loadAll(lboxWg)
        else:
            if '*' in string:
                string = string.replace('*', '.*')
                try:
                    regExp = re.compile(string)
                    lstRst = list(self.lowerDict[name] for name in self.lowerDict if regExp.match(name))
                except IndexError:
                    print("Require at least 2 words for reg search")
            else:
                lstRst = list(self.lowerDict[name] for name in self.lowerDict if string in name)

        if len(lstRst) > 0:
            firstEntry = lstRst[0]
            self.searchedList = lstRst

            # Add searched (and found results) entry to history list
            if string not in self.HISTORY:
                self.HISTORY.insert(0, string)
                if len(self.HISTORY) == 10:
                    del self.HISTORY[-1]
                self.updateHistoryList()
        else:
            firstEntry = 'Not Found'

        self.loadResult(lstRst, lboxWg)
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
            self.fav.set('')
        else:
            self.lang.set(self.db[input]['lang'])
            self.size.set(self.db[input]['size'])
            self.page.set(self.db[input]['page'])
            self.ctime.set(time.ctime(float(self.db[input]['ctime'])))
            self.visit.set(self.db[input]['visit'])
            self.tags.set(self.db[input]['tags'])
            self.cmt.set(self.db[input]['cmt'])

            if self.debug:
                print("\nTime value: %s - type: %s" % (self.db[input]['ctime'], type(self.db[input]['fav'])))

            if self.db[input]['fav'] == 1:
                self.fav.set('Epic')
            else:
                self.fav.set('Normal')

    def loadAll(self, lboxWg):
        # Function to load all title and show in listbox
        lstAll = list(self.db.keys())
        lstAll.sort()
        self.searchedList = lstAll
        self.loadResult(lstAll, lboxWg)

    def loadResult(self, lstSearch, lboxWg, sort = True):
        # Function to load the list of search result to listbox
        if sort:
            lstSearch.sort()
        lboxWg.delete(0, END)

        for title in lstSearch:
            lboxWg.insert(END, title)

    def loadSelected(self, lst, lboxWg):
        return lst[self.whichSelected(lboxWg)]

    def loadThumbNail(self):
        '''
        Function to load a few images of a zip folder.
        :return:
        '''
        zipType = '.pdf' if self.page.get() == '0' else '.zip'
        if zipType == '.zip':
            pathToFile = self.pathVar.get() + self.title.get() + zipType
            index = 0 # Set the index of image
            count = 0
            self.arrImg = [] # Reset the list of previous load
            with zipfile.ZipFile(pathToFile, 'r') as zipRead:
                for item in zipRead.infolist():
                    if index % 3 == 0:
                        index += 1
                        imgZip = Image.open(zipRead.open(item))
                        imgZip = imgZip.resize((250, 300), Image.ANTIALIAS)

                        self.img = ImageTk.PhotoImage(imgZip)
                        self.arrImg.append(self.img)
                        count += 1

                        if count == 4:
                            break
                    else:
                        index += 1

            self.lblThumb1.config(width = self.arrImg[0].width(), image = self.arrImg[0])
            self.lblThumb2.config(width = self.arrImg[1].width(), image = self.arrImg[1])
            self.lblThumb3.config(width = self.arrImg[2].width(), image = self.arrImg[2])
            self.lblThumb4.config(width = self.arrImg[3].width(), image = self.arrImg[3])

    def loadReadLater(self):
        '''
        Function to load favorite added entries without any view
        :return:
        '''
        viewLater = sqlite3.connect(self.pathVar.get() + self.mainDB)
        rlLIst    = viewLater.execute('select * from favorite,hentai where \
                                      (favorite.title=hentai.title and hentai.visit=0)').fetchall()
        self.searchedList = self.tool.convertTupToList(rlLIst)
        self.loadResult(self.searchedList, self.selection)
        viewLater.close()

    def loadComic(self):
        # Function to open up CDisplayex and load the current selected entry
        # For manual test:
        # subprocess.call('C:\\Program Files\\CDisplayEx\\CDisplayEx.exe "H:\\Doujin-Manga\\<>.zip"'
        visitCount = self.db[self.title.get()]['visit']
        visitCount += 1
        # Update to the current view
        self.db[self.title.get()]['visit'] = visitCount
        # Update to the main database
        self.tool.updateDatabase(self.pathVar.get() + self.mainDB, self.title.get(), visitCount, column = 'visit')
        tail = '.pdf' if self.page.get() == '0' else '.zip'
        pathToFile = self.pathVar.get() + self.title.get() + tail
        pathToFile.replace('\\', r'\\')
        subprocess.call('C:\\Program Files\\CDisplayEx\\CDisplayEx.exe "%s"' % pathToFile)

    def loadFavorite(self):
        viewFav   = sqlite3.connect(self.pathVar.get() + self.mainDB)
        favList   = viewFav.execute('select * from favorite').fetchall()
        self.searchedList = self.tool.convertTupToList(favList)
        self.loadResult(self.searchedList, self.selection)
        viewFav.close()

    def loadLatest(self):
        """
        Load most recent added entries. Default is 50.
        :return:
        """
        dbConn = sqlite3.connect(self.pathVar.get() + self.mainDB)
        latestList = dbConn.execute('select title from hentai \
                                    order by createtime DESC \
                                     limit 100').fetchall()
        self.offSet += 100
        self.searchedList = self.tool.convertTupToList(latestList)
        self.loadResult(self.searchedList, self.selection, sort = False)
        dbConn.close()

    def loadJapEntries(self):
        '''
        Show only the
        :return:
        '''
        dbConn = sqlite3.connect(self.pathVar.get() + self.mainDB)
        latestList = dbConn.execute('select title from hentai \
                                            where language="Jap"').fetchall()
        self.searchedList = self.tool.convertTupToList(latestList)
        self.loadResult(self.searchedList, self.selection, sort = False)
        dbConn.close()

    def loadSurprise(self):
        '''
        Load random entries which visit = 0. List of 50.
        :return:
        '''
        viewRand = sqlite3.connect(self.pathVar.get() + self.mainDB)
        randList = viewRand.execute('select * from hentai where visit=0').fetchall()

        self.searchedList = [] # Clear the list
        # list to store random entries
        tmpArr = self.tool.convertTupToList(randList)
        for count in range(0,50):
            index = random.randint(0, len(tmpArr))
            self.searchedList.append(tmpArr[index])
        
        self.loadResult(self.searchedList, self.selection)
        viewRand.close()

    def loadNextPage(self, navVector, number = 100):
        '''
        Load next <number> items in the list if invoked
        :param number: default is 100 items
        :param navVector: forward or backward
        :return: None
        '''

        if navVector == 'backward' and self.offSet <= 0:
            pass
        else:
            dbConn = sqlite3.connect(self.pathVar.get() + self.mainDB)
            if navVector == 'forward':
                latestList = dbConn.execute('select title from hentai \
                                            order by createtime DESC \
                                             limit %s offset %s' % (number, self.offSet)).fetchall()
                self.offSet += number

            else:
                self.offSet -= number * 2
                latestList = dbConn.execute('select title from hentai \
                                            order by createtime DESC \
                                             limit %s offset %s' % (number, self.offSet)).fetchall()

            self.searchedList = self.tool.convertTupToList(latestList)
            self.loadResult(self.searchedList, self.selection, sort = False)
            dbConn.close()
        
    def saveToFavourite(self):
        '''
        Function to save current selected entry to favourite list.
        :param lboxWg: list where result is shown.
        :return: None
        '''
        dbFav = sqlite3.connect(self.pathVar.get() + self.mainDB)

        selectFile = self.loadSelected(self.searchedList, self.selection)
        dbCursor = dbFav.execute('select * from favorite where title="%s"' % selectFile)
        checkData = dbCursor.fetchall()
        if len(checkData) == 0:
            dbFav.execute('update hentai \
                           set fav = 1 where title = "%s"' % selectFile)
            dbFav.commit()

            # Update to current loaded db
            self.db[selectFile]['fav'] = 1
        else:
            # Popup warning
            self.popupWarning('Errrror!','Already added')
            print('Added - %s' %selectFile)

        dbFav.close()

    def removeFromFavorite(self):
        '''
        Function to remove an entry from the list of favorite.
        Should remove from the stored file as well.
        :return:
        '''
        dbFav = sqlite3.connect(self.pathVar.get() + self.mainDB)

        selectFile = self.loadSelected(self.searchedList, self.selection)
        try:
            dbFav.execute('update hentai set fav = 0 where title="%s"' % selectFile)
            dbFav.commit()
            self.db[selectFile]['fav'] = 0
        except:
            self.popupWarning(title = 'Errrrr!', text = 'Entry is not added to Fav yet')
        dbFav.close()

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

    def transferDB(self, dbPathA, dbPathB):
        '''
        Function to transfer data from one db to another
        :param dbPathA: path to original db is located
        :param dbPathB: path to target db
        :return:
        '''
        dbA = sqlite3.connect(dbPathA + self.mainDB)
        dbB = sqlite3.connect(dbPathB + self.mainDB)

        cursor = dbA.execute('select * from hentai')
        dbAEntries = cursor.fetchall()
        for i in range(len(dbAEntries)):
            checkExist = dbB.execute('select title from hentai where title = "%s"' % dbAEntries[i][0]).fetchall()
            if len(checkExist) == 0:
                print('Transfering %s' % dbAEntries[i][0])
                dbB.execute('insert into hentai(title, language, size, page, createtime, comment, visit, tags, fav) \
                            values ("{0}","{1}",{2},{3},"{4}","{5}",{6},"{7}",{8})'.format(*dbAEntries[i]))
                self.transferFile(dbAEntries[i][0], dbPathA, dbPathB)
                dbA.execute('delete from hentai where title = "%s" ' % (dbAEntries[i][0]))
                dbB.commit()
                dbA.commit()
                print('Transfer complete!')
            else:
                print(dbAEntries[i][0] + '\n')  # Flush to a list so we can manually decide what to do next?
        
        dbA.close()
        dbB.close()

    def transferFile(self, file, dirA, dirB):
        """
        Move file from A - > B
        :param file: filename
        :param dirA: path to dir A
        :param dirB: path to dir B
        :return:
        """
        self.tool.moveIfExist(dirA + file + '.zip', dirB)

    def popupTransfer(self):
        '''
        Create a window for choosing which db path to be used
        :return:
        '''
        self.transWin = Toplevel()
        self.transWin.title = 'Transfer data'
        self.transWin.geometry("300x200")
        pathA = StringVar()
        pathB = StringVar()
        pathAList = [u"H:\Doujin-Manga\\",
                     u"H:\Doujin-Manga\\test\\"]
        pathBList = [u"I:\H-Colle\\",
                      u"H:\Doujin-Manga\\",]
        pathA.set(pathAList[0])
        pathB.set(pathBList[0])

        dbA = OptionMenu(self.transWin, pathA, *pathAList)
        dbB = OptionMenu(self.transWin, pathB, *pathBList)

        dbA.pack(padx = 10, pady = 5)
        dbB.pack(padx = 10, pady = 5)

        btnStart = Button(self.transWin, text = 'Start', command = lambda: self.__threadCall(self.transferDB, pathA.get(), pathB.get()))
        btnStart.pack(pady = 3, side = BOTTOM)

    def popupWarning(self, title = None, text = None, bDestroy = False):
        title = 'Sorry !' if title is None else title
        text  = 'Not implemented yet. Contact NoVaci ASAP!!' if text is None else text

        self.win = Toplevel()
        self.win.title(title)
        sorLabel = Label(self.win, text = text, height = 5, width = 50)
        sorLabel.pack()

        if bDestroy:    # does not seem to work yet
            sleep(5)
            self.win.destroy()

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

    def popupAddInfo(self):
        '''
        Show a small window after clicking AddFav to add the note for the current entry.
        :return: None
        '''
        self.noteWin = Toplevel()
        self.noteWin.title('Comment & Tags')
        self.cmtVar.set('') # Clear old data
        self.tagVar.set('') # Clear old data
        cmtEntry = Entry(self.noteWin, textvariable = self.cmtVar, width = 100)
        tagEntry = Entry(self.noteWin, textvariable = self.tagVar, width = 50)
        self.titleVar.set(self.title.get())
        titleEntry = Entry(self.noteWin, textvariable = self.titleVar)
        # cmtEntry.focus_set()
        cmtEntry.selection_range(0, END)

        selectFile = self.loadSelected(self.searchedList, self.selection)
        btnDone   = Button(self.noteWin, text = 'Finish', command = lambda : self._saveAndDestroy(selectFile,
                                                                                                  self.cmtVar.get(),
                                                                                                  self.tagVar.get(),
                                                                                                  self.titleVar.get()))
        btnCancel = Button(self.noteWin, text = 'Cancel', command = self.noteWin.destroy)

        Label(self.noteWin, text = 'Comment').grid(column = 0, row = 0, sticky = 'nsew')
        Label(self.noteWin, text = 'Tag').grid(column = 0, row = 1, sticky = 'nsew')
        Label(self.noteWin, text = 'Title').grid(column = 0, row = 2, sticky = 'nsew')
        cmtEntry.grid(column = 1, row = 0, columnspan = 2, sticky = 'nsew')
        tagEntry.grid(column = 1, row = 1, columnspan = 2, sticky = 'nsew')
        titleEntry.grid(column = 1, row = 2, columnspan = 2, sticky = 'nsew')
        btnDone.grid(column = 0, row = 3, padx = 10)
        btnCancel.grid(column = 1, row = 3, padx = 10)


    def _saveAndDestroy(self, title = None, cmt = '', tag = '', tit = ''):
        '''
        A combine function to save to fav db then close the window
        :param title: must provide title if cmt or tag is not None
        :return: 0 for success, 1 for failure
        '''
        dbConn = sqlite3.connect(self.pathVar.get() + self.mainDB)
        if cmt != '':
            dbConn.execute('update hentai set comment = "%s" \
                           where title = "%s"' % (cmt, title))
            dbConn.commit()
            self.db[title]['cmt'] = cmt
        if tag != '':
            dbConn.execute('update hentai set tags = "%s" \
                           where title = "%s"' % (tag, title))
            dbConn.commit()
            self.db[title]['tags'] = tag

        if tit != '' and tit != title:
            dbConn.execute('update hentai set title = "%s" \
                           where title = "%s"' % (tit, title))
            ##TODO: add pdf option
            dbConn.commit()
            self.tool.renameFile(self.pathVar.get(), title + '.zip', tit + '.zip')
            self.db[tit] = self.db[title]

            del self.db[title]

        dbConn.close()
        sleep(0.5)
        self.noteWin.destroy()

    def _delSelected(self):
        if messagebox.askyesnocancel('Are you sure?', 'This will delete the file completely.'):
            self.tool.removeIfExist(self.__getCurrentEntry())
            # Remove from DB
            try:
                dbConn = sqlite3.connect(self.pathVar.get() + self.mainDB)
                ext = '.pdf' if self.page.get() == '0' else '.zip'
                file = self.title.get()
                dbConn.execute('delete from hentai where title="%s"' % file)
                dbConn.commit()
                dbConn.close()
                del self.db[self.title.get()]
                messagebox.showinfo('Complete', "DB needs to be re-created.")
            except KeyError:
                messagebox.showwarning('Warning', 'Entry %s not exist.' % self.title.get())

    def updateTime(self):
        """
        For one time use, update the datebae with time in seconds.
        :return:
        """
        self.tool.updateTime(self.pathVar.get(), self.mainDB, single = True, title = self.title.get())

if __name__ == '__main__':
    root = Tk()
    root.minsize(height = 300, width = 400)
    root.resizable(True, True)
    app = myGUI(root)
    app.initializeGUI(root)
    root.mainloop()
