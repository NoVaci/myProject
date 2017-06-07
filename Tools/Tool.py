#-*- coding: utf-8 -*-
try:
    import zipfile
    import os
    import shutil
    import tempfile
    import re
    import patoolib
    from pyunpack import Archive
    from tkinter import *

except ImportError:
    raise ImportError("Missing packages")

class Tool:
    def __init__(self):
        print('General Tool class')
        self.lIsCompressed     = []
        self.lReplace          = []

        self.Pattern           = {}

        self.pDigit        = re.compile("[0-9]+")
        self.pOneLetter    = re.compile("[A-Z]{1}[0-9]+")
        self.pMoreLetter   = re.compile("[A-Z]{2,5}[0-9]+")
        self.pMatchAll     = re.compile("[A-Z0-9-._]+")

    def test(self, dirPath, textWg):
        for i in range(len(dirPath)):
            textWg.insert(END, dirPath[i] + '\n')
            textWg.see(END)

    def isEnglish(self, string):
        # function to detect if a string is English or not
        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    def createDatabase(self, dirPath):
        # Fuction to store the downloaded files to a single text file for searching
        dbName   = 'H_DB'

        self.removeIfExist(dirPath + dbName + '.txt')

        f = open(dirPath + '/' + dbName + '.txt', mode='w')
        for file in os.listdir(dirPath):
            # file = tmpFile.decode('UTF-8')
            if len(file.split('.')) > 1 and file.split('.')[1] in ['zip','pdf']:
                sLang = 'Eng'
                fSize = os.stat(dirPath + file).st_size
                fSize = round((fSize / (1024 ** 2)),2)
                with zipfile.ZipFile(dirPath + '/' + file, 'r') as zipRead:
                    # If not english, encode in utf-8 then write to file under binary format.
                    # Decode before reading to get the original form.
                    if not self.isEnglish(file[:-4]):
                        file  = file.encode('utf-8')
                        sLang = 'Jap'

                    # The database entry: <filename>,<language>,<number of pages>
                    f.write('%s,%s,%sMB,%s\n' % (file[:-4], sLang, fSize, len(zipRead.infolist())))

            # else:
            #     self.createDatabase(dirPath + '/' + file)

        f.close()

    def removeIfExist(self, filePath):
        # Function to check if a file existed, remove if Yes.
        if os._exists(filePath):
            os.remove(filePath)

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

    def compressSeparateFolder(self, dirPath, textWg):
        # Function to compress folder in a directory to separate .zip file.
        # Except: compressed files.
        count = 0
        for folder in os.listdir(dirPath):

            if folder[-3:] in ['zip','.py','rar','pdf','txt']:
                continue
            else:
                if folder + '.zip' not in self.lIsCompressed:
                    zipName = zipfile.ZipFile('{0}.zip'.format(os.path.join(dirPath, folder)), 'w', zipfile.ZIP_DEFLATED)
                    for root, dirs, files in os.walk(dirPath + '/' + folder):
                        for file in files:
                            zipName.write(os.path.abspath(os.path.join(root,file)), arcname=file)
                    zipName.close()
                    count += 1
                    print(folder + ' ==> Done compressed. Total: %s' % str(count))
                    textWg.insert(END, folder + ' ==> Done compressed. Total: %s\n' % str(count))
                    textWg.see(END)

                    self.removeFolder(dirPath + '/' + folder)

    def removeFolder(self, dirPath):
        # Function to remove already compressed folder to save space
        shutil.rmtree(dirPath, ignore_errors= True)

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
        lTmp = dirPath.split('/')
        tmpFile = lTmp[len(lTmp) - 1]

        if 'zip' in tmpFile:
            self.replaceFileInZip(dirPath, '')
        else:
            self.replaceFileInFolder(dirPath,'')