import struct
import datetime
from .constants import MAGIC_NUMBER
from .string_table_file import StringTableFile
from .string_table_header import StringTableHeader
from .string_table_string import StringTableString
from .constants import HEADER_SIZE, STRING_HEADER_SIZE

class StringTableReader:
    def __init__(self, file_path, file_contents = None):
        self.file_path = file_path
        self.string_table = StringTableFile()
        self.file_contents = file_contents

    def parse(self):
        self.open()

        try:
            self.string_table.headers = self.get_headers()
            self.string_table.strings = self.get_strings()

        finally:
            self.close()

        return self.string_table

    def get_headers(self):
        headers = StringTableHeader()
        headers.read(self.file_contents[:HEADER_SIZE])
        return headers

    def get_strings(self):
        strings = []
        headers = self.string_table.headers

        start_pos = HEADER_SIZE
        for i in range(headers.mnNumEntries):
            new_str = StringTableString()
            new_str.read_headers(self.file_contents[start_pos:start_pos+STRING_HEADER_SIZE])

            content_start = start_pos+STRING_HEADER_SIZE
            new_str.read_contents(self.file_contents[content_start:content_start+new_str.contents_size()])
            strings.append(new_str)

            start_pos += STRING_HEADER_SIZE + new_str.contents_size()

        return strings

    def open(self):
        if self.file_path is not None:
            self.file = open(self.file_path, mode='rb')
            self.file_contents = self.file.read()

    def close(self):
        if self.file_path is not None:
            self.file.close()
            self.file = None
            self.file_contents = None
