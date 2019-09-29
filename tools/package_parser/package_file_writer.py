import zlib
from .package_file import PackageFile
from .package_file_header import PackageFileHeader
from .package_version import PackageVersion
from .package_flags import PackageFlags
from .package_index_entry import PackageIndexEntry

class PackageFileWriter:
    def __init__(self, package_path):
        self.package_path = package_path

        self.headers = PackageFileHeader()
        self.headers.mnFileIdentifier = 'DBPF'
        self.headers.mnFileVersion = PackageVersion(major=2, minor=1)
        self.headers.mnUserVersion = PackageVersion(major=0, minor=0)
        self.headers.mnIndexRecordPositionLow = 0
        self.headers.mnIndexRecordPosition = 0
        self.headers.constantInstanceIdEx = 0

        self.headers.flags = PackageFlags(
            constantType        = 0,
            constantGroup       = 0,
            constantInstanceEx  = 0,
            reserved            = 0
        )

        self.index_entries = []
        self.records = []
        self.record_data = bytearray([])

    def add_resource(self, type, group, instance_id, data):
        # compressed_data = zlib.compress(data)
        compressed_data = data

        index_entry = PackageIndexEntry(self.headers.flags)
        index_entry.load_resource(type, group, instance_id, data, compressed_data)
        index_entry.mbExtendedCompressionType = 1
        index_entry.mnCompressionType = "Uncompressed"
        index_entry.mnCommitted = 1

        index_entry.mnPosition = self.headers.size() + len(self.record_data)
        self.record_data.extend(compressed_data)

        self.index_entries.append(index_entry)
        self.records.append(compressed_data)


    def write_package_file(self):
        self.headers.mnIndexRecordEntryCount = len(self.index_entries)
        self.headers.mnIndexRecordPosition = self.headers.size() + len(self.record_data)

        index_record_size = 0
        for index_entry in self.index_entries:
            index_record_size += index_entry.size()

        self.headers.mnIndexRecordSize = index_record_size + self.headers.flags.size()

        print(self.headers)

        raw_data = bytearray([])
        raw_data.extend(self.headers.to_bytearray())
        raw_data.extend(self.record_data)
        raw_data.extend(self.headers.flags.to_bytearray())

        for index_entry in self.index_entries:
            raw_data.extend(index_entry.to_bytearray())

        with open(self.package_path, 'w+b') as f:
            f.write(raw_data)
