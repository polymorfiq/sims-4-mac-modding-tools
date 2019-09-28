import struct
import datetime
from package_file import PackageFile, PackageFileHeader, PackageVersion, PackageFlags, PackageIndexEntry
from package_errors import InvalidFileFormat, UnexpectedHeaderUse

MAGIC_NUMBER = 'DBPF'

class PackageFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.package = PackageFile()

    def parse(self):
        self.open()

        try:
            (headers, after_flag_pos) = self.get_headers()
            self.package.headers = headers

            self.package.index_entries = self.get_index_entries(after_flag_pos)
            self.package.records = self.get_records()

            print(self.package)

        finally:
            self.close()

    def get_headers(self):
        headers = PackageFileHeader()

        headers.mnFileIdentifier = self.file_contents[:4].decode('ascii')
        if headers.mnFileIdentifier != MAGIC_NUMBER: raise InvalidFileFormat()

        headers.mnFileVersion = PackageVersion(
            major=struct.unpack('<I', self.file_contents[4:8])[0],
            minor=struct.unpack('<I', self.file_contents[8:12])[0]
        )

        headers.mnUserVersion = PackageVersion(
            major=struct.unpack('<I', self.file_contents[12:16])[0],
            minor=struct.unpack('<I', self.file_contents[16:20])[0]
        )

        headers.unused1 = struct.unpack('<I', self.file_contents[20:24])[0]

        headers.mnCreationTime = datetime.datetime.utcfromtimestamp(struct.unpack('<I', self.file_contents[24:28])[0])
        headers.mnUpdatedTime = datetime.datetime.utcfromtimestamp(struct.unpack('<I', self.file_contents[28:32])[0])

        headers.unused2 = struct.unpack('<I', self.file_contents[32:36])[0]

        headers.mnIndexRecordEntryCount = struct.unpack('<I', self.file_contents[36:40])[0]
        headers.mnIndexRecordPositionLow = struct.unpack('<I', self.file_contents[40:44])[0]
        headers.mnIndexRecordSize = struct.unpack('<I', self.file_contents[44:48])[0]

        headers.unused3 = struct.unpack('<III', self.file_contents[48:60])

        headers.unused4 = struct.unpack('<I', self.file_contents[60:64])[0]

        # This is UINT64, or long long, which might fail on some computers
        # See notes (2) on: https://docs.python.org/2/library/struct.html
        headers.mnIndexRecordPosition = struct.unpack('<Q', self.file_contents[64:72])[0]

        headers.unused5 = struct.unpack('<IIIIII', self.file_contents[72:96])

        indexPos = headers.mnIndexRecordPosition if headers.mnIndexRecordPosition != 0 else headers.mnIndexRecordPositionLow

        flag_data = struct.unpack('<I', self.file_contents[indexPos:indexPos+4])[0]

        headers.flags = PackageFlags(
            constantType        = (flag_data & 0b00000000000000000000000000000001),
            constantGroup       = (flag_data & 0b00000000000000000000000000000010) >> 1,
            constantInstanceEx  = (flag_data & 0b00000000000000000000000000000100) >> 2,
            reserved            = (flag_data & 0b11111111111111111111111111111000) >> 3
        )

        after_flags = indexPos+4
        if headers.flags.constantType != 0:
            headers.flags.constantTypeId = struct.unpack('<I', self.file_contents[after_flags:after_flags+4])[0]
            after_flags += 4

        if headers.flags.constantGroup != 0:
            headers.flags.constantGroupId = struct.unpack('<I', self.file_contents[after_flags:after_flags+4])[0]
            after_flags += 4

        if headers.flags.constantInstanceEx != 0:
            headers.flags.constantInstanceIdEx = struct.unpack('<I', self.file_contents[after_flags:after_flags+4])[0]
            after_flags += 4

        return (headers, after_flags)

    def get_index_entries(self, indices_start_pos):
        index_entries = []
        headers = self.package.headers

        curr_entry_offset = 0
        for i in range(headers.mnIndexRecordEntryCount):
            index_entry = PackageIndexEntry(self.package.headers.flags)

            entry_size = index_entry.size()
            start_pos = indices_start_pos + curr_entry_offset
            end_pos = start_pos + entry_size

            index_entry.read(self.file_contents[start_pos:end_pos])
            index_entries.append(index_entry)

            curr_entry_offset += entry_size

        return index_entries

    def get_records(self):
        records = []
        headers = self.package.headers
        index_entries = self.package.index_entries

        for i in range(headers.mnIndexRecordEntryCount):
            index_entry = index_entries[i]
            raw_record_data = self.file_contents[index_entry.mnPosition:index_entry.mnPosition+index_entry.mnSize]
            records.append(raw_record_data)

        return records

    def open(self):
        self.file = open(self.file_path, mode='rb')
        self.file_contents = self.file.read()

    def close(self):
        self.file.close()
        self.file = None
