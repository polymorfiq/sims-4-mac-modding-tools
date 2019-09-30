import struct

class SimdataSchemaColumn:
    def __init__(self):
        self.position = None
        self.mnNameOffset = None
        self.mnNameHash = None
        self.mnDataType = None
        self.mnFlags = None
        self.mnOffset = None
        self.mnSchemaOffset = None

    def read(self, data):
        self.mnNameOffset = struct.unpack('<i', data[:4])[0]
        self.mnNameHash = struct.unpack('<I', data[4:8])[0]
        self.mnDataType = struct.unpack('<H', data[8:10])[0]
        self.mnFlags = struct.unpack('<H', data[10:12])[0]
        self.mnOffset = struct.unpack('<I', data[12:16])[0]
        self.mnSchemaOffset = struct.unpack('<i', data[16:20])[0]

    def name_position(self):
        return self.position + self.mnNameOffset
