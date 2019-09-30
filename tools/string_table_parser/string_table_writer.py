from fnvhash import fnv1_64
from .string_table_file import StringTableFile
from .string_table_header import StringTableHeader
from .string_table_string import StringTableString
from .constants import STRING_TABLE_RESOURCE_TYPE

class StringTableWriter:
    def __init__(self, name = None):
        self.string_table = StringTableFile()

        self.resource_type = STRING_TABLE_RESOURCE_TYPE
        self.resource_group = 0x8
        if name is not None:
            fnv_hash = fnv1_64(name.encode('ascii'))

            # Set first byte to 0 to default to English
            fnv_hash = fnv_hash & 0b0000000011111111111111111111111111111111111111111111111111111111
            self.resource_instance_id = fnv_hash

        self.string_table.headers = StringTableHeader()
        self.string_table.headers.mnNumEntries = 0
        self.string_table.headers.mnStringLength = 0

    def add_string(self, new_string, name = None):
        string_item = StringTableString()
        string_item.set_string(new_string, name=name)

        self.string_table.strings.append(string_item)
        self.string_table.headers.mnNumEntries += 1
        self.string_table.headers.mnStringLength += string_item.contents_size()

        return string_item

    def to_bytearray(self):
        return self.string_table.to_bytearray()
