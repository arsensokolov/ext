#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import os
import magic
from tabulate import tabulate

__version__ = '0.0.2'


class Ext:
    def __init__(self, *args, **kwargs):
        self.table = kwargs.get('table', False)
        self.mime_type = kwargs.get('mime_type', False)
        self.mime_type_description = kwargs.get('mime_type_description', False)
        self.is_console = kwargs.get('is_console', False)
        self.system = os.name

    @property
    def _headers(self):
        headers = [
            'File name',
            'File extension',
        ]
        if self.mime_type:
            headers.append('MIME type')
        if self.mime_type_description:
            headers.append('MIME description')
        return headers

    def _render_in_table(self, rows):
        return tabulate(rows, headers=self._headers)

    def get_file_extension(self, filename):
        result = [filename]
        ext = filename.split('.')[-1]
        if self.system == 'nt':
            true_ext = ext.split('\\')[-1]
        else:
            true_ext = ext.split('/')[-1]
        result.append(true_ext)

        if self.mime_type:
            result.append(magic.from_file(filename, mime=True))
        if self.mime_type_description:
            result.append(magic.from_file(filename))

        if self.is_console and (self.mime_type or self.mime_type_description):
            if self.table:
                return tabulate([result], headers=self._headers)
            else:
                return '\n'.join(result)
        if self.mime_type or self.mime_type_description:
            return result
        return true_ext

    def get_extensions_in_dir(self, dirname):
        rows = []
        try:
            for filename in os.listdir(dirname):
                if os.path.isfile(os.path.join(dirname, filename)):
                    ext = self.get_file_extension(os.path.join(dirname, filename))
                    row = [
                        filename,
                        ext,
                    ]
                    if self.mime_type:
                        row.append(magic.from_file(os.path.join(dirname, filename), mime=True))
                    if self.mime_type_description:
                        row.append(magic.from_file(os.path.join(dirname, filename)))
                    rows.append(row)
        except OSError as err:
            raise err

        if self.is_console:
            if self.table:
                return self._render_in_table(rows)
            result = []
            for row in rows:
                result.append('\n'.join(row))
            return '\n\n'.join(result)

        return rows


class _C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _usage():
    help_text = [
        _C.HEADER + 'Usage:' + _C.ENDC,
        _C.OKGREEN + '    suext' + _C.ENDC,
        _C.OKGREEN + '    suext ' + _C.OKBLUE + '[-t|--table] [-m|--mime] [-d|--description] ' + _C.UNDERLINE + '<filename>' + _C.ENDC,
        _C.OKGREEN + '    suext ' + _C.OKBLUE + '[-t|--table] [-m|--mime] [-d|--description] ' + _C.UNDERLINE + '<dirname>' + _C.ENDC,
        _C.OKGREEN + '    suext ' + _C.OKBLUE + '-h|--help' + _C.ENDC,
        _C.OKGREEN + '    suext ' + _C.OKBLUE + '-v|--version' + _C.ENDC,
        _C.HEADER + 'Options:' + _C.ENDC,
        '    ' + _C.OKBLUE + _C.UNDERLINE + '<filename>' + _C.ENDC + '\t\tFull or relative path to filename for '
                                                                        'showing file extension.',
        '    ' + _C.OKBLUE + _C.UNDERLINE + '<dirname>' + _C.ENDC + '\t\tFull or relative path to directory for '
                                                                       'showing all files extension in this '
                                                                       'directories.',
        '    ' + _C.OKBLUE + '-t --table' + _C.ENDC + '\t\tDisplay result as table.',
        '    ' + _C.OKBLUE + '-m --mime' + _C.ENDC + '\t\tDisplay mime type.',
        '    ' + _C.OKBLUE + '-d --description' + _C.ENDC + '\tDisplay mime type description.',
        '    ' + _C.OKBLUE + '-h --help' + _C.ENDC + '\t\tShow this screen.',
        '    ' + _C.OKBLUE + '-v --version' + _C.ENDC + '\tShow utility version.',
    ]
    return '\n'.join(help_text)


def _main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'tmdhv', ['table', 'mime', 'description', 'help', 'version'])
    except getopt.GetoptError as err:
        print(_C.FAIL + str(err) + _C.ENDC)
        print(_usage())
        sys.exit(2)

    if not (opts or args):
        print(_usage())
        sys.exit()

    ext = Ext(is_console=True)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(_usage())
            sys.exit()
        elif opt in ('-t', '--table'):
            ext.table = True
        elif opt in ('-m', '--mime'):
            ext.mime_type = True
        elif opt in ('-d', '--description'):
            ext.mime_type_description = True
        elif opt in ('-v', '--version'):
            if ext.system == 'nt':
                filename = sys.argv[0].split('\\')[-1]
            else:
                filename = sys.argv[0].split('/')[-1]
            print(filename + ' version ' + __version__)
            sys.exit()

    if os.path.isfile(args[0]):
        print(ext.get_file_extension(args[0]))
        sys.exit()
    else:
        try:
            print(ext.get_extensions_in_dir(args[0]))
            sys.exit()
        except Exception as err:
            print(_C.FAIL + str(err) + _C.ENDC)
            sys.exit(2)


if __name__ == '__main__':
    _main()
