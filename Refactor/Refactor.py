import os, re, sys

class Refactor(object):
    def __init__(self, path):
        self.lSections = {}
        self.result = []
        self.workdir = os.getcwd()
        self.content = None
        self.new_content = ''
        self.file_path = None
        self.dir_path = path

        self.blank_line_pattern = re.compile(r"[(^\s+)|(^#)]")

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

    def read_file(self):
        with open(self.file_path) as  fileread:
            self.content = fileread.readlines()

    def write_new_content(self):
        for line in self.result:
            self.new_content += line

    def write_to_orginal_file(self):
        with open(os.path.join(self.workdir, self.file_path), "w") as  filewrite:
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

t = Refactor(sys.argv[1])
t.space_refactor_directory('Locators')
print(t.new_content)