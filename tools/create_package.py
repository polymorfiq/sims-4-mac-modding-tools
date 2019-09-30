import sys
import os
import re
import binascii
from package_parser import PackageFileWriter

EXAMPLE_SOURCE = './tmp/data'
EXAMPLE_PACKAGE = './tmp/output.package'
source_path = sys.argv[1] if len(sys.argv) >= 2 else EXAMPLE_SOURCE
package_path = sys.argv[2] if len(sys.argv) >= 3 else EXAMPLE_PACKAGE

writer = PackageFileWriter()

for root, subdirs, files in os.walk(source_path):
    for filename in files:
        if filename.starts_with('0x'):
            writer.add_resource_file(f"{root}/{filename}")

package_data = writer.to_bytearray()
with open(package_path, 'w+b') as f:
    f.write(package_data)
