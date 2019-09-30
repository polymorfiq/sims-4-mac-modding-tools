import re
import binascii
import struct
import lxml.etree as etree

class TuningWriter:
    def __init__(self):
        self.resource_type = None
        self.resource_group = None
        self.resource_instance_id = None

    def load_file(self, file_path, parse_path = True):
        with open(file_path, mode='rb') as f:
            self.data = f.read()

        self.xml = etree.XML(self.data)

        if parse_path: self.parse_filepath(file_path)

    def parse_filepath(self, file_path):
        filename = file_path.split('/')[-1]
        parsed_filename = re.match("0x(.*?)_0x(.*?)_0x(.*?)$", filename)
        parsed_data = parsed_filename.groups()

        self.resource_type = struct.unpack('>I', binascii.a2b_hex(parsed_data[0]))[0]
        self.resource_group = struct.unpack('>I', binascii.a2b_hex(parsed_data[1]))[0]

        instance_id_str = parsed_data[2].split('.')[0]
        resource_name = None
        parsed_instance_id = re.match("(.*?)_(.*?)$", instance_id_str)
        if parsed_instance_id:
            instance_id_str = parsed_instance_id.groups()[0]
            resource_name = parsed_instance_id.groups()[1]

        self.resource_instance_id = struct.unpack('>Q', binascii.a2b_hex(instance_id_str))[0]

    def to_bytearray(self):
        return etree.tostring(self.xml, xml_declaration=True, encoding='utf-8')
