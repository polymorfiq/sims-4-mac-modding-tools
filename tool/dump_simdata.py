import os
import sys
from package_parser import PackageFileReader
from package_parser import resource_type_by_name

EXAMPLE_PACKAGE = '../Documentation/TS4_Custom_Content_Guide/Examples/simsmodsquad-novelist.package'

package_path = sys.argv[1] if len(sys.argv) >= 2 else EXAMPLE_PACKAGE

SIMDATA_TYPE = resource_type_by_name('simdata')

class SimdataDumper:
    def dump():
        reader = PackageFileReader(package_path)
        package = reader.parse()

        for (index, record) in zip(package.index_entries, package.records):
            if index.mType == SIMDATA_TYPE: SimdataDumper.dump_simdata(index, record)

    def dump_simdata(index, record):
        filepath = f'./tmp/simdata/{index.id()}'
        SimdataDumper.create_directory_if_needed(filepath)

        with open(filepath, 'w+b') as f:
            f.write(record)

    def create_directory_if_needed(filepath):
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

SimdataDumper.dump()
