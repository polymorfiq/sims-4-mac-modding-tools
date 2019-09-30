import struct
import datetime
from .constants import MAGIC_NUMBER, RELOFFSET_NULL, HEADER_SIZE, HEADER_TABLE_OFFSET_OFFSET, TABLE_HEADER_SIZE, HEADER_SCHEMA_OFFSET_OFFSET, SCHEMA_HEADER_SIZE, SCHEMA_COLUMN_OFFSET_OFFSET, SCHEMA_COLUMN_SIZE, TABLE_SCHEMA_OFFSET_OFFSET
from .simdata_errors import SchemaNotFound
from .helpers import alignment_for_type, unpack_for_type
from .simdata_file import SimdataFile
from .simdata_file_header import SimdataFileHeader
from .simdata_table_info import SimdataTableInfo
from .simdata_schema import SimdataSchema
from .simdata_string import SimdataString
from .simdata_table_data import SimdataTableData
from .simdata_table_row import SimdataTableRow

class SimdataFileReader:
    def __init__(self, file_path, file_contents = None):
        self.file_path = file_path
        self.file_contents = file_contents
        self.file = None
        self.simdata = SimdataFile()

    def parse(self):
        self.open()

        try:
            self.simdata.headers = self.get_headers()
            self.simdata.table_info = self.get_tables()
            (self.simdata.schemas, end_of_schemas) = self.get_schema()
            self.simdata.strings = self.get_strings(end_of_schemas)
            self.simdata.table_data = self.get_table_data()

        finally:
            self.close()

        return self.simdata

    def get_headers(self):
        headers = SimdataFileHeader()
        headers.read(self.file_contents[:HEADER_SIZE])
        if headers.mnNumTables > 1: print(headers)

        return headers

    def get_tables(self):
        table_infos = []
        headers = self.simdata.headers

        start_pos = HEADER_TABLE_OFFSET_OFFSET + headers.mnTableHeaderOffset
        for i in range(headers.mnNumTables):
            table_info = SimdataTableInfo()
            table_info.position = start_pos
            table_info.read(self.file_contents[start_pos:start_pos+TABLE_HEADER_SIZE])
            table_infos.append(table_info)

            start_pos += TABLE_HEADER_SIZE

        return table_infos

    def get_schema(self):
        schemas = []
        headers = self.simdata.headers

        start_pos = HEADER_SCHEMA_OFFSET_OFFSET + headers.mnSchemaOffset
        last_column_end_pos = start_pos
        for i in range(headers.mnNumSchemas):
            schema = SimdataSchema()
            schema.position = start_pos
            schema.read_headers(self.file_contents[start_pos:start_pos+SCHEMA_HEADER_SIZE])

            column_pos = start_pos + SCHEMA_COLUMN_OFFSET_OFFSET + schema.mnColumnOffset
            column_end_pos = column_pos + (schema.mnNumColumns * SCHEMA_COLUMN_SIZE)
            last_column_end_pos = column_end_pos
            schema.read_columns(self.file_contents[column_pos:column_end_pos])

            schemas.append(schema)
            start_pos += SCHEMA_HEADER_SIZE

        return (schemas, last_column_end_pos)

    def get_strings(self, strings_start_pos):
        eof = len(self.file_contents)
        strings = []

        curr_str_start = strings_start_pos
        curr_pos = strings_start_pos
        while curr_pos <= eof:
            if curr_pos == eof or self.file_contents[curr_pos] == 0x00:
                curr_str = self.file_contents[curr_str_start:curr_pos].decode('ascii')
                strings.append(SimdataString(position=curr_str_start, contents=curr_str))

                curr_str_start = curr_pos + 1

            curr_pos += 1

        return strings

    def get_table_data(self):
        headers = self.simdata.headers
        table_info = self.simdata.table_info
        row_start = HEADER_TABLE_OFFSET_OFFSET + headers.mnTableHeaderOffset + (len(self.simdata.table_info) * TABLE_HEADER_SIZE)

        table_data = SimdataTableData()
        curr_pos = row_start
        for info in table_info:
            rows = []

            aligned = self.align(curr_pos, 15)
            if info.mnRowSize > 1: aligned = self.align(aligned, info.mnRowSize - 1)

            alignment = 1
            for r in range(info.mnRowCount):
                if info.mnSchemaOffset == RELOFFSET_NULL:
                    alignment = alignment_for_type(info.mnDataType)
                else:
                    schema_pos = info.position + TABLE_SCHEMA_OFFSET_OFFSET + info.mnSchemaOffset
                    schema = self.simdata.schema_at_position(schema_pos)

                    for column in schema.columns:
                        name_pos = "Unnamed" if column.mnNameOffset == RELOFFSET_NULL else column.name_position()
                        string = self.simdata.string_at_position(name_pos)

                        data_pos = aligned + column.mnOffset
                        data = self.read_data(data_pos, column.mnDataType)
                        row = SimdataTableRow(name=string, data=data, data_type=column.mnDataType)
                        table_data.rows.append(row)

                        column_alignment = alignment_for_type(column.mnDataType)
                        if column_alignment > alignment: alignment = column_alignment

                    aligned += schema.mnSchemaSize
                    alignment = 1

                aligned = self.align(aligned, alignment)
                curr_pos = aligned

        return table_data

    def read_data(self, pos, data_type):
        data_size = alignment_for_type(data_type)

        return struct.unpack(unpack_for_type(data_type), self.file_contents[pos:pos+data_size])

    def align(self, address, alignment_mask):
        pad_amount = -address & alignment_mask
        return address + pad_amount


    def open(self):
        if self.file_path is not None:
            self.file = open(self.file_path, mode='rb')
            self.file_contents = self.file.read()

    def close(self):
        if self.file_path is not None:
            self.file.close()
            self.file = None
