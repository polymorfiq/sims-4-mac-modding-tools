import sys
import os
sys.path.append(os.path.abspath('../../tools'))
from package_parser import PackageFileWriter
from string_table_parser import StringTableWriter

writer = PackageFileWriter()
writer.add_resource_file('0xE882D22F_0x00000000_0x0000000000008357.art_View.InteractionTuning.xml')

string_writer = StringTableWriter('CORY_TEST')
string_writer.add_string('Observe Art', name='Cory_TEST_OBSERVE')
writer.add_writer(string_writer)
print(hex(string_writer.resource_instance_id))

package_data = writer.to_bytearray()
with open('build/observe_art.package', 'w+b') as f:
    f.write(package_data)
