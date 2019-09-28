import struct
import datetime
from .package_version import PackageVersion

class PackageFileHeader:
    def __init__(self):
        # Magic Number - Should always = 'DBPF' in .package files
        self.mnFileIdentifier = None
        self.mnFileVersion = None
        self.mnUserVersion = PackageVersion(major=0, minor=0)
        self.unused1 = 0

        # Typically not set
        self.mnCreationTime = datetime.datetime.utcfromtimestamp(0)

        # Typically not set
        self.mnUpdatedTime = datetime.datetime.utcfromtimestamp(0)

        self.unused2 = 0
        self.mnIndexRecordEntryCount = None
        self.mnIndexRecordPositionLow = None
        self.mnIndexRecordSize = None
        self.unused3 = (0, 0, 0)

        # Always 3 for historical purposes
        self.unused4 = 0

        self.mnIndexRecordPosition = None
        self.unused5 = (0, 0, 0, 0, 0, 0)
        self.flags = None

    def to_bytearray(self):
        raw_data = bytearray([])

        raw_data.extend(self.mnFileIdentifier.encode('ascii'))
        raw_data.extend(struct.pack('<I', self.mnFileVersion.major))
        raw_data.extend(struct.pack('<I', self.mnFileVersion.minor))
        raw_data.extend(struct.pack('<I', self.mnUserVersion.major))
        raw_data.extend(struct.pack('<I', self.mnUserVersion.minor))
        raw_data.extend(struct.pack('<I', self.unused1))
        raw_data.extend(struct.pack('<I', int(self.mnCreationTime.timestamp())))
        raw_data.extend(struct.pack('<I', int(self.mnUpdatedTime.timestamp())))
        raw_data.extend(struct.pack('<I', self.unused2))
        raw_data.extend(struct.pack('<I', self.mnIndexRecordEntryCount))
        raw_data.extend(struct.pack('<I', self.mnIndexRecordPositionLow))
        raw_data.extend(struct.pack('<I', self.mnIndexRecordSize))
        raw_data.extend(struct.pack('<III', *self.unused3))
        raw_data.extend(struct.pack('<I', self.unused4))
        raw_data.extend(struct.pack('<Q', self.mnIndexRecordPosition))
        raw_data.extend(struct.pack('<IIIIII', *self.unused5))

        return raw_data

    def size(self):
        return 96

    def index_pos(self):
        return self.mnIndexRecordPosition if self.mnIndexRecordPosition != 0 else self.mnIndexRecordPositionLow

    def after_flags_pos(self):
        return self.index_pos() + self.flags.size()

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
