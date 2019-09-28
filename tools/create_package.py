import sys
import os
import re
import binascii
from package_parser import PackageFileWriter

EXAMPLE_SOURCE = './tmp/data'
EXAMPLE_PACKAGE = './tmp/output.package'
source_path = sys.argv[1] if len(sys.argv) >= 2 else EXAMPLE_SOURCE
package_path = sys.argv[2] if len(sys.argv) >= 3 else EXAMPLE_PACKAGE

writer = PackageFileWriter(package_path)

def make_even_length(hex_str):
    return hex_str if len(hex_str) % 2 == 0 else '0%s' % hex_str

for root, subdirs, files in os.walk(source_path):
    for filename in files:
        parsed_filename = re.match("0x(.*?)_0x(.*?)_0x(.*?)$", filename)
        if parsed_filename:
            parsed_data = parsed_filename.groups()

            resource_type = binascii.a2b_hex(make_even_length(parsed_data[0]))
            resource_group = binascii.a2b_hex(make_even_length(parsed_data[1]))

            instance_id_str = parsed_data[2].split('.')[0]
            resource_name = None
            parsed_instance_id = re.match("(.*?)_(.*?)$", instance_id_str)
            if parsed_instance_id:
                instance_id_str = parsed_instance_id.groups()[0]
                resource_name = parsed_instance_id.groups()[1]

            resource_instance_id = binascii.a2b_hex(make_even_length(instance_id_str))

            raw_data = None
            with open(f"{root}/{filename}", mode='rb') as f:
                raw_data = f.read()

            writer.add_resource(resource_type, resource_group, resource_instance_id, raw_data)

writer.write_package_file()
