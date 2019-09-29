import struct

class StringTableString:
    def __init__(self):
        self.mnKeyHash = None
        self.mnFlags = None
        self.mnLength = None
        self.contents = None

    def read_headers(self, data):
        self.mnKeyHash = struct.unpack('<I', data[:4])[0]
        self.mnFlags = data[4]
        self.mnLength = struct.unpack('<H', data[5:7])[0]

    def read_contents(self, data):
        self.contents = data

    def contents_size(self):
        return self.mnLength
