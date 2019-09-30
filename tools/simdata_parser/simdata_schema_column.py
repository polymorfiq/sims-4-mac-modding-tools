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

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(struct.pack('<i', self.mnNameOffset))
        byte_data.extend(struct.pack('<I', self.mnNameHash))
        byte_data.extend(struct.pack('<H', self.mnDataType))
        byte_data.extend(struct.pack('<H', self.mnFlags))
        byte_data.extend(struct.pack('<I', self.mnOffset))
        byte_data.extend(struct.pack('<i', self.mnSchemaOffset))
        return byte_data

    def name_position(self):
        return self.position + self.mnNameOffset
