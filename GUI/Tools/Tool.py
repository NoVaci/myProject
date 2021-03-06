#-*- coding: utf-8 -*-
from zipfile import BadZipFile

try:
    import zipfile
    import os
    import shutil
    import tempfile
    import re
    import patoolib
    from pyunpack import Archive
    import time
    from tkinter import *
    import sqlite3

except ImportError:
    raise ImportError("Missing packages")

class Tool:
    def __init__(self):
        self.lIsCompressed     = []
        self.lReplace          = []

        self.Pattern           = {}

        self.mainTableName     = 'hentai'
        self.favTableName      = 'favorite'

        self.pDigit        = re.compile("[0-9]+")
        self.pOneLetter    = re.compile("[A-Z]{1}[0-9]+")
        self.pMoreLetter   = re.compile("[A-Z]{2,5}[0-9]+")
        self.pMatchAll     = re.compile("[A-Z0-9-._]+")

        self.curZip        = 0
        self.curDB         = 0

    def getTotalFolder(self, dirPath):
        numZip  = self.getTotalZip(dirPath)
        numPDF  = self.getTotalPDF(dirPath)
        numExcl = self.getExcludedFile(dirPath)
        return len(os.listdir(dirPath)) - (numZip + numPDF + numExcl)

    def getTotalZip(self, dirPath):
        filterList = list(filter(lambda x: '.zip' in x, os.listdir(dirPath)))
        return len(filterList)

    def getTotalPDF(self, dirPath):
        filterList = list(filter(lambda x: '.pdf' in x, os.listdir(dirPath)))
        return len(filterList)

    def getExcludedFile(self, dirPath):
        num = 0
        for ext in ['test', 'test.db', 'fav.db', 'Guro', 'main.db']:
            num += 1 if os.path.exists(dirPath + ext) else 0
        return num

    def getCurrentDB(self):
        return self.curDB

    def getCurrentZip(self):
        return self.curZip

    def isEnglish(self, string):
        # function to detect if a string is English or not
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    def createTable(self, dbPath):
        '''
        Create a table for storing H-title
        :param dbPath: path of db, check before creating
        :return: True, False
        '''
        if os.path.exists(dbPath):
            return True
        else:
            dbConn = sqlite3.connect(dbPath)
            dbConn.execute('''create table hentai
                    (title text primary key     not null,
                     language text,
                     size     real,
                     page     int,
                     createtime    text,
                     comment        text,
                     visit      int,
                     tags       text,
                     fav    int);''')
            dbConn.commit()
            dbConn.close()

            return True

    def createFavoriteView(self, dbPath, bDrop = False):
        '''
        Create a view for favorite entries
        :param dbPath: path of db, same path as main db.
        :param bDrop: flag to signal drop the current view and create anew
        :return:
        '''
        dbConn = sqlite3.connect(dbPath)
        if bDrop:
            dbConn.execute('drop view if exists favorite')
        try:
            dbConn.execute('select * from favorite')
        except sqlite3.OperationalError:
            dbConn.execute('create view favorite as \
                            select title            \
                            from hentai where fav=1 ')
            dbConn.commit()
            dbConn.close()
        return True

    def createMainDatabase(self, dirPath, dbName):
        '''
        Fuction to store the downloaded files to a db file for searching
        :param dirPath: dir to create db
        :param dbName: path to db file
        :return:
        '''
        self.removeIfExist(dirPath + dbName)
        self.curDB = 0
        if self.createTable(dirPath + dbName):
            dbConn = sqlite3.connect(dirPath + dbName)
        else:
            print("Something's wrong on db side. Can't create a db")

        tmpCmt = 'Not Added'
        tmpTag = 'Not Added'
        initFav = 0
        for file in os.listdir(dirPath):
            if 'test' not in file or 'fav' not in file:
                err, tmpAttr = self.getFileAttribute(dirPath, file)
                if err == 1 or err == -1:
                    continue
                try:
                    dbConn.execute('insert into %s (title, language, size, page, createtime, comment, visit, tags, fav) \
                                   values ("%s", "%s", %s, %s, "%s", "%s", %s, "%s", %s)'
                                   % (self.mainTableName, file[:-4], tmpAttr[0], tmpAttr[1], tmpAttr[2], tmpAttr[3],
                                      tmpCmt, tmpAttr[4], tmpTag, initFav))
                except sqlite3.IntegrityError:
                    print(file[:-4])
                    print('\n')

                dbConn.commit()
                self.curDB += 1
        dbConn.close()

    def updateDatabase(self, fullDBPath, *newEntry, column= None):
        '''
        function to update the database to avoid re-populate the whole database.
        :param dirPath: current path
        :param dbName: db name
        :return: 0 if success, 1 if already exist
        '''
        dbConn = sqlite3.connect(fullDBPath)
        cursor = dbConn.execute('select * from hentai where title = "%s"' % newEntry[0])
        data = cursor.fetchall()

        tmpCmt  = 'Not Added'
        tmpTag  = 'Not Added'
        initFav = 0
        if len(data) == 0:
            # New entry: path to dir, file name
            err, attrList = self.getFileAttribute(newEntry[0], newEntry[1])
            if err == 0:
                dbConn.execute('insert into hentai (title, language, size, page, createtime, comment, visit, tags, fav) \
                                values ("%s", "%s", %s, %s, "%s", "%s", %s, "%s", %s)' %
                               (newEntry[1][:-4], attrList[0], attrList[1], attrList[2], attrList[3],
                                tmpCmt, attrList[4], tmpTag, initFav))
                dbConn.commit()
            else:
                dbConn.close()
            return 0
        else:
            # Do update to the column specified
            # New entry: title name, value of column
            dbConn.execute('update hentai set %s = "%s" '
                           'where title="%s"' % (column, newEntry[1], newEntry[0]))
            dbConn.commit()
            dbConn.close()
            return 1

    def readDB(self, dbPath, tbName):
        # Function to read detail info inside DB file and put into a dictionary
        # return { title : { size: <> , lang: <>, pages: <> }
        dData = {}

        try:
            dbConn = sqlite3.connect(dbPath)
            readAll = dbConn.execute('select * from %s' % tbName)
            for entry in readAll:
                dData.update({entry[0] : {'lang': entry[1], 'size': entry[2], 'page': entry[3], 'ctime': entry[4],
                                          'cmt': entry[5], 'visit': entry[6], 'tags': entry[7], 'fav': entry[8]}})
        except FileNotFoundError:
            raise FileNotFoundError("File %s not found" % dbPath)
        except sqlite3.OperationalError:
            self.createFavoriteView(dbPath)

        return dData

    def getFileAttribute(self, dirPath, file):
        '''
        Function to get a zip,pdf file attribute: size, language, no. page...
        Attention: should only be used when initiating the database or adding anew..
        :param filePath: file name
        :return: list of attributes + error (0 for success, 1 for failure, -1 for not supported file)
        '''
        iError = 0
        tmpList = file.split('.')
        sLang = 'Eng'
        fSize = 0
        iPage = 0
        cTime = ''
        iVisit = 0

        if len(tmpList) > 1 and tmpList[len(tmpList) - 1] in ['zip', 'pdf']:
            fStat = os.stat(dirPath + file)
            fSize = fStat.st_size
            fSize = round((fSize / (1024 ** 2)), 2)
            # Get created time
            cTime = fStat.st_ctime

            if not self.isEnglish(file[:-4]):
                sLang = 'Jap'
            if tmpList[len(tmpList) - 1] == 'zip':
                try:
                    with zipfile.ZipFile(dirPath + '/' + file, 'r') as zipRead:
                        iPage = len(zipRead.infolist())
                except BadZipFile:
                    print(file)
                    iError = 1
            return iError, [sLang, fSize, iPage, cTime, iVisit]
        else:
            iError = -1
            return iError, []

    def compressSeparateFolder(self, dirPath, textWg):
        # Function to compress folder in a directory to separate .zip file.
        # Except: compressed files.
        self.listCompressed(dirPath)
        self.curZip = 0
        for folder in os.listdir(dirPath):

            if folder[-3:] in ['zip', '.py', 'rar', 'pdf', 'txt', '.db'] or folder in ['Guro', 'test']:
                continue
            else:
                if folder + '.zip' not in self.lIsCompressed:
                    zipName = zipfile.ZipFile('{0}.zip'.format(os.path.join(dirPath, folder)), 'w',
                                              zipfile.ZIP_DEFLATED)
                    for root, dirs, files in os.walk(dirPath + '/' + folder):
                        for file in files:
                            zipName.write(os.path.abspath(os.path.join(root, file)), arcname = file)
                    zipName.close()
                    textWg.insert(END, folder + ' ==> Done compressed. Total: %s\n' % str(self.curZip))
                    textWg.see(END)

                    self.curZip += 1

                    self.removeFolder(dirPath + '/' + folder)

    def listCompressed(self, dirPath):
        for folder in os.listdir(dirPath):
            if folder[-3:] == 'zip':
                self.lIsCompressed.append(folder)

    def listEverything(self, dirPath):
        # List all file in an archive
        for file in os.listdir(dirPath):
            if 'zip' in file:
                print('-- %s \n' % file)
                with zipfile.ZipFile(dirPath + file, 'r') as zipRead:
                    for item in zipRead.infolist():
                        print('->> %s' % item.filename)

    def unRar(self, dirPath, destPath):
        # Function to unrar .rar file.
        for folder in os.listdir(dirPath):
            if folder[-3:] == 'rar':
                Archive(dirPath + '/' + folder).extractall(destPath)
                print('Done unRAR %s' % folder)
                shutil.rmtree(dirPath + '/' + folder)

    def removeFolder(self, dirPath):
        # Function to remove already compressed folder to save space
        shutil.rmtree(dirPath, ignore_errors= True)

    def removeIfExist(self, filePath):
        # Function to check if a file existed, remove if Yes.
        if os.path.exists(filePath):
            os.remove(filePath)

    def renameFile(self, dirPath, oldName, newName):
        if os.path.exists(dirPath + oldName):
            os.rename(dirPath + oldName, dirPath + newName)

    def moveIfExist(self, filePath, dstDir):
        try:
            shutil.move(filePath, dstDir)
        except FileNotFoundError:
            print('Check file location')

    def getCommonPattern(self, dirPath):
        # Function to summarize general pattern of picture file
        self.Pattern = {'digit'     : 0,
                        'oneLetter' : 0,
                        'moreLetter': 0,
                        'matchAll'  : 0,
                        'UI'        : []}
        iCount = 100
        for file in os.listdir(dirPath):
            if iCount == 0:
                break
            if 'zip' in file:
                with zipfile.ZipFile(dirPath + file, 'r') as zipRead:
                    for item in zipRead.infolist():
                        if self.pDigit.match(item.filename):
                            self.Pattern['digit'] += 1
                            iCount -= 1
                            break
                        elif self.pOneLetter.match(item.filename):
                            self.Pattern['oneLetter'] += 1
                            iCount -= 1
                            break
                        elif self.pMoreLetter.match(item.filename):
                            self.Pattern['moreLetter'] += 1
                            iCount -= 1
                            break
                        elif self.pMatchAll.match(item.filename):
                            self.Pattern['matchAll'] += 1
                            iCount -= 1
                            break
                        else:
                            self.Pattern['UI'].append(item.filename)
                            iCount -= 1
                            break

        dPattern = self.Pattern
        return dPattern

    def checkContentofArchive(self, zipFolder, pattern):
        # Function to check the content of a zip archive if follow a defined pattern
        # Return True / False
        iMisMatch = 0 # If pattern not match, count until reach a define number, here we can decide not to continue
        iMatch    = 0

        with zipfile.ZipFile(zipFolder, 'r') as zipRead:
            for item in zipRead.infolist():
                if iMisMatch > 5:
                    return False
                if pattern.match(item.filename):
                    iMatch += 1
                    if iMatch > 5:
                        return True
                else:
                    iMisMatch += 1

        return True

    def checkContentofFolder(self, folder, pattern):
        # Function to check the content of a zip archive if follow a defined pattern
        # @param zipFolder: path to folder
        # @param pattern: string to compare
        # Return True if not match, need to be processed/ False
        iMisMatch = 0  # If pattern not match, count until reach a define number, here we can decide not to continue
        iMatch    = 0
        for item in folder:
            if iMisMatch > 5:
                return False
            if pattern not in item:
                iMatch += 1
                if iMatch > 5:
                    return True
            else:
                iMisMatch += 1

        return True

    def replaceFileInFolder(self, folderPath, pattern):
        # Function to replace a file in a folder
        lTemp   = folderPath.split('/')
        titleName = lTemp[len(lTemp) - 1]

        if self.checkContentofFolder(folderPath, pattern):
            for item in os.listdir(folderPath):
                newName = titleName + '_' + item.filename
                os.rename(item, newName)

    def replaceFileInZip(self, zipPath, pattern):
        # Function to replace a file in an archive
        lTemp   = zipPath.split('/')
        zipName = lTemp[len(lTemp) - 1]

        if 'zip' in zipName:
            if self.checkContentofArchive(zipPath, pattern):
                tmpDir  = tempfile.mkdtemp()
                tmpName = os.path.join(tmpDir, 'new.zip')

                with zipfile.ZipFile(zipPath, 'r') as zipRead:
                    with zipfile.ZipFile(tmpName, 'w') as zipWrite:
                        for item in zipRead.infolist():
                            newName = zipName + '_' + item.filename
                            zipWrite.writestr(newName, zipRead.read(item.filename))

                shutil.move(tmpName, zipPath)
        else:
            print('%s not compressed yet' % zipName)

    def replaceFile(self, dirPath):
        # General function to make change to a file (in folder or an archive)
        #TODO: incomplete.
        lTmp = dirPath.split('/')
        tmpFile = lTmp[len(lTmp) - 1]

        if 'zip' in tmpFile:
            self.replaceFileInZip(dirPath, '')
        else:
            self.replaceFileInFolder(dirPath,'')

    def updateTime(self, dirPath, dbName, single = True, title = ''):
        dbConn = sqlite3.connect(dirPath + dbName)
        if single:
            fStat = os.stat(dirPath + title + '.zip')
            coreTime = fStat.st_ctime
            dbConn.execute('update hentai set createtime="%s" \
                            where title = "%s"' % (coreTime, title))
            dbConn.commit()
        else:
            count  = 0
            for file in os.listdir(dirPath):
                if 'test' not in file or 'fav' not in file or 'Guro' not in file:
                    fStat = os.stat(dirPath + file)
                    coreTime = fStat.st_ctime
                    dbConn.execute('update hentai set createtime="%s" \
                                    where title = "%s"' %(coreTime, file[:-4]))
                    count += 1
                    print('Finished: %s\n' % count)

                    dbConn.commit()

        dbConn.close()

    def convertTupToList(self, list):
        '''
        Function to convert tuple element of a list to a simple list
        :param list: list contains tuple with len of 1. [(,),(,)]
        :return: list
        '''
        resList = []
        for i in range(len(list)):
            if type(list[i]) == tuple:
                resList.append(list[i][0])
        return resList

    def fillMissing(self, dirPath, dbName):
        '''
        Find unregistered entry and fill in the database
        '''
        # Get all entries from database
        dbEntries = sqlite3.connect(dirPath + dbName)
        lEntries    = dbEntries.execute('select * from hentai').fetchall()
        lEntries  = self.convertTupToList(lEntries)

        tmpCmt = 'Not Added'
        tmpTag = 'Not Added'
        initFav = 0
        count = 0   # debug
        for file in os.listdir(dirPath):
            if '.zip' in file and '.db' not in file:
                if file[:-4] not in lEntries:
                    err, tmpAttr = self.getFileAttribute(dirPath, file)
                    if err == 1 or err == -1:
                        print('Error - %s - Invalid zip' % file)
                        continue
                    try:
                        count += 1
                        print(file + ' - Total: ' + str(count))
                        dbEntries.execute('insert into %s (title, language, size, page, createtime, comment, visit, tags, fav) \
                                                       values ("%s", "%s", %s, %s, "%s", "%s", %s, "%s", %s)'
                                       % (self.mainTableName, file[:-4], tmpAttr[0], tmpAttr[1], tmpAttr[2], tmpAttr[3],
                                          tmpCmt, tmpAttr[4], tmpTag, initFav))
                    except sqlite3.IntegrityError:
                        print(file[:-4])
                        print('\n')

                    dbEntries.commit()

        dbEntries.close()


