import argparse
import re
import os
import cv2

class Generator(object):
    def __init__(self):
        self.work_dir         = os.getcwd()

        self.content          = None
        self.args             = None
        self.suite_root_path  = 'TestTemplate\\'
        self.data_root_path   = 'Example\\'

    def _get_template(self, temp_path = None):
        """

        :param temp_path: relative path to the template
        :return: string
        """
        with open(temp_path, "r") as file:
            self.content = file.read()
        return self.content

    def create_template(self):
        """
        Create 2 files: data.yaml and suite.robot
        :return: None
        """
        #todo: perform check amongst existing folder
        SUITE_DIR = ['CDA', 'DTR', 'SITE_DQ', 'MVR_SDR']
        DATA_DIR  = ['']
        warning = 'ok'

        # Create data yaml
        self.data_file_name = input('1. Enter the yaml file name. Format <>: ')
        data_path = os.path.join(self.work_dir, self.data_root_path, self.args['data'], self.data_file_name)
        if os.path.exists(data_path):
            warning = input('STOP! This file exists. Continue will re-write the content. Type "ok" to continue: ')
        if warning == 'ok':
            with open(data_path, 'w') as data_write:
                data_write.write(self.args['ticket_id'])

        # Create suite file with replaced content
        self.suite_file_name = input('2. Enter the suite file name. Format <>: ')
        suite_path = os.path.join(self.work_dir, self.suite_root_path, self.args['suite'], self.suite_file_name)
        if os.path.exists(suite_path):
            warning = input('STOP! This file exists. Continue will re-write the content. Type "ok" to continue: ')

        if warning == 'ok':
            content = self._create_test_template()

            with open(suite_path, "w") as suite_write:
                suite_write.write(content)

    def _create_test_template(self):
        """
        Put information into the template
        :return: None
        """
        print('Args: {0}'.format(self.args))
        self._get_template(os.path.join(self.work_dir, 'TestTemplate\Template.txt'))
        urs_title, tags = self._parse_urs_list()
        content = self.content.replace('<ticket_id>', self.args['ticket_id'])
        content = content.replace('<urs_ids>', urs_title)
        if self.args['test_descript'] != None:
            content = content.replace('<test_description>', self.args['test_descript'])
        content = content.replace('<urs_ids_list>', tags)
        return content

    def parse_user_variables(self, **kwargs):
        """
        Read given vars and store them

        :param kwargs:
        :return: None
        """
        parser = argparse.ArgumentParser(prog = 'Generator.py')
        parser.add_argument('-s', '--suite', required = True, help = 'The folder where suite be stored')
        parser.add_argument('-d', '--data', required = True, help = 'The folder where data (yaml) be stored')
        parser.add_argument('-u', '--urs', required = True, help = 'List of urs this test case covered, separate by comma')
        parser.add_argument('-id', '--ticket_id', required = True, help = 'Jira ticket id')
        parser.add_argument('--test_descript', help = 'Test case description')
        self.args = vars(parser.parse_args())
        # print('Args list: {0}'.format(self.args))

    def _parse_urs_list(self):
        urs_list = self.args['urs'].split(',')

        # Check the format of urs
        pattern = re.compile("[A-Z]{2}\_\d+\.\d+\.\d+")
        for item in urs_list:
            if pattern.match(item) == None:
                raise TypeError('URS {0} format is not correct. Check it now!'.format(item))

        urs_as_tag = "  ".join(urs_list)
        urs_as_title = "_".join(urs_list)
        print('Title, tags urs: \n{0} \n {1}'.format(urs_as_title, urs_as_tag))
        return urs_as_title, urs_as_tag
    # def generate

def parser():
    parser = argparse.ArgumentParser(prog = 'Generator.py')
    parser.add_argument('-s', '--suite', required = True, help = 'The folder where suite be stored')
    parser.add_argument('-d', '--data', required = True, help = 'The folder where data (yaml) be stored')
    parser.add_argument('-u', '--urs', required = True, help = 'List of urs this test case covered, separate by comma')
    parser.add_argument('-id', '--ticket_id', required = True, help = 'Jira ticket id')
    parser.add_argument('--test_descript', help = 'Test case description')
    return vars(parser.parse_args())

if __name__ == '__main__':
    args = parser()
    generator = Generator()
    generator.args = args
    generator.create_template()

