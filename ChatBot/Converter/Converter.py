import codecs
import json
import re
import sys
from optparse import OptionParser

from ChatBot.Converter.EncodedValue import *
from ChatBot.YamlCreator.YamlCreator import YamlCreator


class Converter(object):

    def __init__(self):
        parser = OptionParser()
        parser.add_option("--yaml", dest = "filename")
        if len(sys.argv) < 2:
            raise RuntimeError("Not enough argument. Must provide yml output file")
        else:
            (arg, value) = parser.parse_args()

            self.yml = YamlCreator(arg.filename)
            # raise RuntimeWarning("Not supported argument")

    def isURL(self, text):
        """
        Return False if URL detected. Else True
        :param text: string to check
        :return: True/False
        """
        URL = ['www', 'http', 'https']
        for link in URL:
            if link in text:
                return False
        return True

    def isTextContained(self, dMsg):
        """
        If message does not contain text, return False
        :param dMsg:
        :return: True/False
        """
        if "content" not in dMsg:
            return False
        return True

    def isSpecialCharContain(self, text):
        pattern = re.compile(
            r"[^a-z0-9A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+")
        return True if len(pattern.findall(text)) else False

    def removeSpecialCharacter(self, text):
        lSpecial = ['ð', ]

    def convertEncodedToRealValue(self, file):
        """
        Read real value from encoded file and replace all in file
        :param file:
        :return:
        """
        with codecs.open(file, "r", "utf-8") as fileRead:
            source = fileRead.read()

        with codecs.open(file, "w", "utf-8") as fileWrite:
            for encode, value in dValue.items():
                try:
                    source = source.replace(encode, value)
                except UnicodeEncodeError:
                    print("Error at: %s - %s" % (encode, value))
            try:
                fileWrite.write(source)
            except UnicodeEncodeError:
                print(source)
            # else:
            #     print("All values are decoded")

    def convertToYamlCorpus(self, file):
        """
        Take json as input file and return a corpus format
        :param file:
        :return:
        """
        isNewContext = False

        with codecs.open(file, "r", "utf-8") as fileRead:
            data = json.load(fileRead)

        dUsers = {1: data['participants'][0]['name'],
                  2: data['participants'][1]['name']}
        msgLen = len(data['messages'])
        lMsg = data['messages']
        iRootTimeStamp = data['messages'][-1]['timestamp_ms']

        lContext = []
        counter = 0
        for dMessage in reversed(lMsg):
            counter += 1
            if dMessage['timestamp_ms'] - iRootTimeStamp >= (240 * 60 * 1000):
                isNewContext = True
                iRootTimeStamp = dMessage['timestamp_ms']
                self.yml.appendYaml(lContext)

                # Clear previous data
                lContext = []
                if self.isTextContained(dMessage):
                    try:
                        if self.isURL(dMessage['content']) and self.isSpecialCharContain(dMessage['content']):
                            lContext.append(dMessage['content'])
                    except KeyError:
                        print(dMessage)

            else:
                print("Processing at: ", counter)
                if self.isTextContained(dMessage):
                    try:
                        if self.isURL(dMessage['content']) and self.isSpecialCharContain(dMessage['content']):
                            lContext.append(dMessage['content'])
                    except KeyError:
                        print(dMessage)

        self.yml.appendYaml(lContext)


convert = Converter()
pathToFile = 'C:\\Users\\NoVaci\\PycharmProjects\\myProject\\ChatBot\\messages\\TNThienLy_a09e7d1151\\message.json'
# C:\Users\NoVaci\PycharmProjects\myProject\ChatBot\messages\TNThienLy_a09e7d1151\message.json
# 'C:\Users\NoVaci\PycharmProjects\myProject\ChatBot\messages\dongkhanhthukhoa_1254b63b87\message.json'
convert.convertEncodedToRealValue(pathToFile)
convert.convertToYamlCorpus(pathToFile)
