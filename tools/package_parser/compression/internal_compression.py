import struct
from .constants import INTERNAL_COMPRESSION_TYPE_LARGE, INTERNAL_COMPRESSION_TYPES
from .compression_errors import InvalidCompressionType, InvalidMagicNumber, UnknownControlCode

# DBPF/Compression format described here:
# http://modthesims.info/wiki.php?title=Sims_3:DBPF/Compression

class InternalCompression:
    def __init__(self, debug = False):
        self.debug = debug
        self.compression_type = None
        self.magic_number = None # Should always be 0xFB
        self.uncompressed_size = None # 3 bytes, 4 bytes if INTERNAL_COMPRESSION_TYPES['LARGE']

    def decompress(self, data):
        self.compression_type = data[0]
        if self.compression_type not in INTERNAL_COMPRESSION_TYPES:
            raise InvalidCompressionType()

        self.magic_number = data[1]
        if self.magic_number != 0xFB:
            raise InvalidMagicNumber()

        self.header_size = 2
        if self.compression_type == INTERNAL_COMPRESSION_TYPE_LARGE:
            self.uncompressed_size = struct.unpack('>I', data[2:6])[0]
            self.header_size += 4
        else:
            raw_data = struct.unpack('>I', data[2:6])[0]

            # We only care about the first 3 bytes
            # TODO: Is there a way to unpack a 3 byte uint without this in struct?
            self.uncompressed_size = (raw_data & 0b11111111111111111111111100000000) >> 8
            self.header_size += 3

        curr_offset = self.header_size

        self.output = []
        while curr_offset is not None and curr_offset < len(data):
            next_offset = self.parse_control_character(data, curr_offset)
            curr_offset = next_offset

        return bytes(self.output)

    def parse_control_character(self, data, offset, debug = False):
        cc_length = None
        num_plain_text = None
        num_to_copy = None
        copy_offset = None

        byte_0 = data[offset]
        if byte_0 >= 0x00 and byte_0 <= 0x7F:
            byte_1 = data[offset+1]
            cc_length = 2
            num_plain_text = byte_0 & 0x03
            num_to_copy = ((byte_0 & 0x1C) >> 2) + 3
            copy_offset = ((byte_0 & 0x60) << 3) + byte_1 + 1

            if self.debug: print("0x00-0x7F", (offset, cc_length, num_plain_text, num_to_copy, copy_offset))

        elif byte_0 >= 0x80 and byte_0 <= 0xBF:
            (byte_1, byte_2) = (data[offset+1], data[offset+2])
            cc_length = 3
            num_plain_text = ((byte_1 & 0xC0) >> 6) & 0x03
            num_to_copy = (byte_0 & 0x3F) + 4
            copy_offset = ((byte_1 & 0x3F) << 8) + byte_2 + 1

            if self.debug: print("0x80-0xBF", (offset, cc_length, num_plain_text, num_to_copy, copy_offset))

        elif byte_0 >= 0xC0 and byte_0 <= 0xDF:
            (byte_1, byte_2, byte_3) = (data[offset+1], data[offset+2], data[offset+3])
            cc_length = 4
            num_plain_text = byte_0 & 0x03
            num_to_copy = ((byte_0 & 0x0C) << 6) + byte_3 + 5
            copy_offset = ((byte_0 & 0x10) << 12) + (byte_1 << 8) + byte_2 + 1

            if self.debug: print("0xC0-0xDF", (offset, cc_length, num_plain_text, num_to_copy, copy_offset))

        elif byte_0 >= 0xE0 and byte_0 <= 0xFB:
            cc_length = 1
            num_plain_text = ((byte_0 & 0x1F) << 2) + 4
            num_to_copy = 0
            copy_offset = None

            if self.debug: print("0xE0-0xFB", (offset, cc_length, num_plain_text, num_to_copy, copy_offset))

        elif byte_0 >= 0xFC and byte_0 <= 0xFF:
            cc_length = 1
            num_plain_text = (byte_0 & 0x03)
            num_to_copy = 0
            copy_offset = None

            if self.debug: print("0xFC-0xFF", (offset, cc_length, num_plain_text, num_to_copy, copy_offset))

        else:
            raise UnknownControlCode()

        start_of_plain_text = offset + cc_length
        if self.debug: print("start_of_plain_text", start_of_plain_text)

        curr_plain_text_offset = start_of_plain_text
        for i in range(num_plain_text):
            self.output.append(data[curr_plain_text_offset])
            curr_plain_text_offset += 1

        curr_output_text_offset = copy_offset
        for i in range(num_to_copy):
            self.output.append(self.output[-curr_output_text_offset])

        return offset + cc_length + num_plain_text


    def __str__(self):
        return ("Internal Compression: \n" +
            f"  compression_type: {hex(self.compression_type)}\n" +
            f"  magic_number: {hex(self.magic_number)}\n" +
            f"  uncompressed_size: {self.uncompressed_size}\n" +
            f"  header_size: {self.header_size}\n" +
            f"  output_size: {len(self.output)}\n\n"
        )
