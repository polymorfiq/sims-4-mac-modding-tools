import struct
from .constants import MAGIC_NUMBER
from .string_table_errors import InvalidFileFormat

class StringTableHeader:
    def __init__(self):
        # Should always be STBL
        self.mnFileIdentifier = None

        # Base game version is 5
        self.mnVersion = 5

        # Compression is not currently supported by Sims 4
        self.mbCompressed = 0

        self.mnNumEntries = None
        self.mReserved = [0, 0]
        self.mnStringLength = None

    def read(self, data):
        self.mnFileIdentifier = data[:4].decode('ascii')
        if self.mnFileIdentifier != MAGIC_NUMBER:
            raise InvalidFileFormat()

        self.mnVersion = struct.unpack('<H', data[4:6])[0]
        self.mbCompressed = data[6]

        # This is UINT64, or long long, which might fail on some computers
        # See notes (2) on: https://docs.python.org/2/library/struct.html
        self.mnNumEntries = struct.unpack('<Q', data[7:15])[0]

        self.mReserved = [data[15], data[16]]
        self.mnStringLength = struct.unpack('<I', data[17:21])[0]
