import os, re, sys, time

class Refactor(object):
    def __init__(self, path, file_path=None):
        self.lSections = {}
        self.result = []
        self.workdir = os.getcwd()
        self.content = None
        self.new_content = ''
        self.file_path = file_path
        self.dir_path = path

        self.blank_line_pattern = re.compile(r"[(^\s+)|(^#)]")
        self.unnamed_img_pattern = re.compile(r"(_SS)\_img")
        self.named_img_pattern = re.compile(r"(_SS)\_\d{1,3}")

    def _get_spaces_of_line(self, line):
        space_start = line.find('}')
        space_end = line.find('id') if 'id' in line else line.find('xpath')
        print('Space start: ', space_start)
        print('Space end: ', space_end)
        return space_start, space_end

    def _get_longest_space_length_of_section(self):
        max_len = 0
        for line, space_len in self.lSections.items():
            cur_start, cur_end = self._get_spaces_of_line(line)
            self.lSections[line] = cur_start + 1
            if cur_end > max_len:
                max_len = cur_end

        return max_len

    def _fill_in_spaces(self, space_max):
        for line, space_len in self.lSections.items():
            space_to_fill = space_max - space_len
            print('Space num {0} to fill with space_max {1}'.format(space_to_fill, space_max))
            line = re.sub(r"\s+([xpath|id])", " " * space_to_fill + "\\1", line)
            self.result.append(line)

    def calculate_space(self):
        self._fill_in_spaces(self._get_longest_space_length_of_section())

    def combined_steps(self, line):
        self.calculate_space()
        self.write_new_content()
        self.new_content += line
        self.write_to_orginal_file()
        self.lSections = {}
        self.result = []

    def read_file(self, read_all=False):
        # with open(self.file_path, encoding='cp1252') as fileread:
        with open(self.file_path) as fileread:
            if not read_all:
                self.content = fileread.readlines()
            else:
                self.content = fileread.read()

    def _combine_data_in_lines(self, lines):
        result = ''
        for item in lines:
            result += item
        return result

    def write_new_content(self):
        for line in self.result:
            self.new_content += line

    def write_to_orginal_file(self):
        if isinstance(self.new_content, list):
            self.new_content = self._combine_data_in_lines(self.new_content)
        # with open(os.path.join(self.file_path), "w", encoding='cp1252') as  filewrite:
        with open(os.path.join(self.file_path), "w") as  filewrite:
            filewrite.write(self.new_content)

    def parse_file(self):
        for line in self.content:
            if self.blank_line_pattern.match(line) is None:
                self.lSections.update({line: 0})
            else:
                # Start calculate spaces
                self.combined_steps(line)

        if self.lSections != {}:
            self.combined_steps('')

    def standardlized_replacement(self, text):
        if isinstance(text, str):
            return re.sub(self.named_img_pattern, r"\1_img", text)
        elif isinstance(text, list):
            for i in range(len(text)):
                text[i] = re.sub(self.named_img_pattern, r"\1_img", text[i])
            return text

    def name_img_in_screenshot(self, standardlize = True, lines = False):
        self.new_content = self.content
        if standardlize:
            self.new_content = self.standardlized_replacement(self.new_content)
        if not lines:
            for i in range(self.content.count('.png')):
                if len(str(i)) == 1:
                    sCounter = '0' + str(i)
                else:
                    sCounter = str(i)
                self.new_content = re.sub(self.unnamed_img_pattern, r"\1_" + sCounter, self.new_content, 1)

        else:
            sCounter = 0
            for i in range(len(self.new_content)):
                if re.findall(self.unnamed_img_pattern, self.new_content[i]):
                    if len(str(sCounter)) == 1:
                        sCounter = '0' + str(sCounter)
                    self.new_content[i] = re.sub(self.unnamed_img_pattern, r"\1_" + str(sCounter), self.new_content[i])
                    sCounter = int(sCounter) + 1

                if '[Tags]' in self.new_content[i]:
                    # reset the counter
                    sCounter = 0

    def space_refactor_directory(self, dir_name):
        for root, dirs, files in os.walk(os.path.join(self.dir_path, dir_name)):
            # for dir in dirs:
            for file in files:
                print(file)
                self.file_path = os.path.join(root, file)
                self.execute()
                self.new_content = ''

    def execute(self):
        self.read_file()
        self.parse_file()

    def rename_screenshot_png(self, dir_name):
        # Nhung
        # original_pattern = re.compile(r"(FUL_)(\d{2})(_SS\d{2}).+(.png)")
        original_pattern = re.compile(r"(DTR_)(\d{2})(_SS\d{2})(.png)")
        for root, dirs, files in os.walk(os.path.join(self.dir_path, dir_name)):
            for file in files:
                time.sleep(0.2)
                print(file)
                self.file_path = os.path.join(root, file)
                # new_name = re.sub(r"(_)(CL_\d\.\d\.\d{1,2})(_SS_\d{2})", r"\1Confirmation_Letter\3_\2", file)
                new_name = re.sub(original_pattern, r"SP0030_\1PSV_\2\3\4", file)
                print("Changed to: " + new_name)
                new_file_path = os.path.join(root, new_name)
                os.rename(self.file_path, new_file_path)

    def replace_url_link(self, dir_name):
        for root, dirs, files in os.walk(os.path.join(self.dir_path, dir_name)):
            # for dir in dirs:
            for file in files:
                time.sleep(0.2)
                print(file)
                self.file_path = os.path.join(root, file)
                self.read_file(True)
                self.new_content = re.sub(r"(URL Address).*",r"\1 of ICOTrial Application", self.content)
                self.write_to_orginal_file()

    def execute_rename_img(self, dir_name, lines):
        for root, dirs, files in os.walk(os.path.join(self.dir_path, dir_name)):
            # for dir in dirs:
            for file in files:
                print(file)
                self.file_path = os.path.join(root, file)
                self.read_file()
                self.name_img_in_screenshot(standardlize=True, lines = lines)
                self.write_to_orginal_file()


t = Refactor(sys.argv[1])
# t = Refactor("D:\svn_master\\uat_services_master\src\\robot\TestPlan\TestSuites\\")
# t = Refactor("D:\\")
# t.space_refactor_directory('Locators')
# replace SS_img or SS_00 to SS_00,01,02 (ordering)
# t.execute_rename_img(sys.argv[2], True)
# t.replace_url_link(sys.argv[2])
t.rename_screenshot_png(sys.argv[2])