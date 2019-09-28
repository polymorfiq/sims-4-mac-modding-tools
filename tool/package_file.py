import struct

class PackageFile:
    def __init__(self):
        self.headers = None
        self.index_entries = None
        self.records = None


    def __str__(self):
        my_str = str(self.headers) + "\n\n\n"

        for entry in self.index_entries:
            my_str += str(entry) + "\n\n"

        return my_str

class PackageFileHeader:
    def __init__(self):
        # Magic Number - Should always = 'DBPF' in .package files
        self.mnFileIdentifier = None
        self.mnFileVersion = None
        self.mnUserVersion = None
        self.unused1 = None

        # Typically not set
        self.mnCreationTime = None

        # Typically not set
        self.mnUpdatedTime = None

        self.unused2 = None
        self.mnIndexRecordEntryCount = None
        self.mnIndexRecordPositionLow = None
        self.mnIndexRecordSize = None
        self.unused3 = None

        # Always 3 for historical purposes
        self.unused4 = None

        self.mnIndexRecordPosition = None
        self.unused5 = None
        self.flags = None

    def __str__(self):
        return ("Package Headers:\n" +
        f"  mnFileIdentifier: {self.mnFileIdentifier}\n" +
        f"  mnFileVersion: {self.mnFileVersion}\n" +
        f"  mnUserVersion: {self.mnUserVersion}\n" +
        f"  unused1: {self.unused1}\n" +
        f"  mnCreationTime: {self.mnCreationTime}\n" +
        f"  mnUpdatedTime: {self.mnUpdatedTime}\n" +
        f"  unused2: {self.unused2}\n" +
        f"  mnIndexRecordEntryCount: {self.mnIndexRecordEntryCount}\n" +
        f"  mnIndexRecordPositionLow: {self.mnIndexRecordPositionLow}\n" +
        f"  mnIndexRecordSize: {self.mnIndexRecordSize}\n" +
        f"  unused3: {self.unused3}\n" +
        f"  unused4: {self.unused4}\n" +
        f"  mnIndexRecordPosition: {self.mnIndexRecordPosition}\n" +
        f"  unused5: {self.unused5}\n" +
        f"  flags: {self.flags}\n")

class PackageVersion:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __str__(self):
        return f"{self.major}.{self.minor}"


COMPRESSION_TYPES = {
    0x0000: "Uncompressed",
    0xfffe: "Streamable compression",
    0xffff: "Internal compression",
    0xffe0: "Deleted record",
    0x5a42: "ZLIB"
}

RESOURCE_TYPES = {
    0x034aeecb: "Create a Sim (CAS) Catalog Instance",
    0x545ac67a: "Simdata"
}

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

        self.mnSize                     = data_desc & 0b01111111111111111111111111111111
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
        total_size = 20

        if self.flags.constantType == 0: total_size += 4
        if self.flags.constantGroup == 0: total_size += 4
        if self.flags.constantInstanceEx == 0: total_size += 4
        if self.mbExtendedCompressionType == 1: total_size += 4

        return total_size

    def __str__(self):
        return ("PackageIndexEntry:\n" +
            f"  mType: " + to_hex(self.mType) + "\n" +
            f"  mGroup: " + to_hex(self.mGroup) + "\n" +
            f"  mInstanceEx: " + to_hex(self.mInstanceEx) + "\n" +
            f"  mInstance: " + to_hex(self.mInstance) + "\n" +
            f"  mnPosition: {self.mnPosition}\n" +
            f"  mnSize: {self.mnSize}\n" +
            f"  mbExtendedCompressionType: {self.mbExtendedCompressionType}\n" +
            f"  mnSizeDecompressed: {self.mnSizeDecompressed}\n" +
            f"  mnCompressionType: {self.mnCompressionType}\n" +
            f"  mnCommitted: {self.mnCommitted}\n")

class PackageFlags:
    def __init__(self, constantType, constantGroup, constantInstanceEx, reserved):
        self.constantType = constantType
        self.constantGroup = constantGroup
        self.constantInstanceEx = constantInstanceEx
        self.reserved = reserved

        # Set if flags.constantType != 0
        self.constantTypeId = None

        # Set if flags.constantGroup != 0
        self.constantGroupId = None

        # Set if flags.constantInstanceEx != 0
        self.constantInstanceIdEx = None

    def __str__(self):
        return ("(" +
            f"constantType: {self.constantType}, " +
            f"constantGroup: {self.constantGroup}, " +
            f"constantInstanceEx: {self.constantInstanceEx}, " +
            f"reserved: {self.reserved}, " +
            f"constantTypeId: " + to_hex(self.constantTypeId) + ", " +
            f"constantGroupId: " + to_hex(self.constantGroupId) + ", " +
            f"constantInstanceIdEx: " + to_hex(self.constantInstanceIdEx) +
            ")")

def to_hex(num):
    if num is None: return 'None'

    return "0x{:02x}".format(num)
