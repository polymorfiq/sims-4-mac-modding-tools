import os
import sys
import lxml.etree as etree
from package_parser import PackageFileReader
from package_parser import resource_type_by_name
from string_table_parser import StringTableReader
from simdata_parser import SimdataFileReader

EXAMPLE_PACKAGE = '../Documentation/TS4_Custom_Content_Guide/Examples/simsmodsquad-novelist.package'
package_path = sys.argv[1] if len(sys.argv) >= 2 else EXAMPLE_PACKAGE

SIMDATA_TYPE = resource_type_by_name('simdata')
STRING_TABLE_TYPE = resource_type_by_name('string_table')
XML_TYPES = [
    0x6017e896,
    0xb61de6b4,
    0xc772e27,
    0xcb5fddc7,
    0xe882d22f,
    0x2d5df13,
    0x2e47a104,
    0x3c1d8799,
    0x3e9d964,
    0x4f739cee,
    0x5b02819e,
    0x6fa49828,
    0x7df2169c,
    0x9c07855f,
    0x28b64675,
    0x339bc5bd,
    0x598f28e7,
    0x904df10,
    0x69453e,
    0xb8bf1a63,
    0xdebafb73,
    0xe4d15fb,
    0xe350dbd8,
    0xec6a8fc6,
    0xee17c6ad,
    0xf401205d,
    0xfa0ffa34,
    0xfbc3aeeb
]

class PackageDumper:
    def dump():
        reader = PackageFileReader(package_path)
        package = reader.parse()

        for (index, record) in zip(package.index_entries, package.records):
            if index.mType == SIMDATA_TYPE:
                reader = SimdataFileReader(None, record)
                simdata = reader.parse()
                PackageDumper.dump_resource('simdata', index, simdata.to_bytearray())

            if index.mType == STRING_TABLE_TYPE:
                reader = StringTableReader(None, record)
                string_table = reader.parse()
                PackageDumper.dump_resource('string_tables', index, string_table.to_bytearray())

            elif index.mType in XML_TYPES:
                parsed = etree.XML(record)

                name = None
                root_elem = parsed.xpath("/I")
                if len(root_elem) == 0: root_elem = parsed.xpath("/Instance")
                if len(root_elem) == 0: root_elem = parsed.xpath("/M")
                if len(root_elem) == 0: root_elem = parsed.xpath("/Module")
                if len(root_elem) == 0: root_elem = parsed.xpath("/ASM")
                if len(root_elem) > 0 and 'n' in root_elem[0].attrib:
                    name = root_elem[0].attrib['n']

                if len(root_elem) > 0 and 'name' in root_elem[0].attrib:
                    name = root_elem[0].attrib['name']

                if name is not None:
                    name = name.replace('/', '-')

                pretty = etree.tostring(parsed, pretty_print=True, xml_declaration=True, encoding='utf-8')
                PackageDumper.dump_resource('xml', index, pretty, extension="xml", name=name)

            else:
                PackageDumper.dump_resource('various', index, record)

    def dump_resource(subdir, index, record, extension = None, name = None):
        filepath = f'./tmp/data/{subdir}/{index.id()}'
        if name is not None: filepath += f"_{name}"
        if extension is not None: filepath += f".{extension}"

        PackageDumper.create_directory_if_needed(filepath)

        with open(filepath, 'w+b') as f:
            f.write(record)

    def create_directory_if_needed(filepath):
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

PackageDumper.dump()
