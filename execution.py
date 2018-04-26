try:
    from GUI.Tools import Tool
except ImportError:
    raise ImportError('Lacking tool class')

if __name__ == '__main__':
    tool = Tool.Tool()
    #TODO: implement replace file name for new folder only

    # Compress hentai folder to zip
    # dirPath = (u"H:/Doujin-Manga/")
    dirPath = (u"I:/H-Colle/")
    dbName  = 'test.db'
    # tool.listCompressed(dirPath)
    # tool.compressSeparateFolder(dirPath)

    # dirPath  = ("I:/MyComic_SecondSection/")
    # destPath = ("H:/Doujin-Manga/")
    # tool.unRar(dirPath, destPath)
    # pattern = re.compile("[A-Z]{1}[0-9]+")
    # for archive in os.listdir(dirPath):
    #     tool.replaceFileInZip(dirPath + archive, pattern)

    # tool.getCommonPattern(dirPath)

    # tool.listEverything(dirPath)
    # tool.createDatabase(dirPath, dbPath)
    # dB = tool.readDB(dirPath + dbName)
    # tool.removeFolder(dirPath)
    # length = tool.getExcludedFile(dirPath)
    # length = tool.getTotalPDF(dirPath)
    # length = tool.getExcludedFile(dirPath)
    # length = tool.getTotalFolder(dirPath)
    # tool.replaceFile(dirPath)
    tool.fillMissing(dirPath, dbName)
