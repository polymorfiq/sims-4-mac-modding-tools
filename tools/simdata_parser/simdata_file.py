from .simdata_errors import SchemaNotFound, StringNotFound

class SimdataFile:
    def __init__(self):
        self.headers = None
        self.table_info = None
        self.schemas = None
        self.strings = None
        self.rows = None

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
