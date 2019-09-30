import struct
from fnvhash import fnv1_32

class StringTableString:
    def __init__(self):
        self.mnKeyHash = None
        self.mnFlags = 0
        self.mnLength = None
        self.contents = None

    def read_headers(self, data):
        self.mnKeyHash = struct.unpack('<I', data[:4])[0]
        self.mnFlags = data[4]
        self.mnLength = struct.unpack('<H', data[5:7])[0]

    def read_contents(self, data):
        self.contents = data

    def set_string(self, data, name = None):
        self.mnKeyHash = fnv1_32(data.encode('ascii')) if name is None else fnv1_32(name.encode('ascii'))
        self.mnLength = len(data)
        self.contents = data.encode('ascii')

    def contents_size(self):
        return self.mnLength

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(struct.pack('<I', self.mnKeyHash))
        byte_data.extend(bytearray([self.mnFlags]))
        byte_data.extend(struct.pack('<H', self.mnLength))
        byte_data.extend(self.contents)
        return byte_data
