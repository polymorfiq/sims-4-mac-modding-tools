import struct
import datetime
from .constants import MAGIC_NUMBER
from .simdata_file import SimdataFile
from .simdata_file_header import SimdataFileHeader

class SimdataFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.simdata = SimdataFile()

    def parse(self):
        self.open()

        try:
            self.simdata.headers = self.get_headers()

        finally:
            self.close()

        return self.simdata

    def get_headers(self):
        headers = SimdataFileHeader()

        headers.mnFileIdentifier = self.file_contents[:4].decode('ascii')
        if headers.mnFileIdentifier != MAGIC_NUMBER: raise InvalidFileFormat()

        headers.mnVersion = struct.unpack('<I', self.file_contents[4:8])[0]

        headers.mnVersion = struct.unpack('<I', self.file_contents[4:8])[0]
        print(headers)

    def open(self):
        self.file = open(self.file_path, mode='rb')
        self.file_contents = self.file.read()

    def close(self):
        self.file.close()
        self.file = None
