import os
import sys
from simdata_parser import SimdataFileReader

EXAMPLE_SIMDATA = './tmp/simdata/0x545ac67a_0x5fdd0c_0xed7000a97ea8f032'

simdata_path = sys.argv[1] if len(sys.argv) >= 2 else EXAMPLE_SIMDATA

reader = SimdataFileReader(simdata_path)
package = reader.parse()
