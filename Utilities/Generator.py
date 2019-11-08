import pandas as pd
import re

class Generator(object):
    def __init__(self):
        self.content = ''
        # with open('Template.json') as file:
        #     self.template_line = json.load(file)
        # self.data = pd.read_csv('template.csv')
        self.HEADINGS = ['System', 'Test Description', 'Expected Outcome', 'Test Suite', 'Action', 'Test Type', 'Comment',
                         'Jenkins', 'SVN Script', 'Screenshot', 'Result']
        self.dataframe = []

    def _read_excel(self):
        self.data = pd.read_excel('template.xlsx')

    def generate_testing_analysis_format(self):
        self._read_excel()
        for index, row in self.data.iterrows():
            jenkins_link = ('[Jenkins|{0}]'.format(self.data['Jenkins'][index])) if self.data['Jenkins'][index] != 'nope' else ''
            svn_link = '[SVN Script|{0}]'.format(self.data['SVN Script'][index]) if self.data['SVN Script'][index] != 'nope' else ''
            screenshot_link = '[Screenshot|{0}]'.format(self.data['Screenshot'][index]) if self.data['Screenshot'][index] != 'nope' else ''
            result_link = '[Result|{0}]'.format(self.data['Result'][index]) if self.data['Result'][index] != 'nope' else ''
            comment = self.data['Comment'][index] if self.data['Comment'][index] != 'nope' else ''
            comment_final = '(/) ' + comment + ' ' + jenkins_link + ' ' + svn_link + ' ' + screenshot_link + ' ' + result_link

            self.content += '|{0}|{1}|{2}|{3}|{4}|{5}|{6}|\n'.format(self.data['System'][index],
                                                                      self.data['Test Description'][index],
                                                                      self.data['Expected Outcome'][index],
                                                                      self.data['Test Suite'][index],
                                                                      self.data['Action'][index],
                                                                      self.data['Test Type'][index],
                                                                      comment_final)
        with open('test.txt', 'w') as f:
            f.write(self.content)

    def _extract_link(self, item, prefix):
        match = re.search(r"(?<={}\|)http:\S+(?=\])".format(prefix), item)
        return match.group(0) if match is not None else 'nope'

    def _convert_to_dataframe(self, headers, data):
        df = {}
        _ = 0
        for row in data:
            df.update({headers[_]: row})
            _ += 1
        return pd.DataFrame(df)

    def convert_raw_text_to_excel(self):
        dataframe = []
        with open('raw.txt', 'r') as file_read:
            self.content = file_read.readlines()

        for line in self.content:
            script_link = self._extract_link(line, 'SVN Script')
            screenshot_link = self._extract_link(line, 'Screenshot')
            result_link = self._extract_link(line, 'Result')
            jenkin_link = self._extract_link(line, 'Jenkins')
            all_links = [jenkin_link, script_link, screenshot_link, result_link]
            first_part = line.split('(/)')[0]
            texts = first_part.split('|')
            for _ in range(texts.count('')):
                texts.remove('')
            texts.append('(/)')
            all_data = texts + all_links
            dataframe.append(all_data)

        # data = self._convert_to_dataframe(self.HEADINGS, dataframe)
        data = pd.DataFrame(dataframe, columns= self.HEADINGS)
        writer = pd.ExcelWriter('template.xlsx', engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Table', index = False)
        writer.save()

test = Generator()
# => used when updating an existing table
# test.convert_raw_text_to_excel()

# => Use when first updating a new ticket
test.generate_testing_analysis_format()