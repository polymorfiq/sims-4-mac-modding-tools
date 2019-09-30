from .simdata_errors import SchemaNotFound, StringNotFound

class SimdataFile:
    def __init__(self):
        self.headers = None
        self.table_info = []
        self.table_data = []
        self.schemas = []
        self.strings = []

    def schema_at_position(self, pos):
        for curr_schema in self.schemas:
            if curr_schema.position == pos:
                return curr_schema

        raise SchemaNotFound()

    def string_at_position(self, pos):
        for curr_str in self.strings:
            if curr_str.position == pos:
                return curr_str.contents

        raise StringNotFound()

    def to_bytearray(self):
        byte_data = bytearray([])
        byte_data.extend(self.headers.to_bytearray())

        for table_info in self.table_info:
            byte_data.extend(table_info.to_bytearray())

        byte_data.extend(self.table_data.to_bytearray())

        for schema in self.schemas:
            byte_data.extend(schema.to_bytearray())

        for curr_str in self.strings:
            if len(curr_str.contents) > 0:
                byte_data.extend(curr_str.to_bytearray())
                byte_data.extend(bytearray([0x00]))

        return byte_data
