import struct
from .constants import SCHEMA_HEADER_SIZE, SCHEMA_COLUMN_SIZE, SCHEMA_COLUMN_OFFSET_OFFSET
from .simdata_schema_column import SimdataSchemaColumn

class SimdataSchema:
    def __init__(self):
        self.position = None
        self.mnNameOffset = None
        self.mnNameHash = None
        self.mnSchemaHash = None
        self.mnSchemaSize = None
        self.mnColumnOffset = None
        self.mnNumColumns = None
        self.columns = []

    def read_headers(self, data):
        self.mnNameOffset = struct.unpack('<i', data[:4])[0]
        self.mnNameHash = struct.unpack('<I', data[4:8])[0]
        self.mnSchemaHash = struct.unpack('<I', data[8:12])[0]
        self.mnSchemaSize = struct.unpack('<I', data[12:16])[0]
        self.mnColumnOffset = struct.unpack('<i', data[16:20])[0]
        self.mnNumColumns = struct.unpack('<I', data[20:24])[0]

    def read_columns(self, data):
        start_pos = 0
        for i in range(self.mnNumColumns):
            column = SimdataSchemaColumn()
            column.read(data[start_pos:start_pos+SCHEMA_COLUMN_SIZE])
            column.position = self.position + SCHEMA_COLUMN_OFFSET_OFFSET + self.mnColumnOffset + (i * SCHEMA_COLUMN_SIZE)

            self.columns.append(column)

            start_pos += SCHEMA_COLUMN_SIZE

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(struct.pack('<i', self.mnNameOffset))
        byte_data.extend(struct.pack('<I', self.mnNameHash))
        byte_data.extend(struct.pack('<I', self.mnSchemaHash))
        byte_data.extend(struct.pack('<I', self.mnSchemaSize))
        byte_data.extend(struct.pack('<i', self.mnColumnOffset))
        byte_data.extend(struct.pack('<I', self.mnNumColumns))

        for column in self.columns:
            byte_data.extend(column.to_bytearray())

        return byte_data

    def size(self):
        return SCHEMA_HEADER_SIZE
