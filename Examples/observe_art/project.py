import sys
import os
import lxml.etree as etree
sys.path.append(os.path.abspath('../../tools'))
from package_parser import PackageFileWriter
from string_table_parser import StringTableWriter
from tuning_parser import TuningWriter

writer = PackageFileWriter()

string_writer = StringTableWriter('SPP_TEST_OBSERVE_ART')
OBSERVE_ART = string_writer.add_string('Observe Art', name='SPP_TEST_OBSERVE_ART_STRING')

tuning_writer = TuningWriter()
tuning_writer.load_file('game_files/0xE882D22F_0x00000000_0x0000000000008357.art_View.InteractionTuning.xml')
tuning_writer.xml.xpath("//*[@n='display_name']")[0].text = OBSERVE_ART.hash_str()

writer.add_writer(string_writer)
writer.add_writer(tuning_writer)

package_data = writer.to_bytearray()
with open('build/observe_art.package', 'w+b') as f:
    f.write(package_data)
