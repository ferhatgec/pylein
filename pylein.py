#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#

# PyLein : colorful CLI File information tool.
#
# github.com/ferhatgec/pylein
#
#

from requests import get
from sys      import argv, exit
from re       import search

website='https://fileinfo.com/extension/{file_format}'

class Pylein:
    def __init__(self):
        self.extension  = ''
        self.info       = ''
        self.data       = ''

        self.raw_extension = '<h2><span class="fileType">(.*)</span>(.*)</h2>'
        self.raw_info      = '<div class="infoBox">\n<p>(.*)</p>\n</div>'

    def hmm(self, length: int):
        for i in range(0, length):
            print('-', end='')

        print()

    def initialize(self, extension: str):
        if not self.check_internet_connection():
            print('Oops!')
            exit(1)

        self.extension = extension

        self.data = get(website.format(file_format=self.extension)).text

        self.parse_extension()

    def parse_extension(self):
        data = search(self.raw_extension, self.data)
        info = search(self.raw_info     , self.data)

        if data and info:
            print('\033[0;95m'
                  + data[2]
                  + '\033[0m',
                  '\033[0;97m(\033[0;93m'
                  + self.extension
                  + '\033[0;97m)',
                  end='\033[0m\n')

            self.hmm(len(data[2]))

            self.info = info[1]

            for line in self.info.split('.  '):
                if 'href' not in line:
                    # Replace newline after . (dot) and , (comma) to make it easy-to readable

                    line = line.replace('.  ', '.\n')
                    line = line.replace(', ' , ',\n')

                    line = line.replace(self.extension.lower(),
                                          ('\033[0;93m'
                                           + self.extension.lower()
                                           + '\033[0;97m'))

                    line = line.replace(self.extension.upper(),
                                          ('\033[0;93m'
                                           + self.extension.upper()
                                           + '\033[0;97m'))

                    print('\033[0;97m', line, sep='', end='\033[0m\n')
        else:
            print('Not found :^(')

        exit(0)


    # From github.com/ferhatgec/pycliwidget
    @staticmethod
    def check_internet_connection() -> bool:
        try:
            import httplib
        except:
            import http.client as httplib

        connection = httplib.HTTPConnection("www.google.com", timeout=1)

        try:
            connection.request("HEAD", "/")
            connection.close()

            return True
        except:
            connection.close()

            return False

if len(argv) < 2:
    print('PyLein - CLI file-info reader',
          '------',
          argv[0] + ' {extension}',
          sep='\n')

    exit(1)


init = Pylein()

init.initialize(argv[1])