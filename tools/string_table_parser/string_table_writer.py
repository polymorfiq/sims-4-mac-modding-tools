from .string_table_file import StringTableFile

class StringTableWriter:
    def __init__(self):
        self.string_table = StringTableFile()
        self.string_table.headers = StringTableHeader()
        self.string_table.headers.mnNumEntries = 0
        self.string_table.headers.mnStringLength = 0

    def add_string(self, new_string):
        string_item = StringTableString()
        string_item.set_string(new_string)

        self.string_table.strings.append(string_item)
        self.string_table.headers.nmNumEntries += 1
        self.string_table.headers.mnStringLength += string_item.contents_size()

    def to_bytearray(self):
        return self.string_table.to_bytearray()
