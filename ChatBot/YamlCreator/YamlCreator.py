import codecs
import os


class YamlCreator(object):
    def __init__(self, fileName, lang = "vietnamese", category = "daily"):
        sRootPath = os.getcwd()
        sCorpusPath = "venv\\Lib\\site-packages\\chatterbot_corpus\\data"
        self.filePath = os.path.join(sRootPath, sCorpusPath, lang, fileName)
        if not os.path.exists(self.filePath):
            with open(self.filePath, "w") as fileWrite:
                dContent = {"categories": category,
                            "conversations": ""}
                sContent = "categories:\n" \
                           "- %s\n" \
                           "conversations:\n" \
                           "" % category
                # yaml.dump(dContent, fileWrite, default_flow_style = False)
                fileWrite.write(sContent)

    def appendYaml(self, content):
        """

        :param content:
        :return:
        """
        tmp = ""
        isFirstLine = True
        with codecs.open(self.filePath, "a", "utf-8") as fileWrite:
            for item in content:
                if isFirstLine:
                    tmp += "- - " + item + "\n"
                    isFirstLine = False
                else:
                    tmp += "  - " + item + "\n"

            fileWrite.write(tmp)


test = YamlCreator("test.yml")
