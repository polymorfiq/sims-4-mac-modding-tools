import struct
from .constants import MAGIC_NUMBER

class SimdataFileHeader:
    def __init__(self):
        self.mnFileIdentifier = None        # Should always be 'DATA'
        self.mnVersion = None               # Base game version is 0x100
        self.mnTableHeaderOffset = None     # Offset of table header data
        self.mnNumTables = None             # Number of table headers
        self.mnSchemaOffset = None          # Offset of schema data
        self.mnNumSchemas = None            # Number of schemas

    def read(self, data):
        self.mnFileIdentifier = data[:4].decode('ascii')
        if self.mnFileIdentifier != MAGIC_NUMBER: raise InvalidFileFormat()

        self.mnVersion = struct.unpack('<I', data[4:8])[0]
        self.mnTableHeaderOffset = struct.unpack('<i', data[8:12])[0]
        self.mnNumTables = struct.unpack('<i', data[12:16])[0]
        self.mnSchemaOffset = struct.unpack('<i', data[16:20])[0]
        self.mnNumSchemas = struct.unpack('<i', data[20:24])[0]

    def __str__(self):
        return ("Simdata File Header: \n" +
            f"  mnFileIdentifier: {self.mnFileIdentifier}\n" +
            f"  mnVersion: {self.mnVersion}\n" +
            f"  mnTableHeaderOffset: {self.mnTableHeaderOffset}\n" +
            f"  mnNumTables: {self.mnNumTables}\n" +
            f"  mnSchemaOffset: {self.mnSchemaOffset}\n" +
            f"  mnNumSchemas: {self.mnNumSchemas}\n" +
        "\n")
