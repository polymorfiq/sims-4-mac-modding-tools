import struct
import binascii
from .constants import COMPRESSION_TYPES
from .helpers import pad_bytes_start, compression_type_by_name

class PackageIndexEntry:
    def __init__(self, flags):
        self.flags = flags

        # if flags.constantType = 0
        self.mType = None

        # if flags.constantGroup = 0
        self.mGroup = None

        # if flags.constantInstanceEx = 0
        self.mInstanceEx = None

        self.mInstance = None
        self.mnPosition = None
        self.mnSize = None
        self.mbExtendedCompressionType = None
        self.mnSizeDecompressed = None

        # if mbExtendedCompressionType = 1
        self.mnCompressionType = None
        self.mnCommitted =  None # typically 1

    def load_resource(self, resource_type, resource_group, resource_instance_id, uncompressed_data, compressed_data):

        # Expects data in big-endian format
        self.mType = struct.unpack('>I', pad_bytes_start(resource_type, 4))[0]
        self.mGroup = struct.unpack('>I', pad_bytes_start(resource_group, 4))[0]
        self.mInstanceEx = struct.unpack('>I', pad_bytes_start(resource_instance_id[:4], 4))[0]
        self.mInstance = struct.unpack('>I', pad_bytes_start(resource_instance_id[4:8], 4))[0]

        self.mnSize = len(compressed_data)
        self.mnSizeDecompressed = len(uncompressed_data)

    def to_bytearray(self):
        raw_data = bytearray([])

        if self.flags.constantType == 0: raw_data.extend(struct.pack('<I', self.mType))
        if self.flags.constantGroup == 0: raw_data.extend(struct.pack('<I', self.mGroup))
        if self.flags.constantInstanceEx == 0: raw_data.extend(struct.pack('<I', self.mInstanceEx))

        raw_data.extend(struct.pack('<I', self.mInstance))
        raw_data.extend(struct.pack('<I', self.mnPosition))

        data_desc = self.mnSize | (self.mbExtendedCompressionType << 31)
        raw_data.extend(struct.pack('<I', data_desc))
        raw_data.extend(struct.pack('<I', self.mnSizeDecompressed))

        if self.mbExtendedCompressionType == 1:
            raw_data.extend(struct.pack('<H', compression_type_by_name(self.mnCompressionType)))
            raw_data.extend(struct.pack('<H', self.mnCommitted))

        return raw_data

    def read(self, entry_data, debug = False):
        start_pos = 0

        if self.flags.constantType == 0:
            self.mType = struct.unpack('<I', entry_data[start_pos:start_pos+4])[0]
            start_pos += 4

        if self.flags.constantGroup == 0:
            self.mGroup = struct.unpack('<I', entry_data[start_pos:start_pos+4])[0]
            start_pos += 4

        if self.flags.constantInstanceEx == 0:
            self.mInstanceEx = struct.unpack('<I', entry_data[start_pos:start_pos+4])[0]
            start_pos += 4

        self.mInstance = struct.unpack('<I', entry_data[start_pos:start_pos+4])[0]
        self.mnPosition = struct.unpack('<I', entry_data[start_pos+4:start_pos+8])[0]

        data_desc = struct.unpack('<I', entry_data[start_pos+8:start_pos+12])[0]
        if debug: print("{0:b}".format(data_desc))

        self.mnSize                     = (data_desc & 0b01111111111111111111111111111111)
        self.mbExtendedCompressionType  = (data_desc & 0b10000000000000000000000000000000) >> 31
        self.mnSizeDecompressed = struct.unpack('<I', entry_data[start_pos+12:start_pos+16])[0]

        if self.mbExtendedCompressionType == 1:
            compression_type_num = struct.unpack('<H', entry_data[start_pos+16:start_pos+18])[0]
            self.mnCompressionType = self.read_compression_type(compression_type_num)
            self.mnCommitted = struct.unpack('<H', entry_data[start_pos+18:start_pos+20])[0]

        if debug: print(self)

    def read_compression_type(self, type_num):
        return COMPRESSION_TYPES.get(type_num, "Unknown")

    def size(self):
        # Base size, regardless of flags
        total_size = 16

        if self.flags.constantType == 0: total_size += 4
        if self.flags.constantGroup == 0: total_size += 4
        if self.flags.constantInstanceEx == 0: total_size += 4
        if self.mbExtendedCompressionType == 1: total_size += 4

        return total_size

    def id(self):
        return f"{self.type_id()}_{self.group_id()}_{self.instance_id()}"

    def type_id(self):
        return '0x' + binascii.b2a_hex(struct.pack('>I', self.mType)).decode('ascii')

    def group_id(self):
        return '0x' + binascii.b2a_hex(struct.pack('>I', self.mGroup)).decode('ascii')

    def instance_id(self):
        return '0x' + binascii.b2a_hex(struct.pack('>I', self.mInstanceEx)).decode('ascii') + binascii.b2a_hex(struct.pack('>I', self.mInstance)).decode('ascii')

    def __str__(self):
        return ("PackageIndexEntry:\n" +
            f"  mType: " + hex(self.mType) + "\n" +
            f"  mGroup: " + hex(self.mGroup) + "\n" +
            f"  mInstanceEx: " + hex(self.mInstanceEx) + "\n" +
            f"  Instance ID: " + self.instance_id() + "\n" +
            f"  mInstance: " + hex(self.mInstance) + "\n" +
            f"  mnPosition: {self.mnPosition}\n" +
            f"  mnSize: {self.mnSize}\n" +
            f"  mbExtendedCompressionType: {self.mbExtendedCompressionType}\n" +
            f"  mnSizeDecompressed: {self.mnSizeDecompressed}\n" +
            f"  mnCompressionType: {self.mnCompressionType}\n" +
            f"  mnCommitted: {self.mnCommitted}\n")
