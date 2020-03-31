#!/usr/bin/env python
import sys
import getopt
import os


class Ext:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def usage(cls):
        help_text = [
            cls.HEADER + 'Usage:' + cls.ENDC,
            cls.OKGREEN + '\tsuext' + cls.ENDC,
            cls.OKGREEN + '\tsuext ' + cls.OKBLUE + cls.UNDERLINE + '<filename>' + cls.ENDC,
            cls.OKGREEN + '\tsuext ' + cls.OKBLUE + cls.UNDERLINE + '<dirname>' + cls.ENDC,
            cls.OKGREEN + '\tsuext ' + cls.OKBLUE + '-h|--help' + cls.ENDC,
            cls.HEADER + 'Options:' + cls.ENDC,
            '\t' + cls.OKBLUE + cls.UNDERLINE + '<filename>' + cls.ENDC + '\tFull or relative path to filename for '
                                                                          'showing file extension.',
            '\t' + cls.OKBLUE + cls.UNDERLINE + '<dirname>' + cls.ENDC + '\tFull or relative path to directory for '
                                                                         'showing all files extension in this '
                                                                         'directories.',
            '\t' + cls.OKBLUE + '-h --help' + cls.ENDC + '\tShow this screen.'
        ]
        return '\n'.join(help_text)

    @classmethod
    def get_file_extension(cls, filename):
        ext = filename.split('.')[-1]
        return ext.split('/')[-1]

    @classmethod
    def get_file_extensions_in_dir(cls, dirname, return_list=True):
        files_extensions = []
        try:
            for filename in os.listdir(dirname):
                if os.path.isfile(os.path.join(dirname, filename)):
                    files_extensions.append(cls.get_file_extension(os.path.join(dirname, filename)))
        except OSError as err:
            raise err

        if return_list:
            return files_extensions
        return '\n'.join(files_extensions)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(Ext.FAIL + str(err) + Ext.ENDC)
        print(Ext.usage())
        sys.exit(2)

    if not (opts or args):
        print(Ext.usage())
        sys.exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(Ext.usage())
            sys.exit()

    if os.path.isfile(args[0]):
        print(Ext.get_file_extension(args[0]))
        sys.exit()
    else:
        try:
            print(Ext.get_file_extensions_in_dir(args[0], False))
            sys.exit()
        except Exception as err:
            print(Ext.FAIL + str(err) + Ext.ENDC)
            sys.exit(2)


if __name__ == '__main__':
    main()
