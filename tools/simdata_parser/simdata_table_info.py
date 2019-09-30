import struct

class SimdataTableInfo:
    def __init__(self):
        self.mnNameOffset = None
        self.mnNameHash = None
        self.mnSchemaOffset = None
        self.mnDataType = None
        self.mnRowSize = None
        self.mnRowOffset = None
        self.mnRowCount = None

    def read(self, data):
        self.mnNameOffset = struct.unpack('<i', data[:4])[0]
        self.mnNameHash = struct.unpack('<I', data[4:8])[0]
        self.mnSchemaOffset = struct.unpack('<i', data[8:12])[0]
        self.mnDataType = struct.unpack('<I', data[12:16])[0]
        self.mnRowSize = struct.unpack('<I', data[16:20])[0]
        self.mnRowOffset = struct.unpack('<i', data[20:24])[0]
        self.mnRowCount = struct.unpack('<I', data[24:28])[0]

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(struct.pack('<i', self.mnNameOffset))
        byte_data.extend(struct.pack('<I', self.mnNameHash))
        byte_data.extend(struct.pack('<i', self.mnSchemaOffset))
        byte_data.extend(struct.pack('<I', self.mnDataType))
        byte_data.extend(struct.pack('<I', self.mnRowSize))
        byte_data.extend(struct.pack('<i', self.mnRowOffset))
        byte_data.extend(struct.pack('<I', self.mnRowCount))
        return byte_data

    def __str__(self):
        return ("Simdata Table Info: \n" +
            f"  mnNameOffset: {self.mnNameOffset}\n" +
            f"  mnNameHash: {self.mnNameHash}\n" +
            f"  mnSchemaOffset: {self.mnSchemaOffset}\n" +
            f"  mnDataType: {self.mnDataType}\n" +
            f"  mnRowSize: {self.mnRowSize}\n" +
            f"  mnRowOffset: {self.mnRowOffset}\n" +
            f"  mnRowCount: {self.mnRowCount}\n" +
        "\n")
