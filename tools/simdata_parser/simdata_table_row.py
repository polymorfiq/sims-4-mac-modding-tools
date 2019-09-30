import struct
from .helpers import unpack_for_type

class SimdataTableRow:
    def __init__(self, name, data, data_type):
        self.name = name
        self.data = data
        self.data_type = data_type

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(struct.pack(unpack_for_type(self.data_type), *self.data))
        return byte_data
