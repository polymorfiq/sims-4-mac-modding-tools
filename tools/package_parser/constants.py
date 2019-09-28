MAGIC_NUMBER = 'DBPF'

COMPRESSION_TYPES = {
    0x0000: "Uncompressed",
    0xfffe: "Streamable compression",
    0xffff: "Internal compression",
    0xffe0: "Deleted record",
    0x5a42: "ZLIB"
}

COMPRESSION_TYPES_BY_NAME = {
    "Uncompressed": 0x0000,
    "Streamable compression": 0xfffe,
    "Internal compression": 0xffff,
    "Deleted record": 0xffe0,
    "ZLIB": 0x5a42
}

RESOURCE_TYPES = {
    0x034aeecb: "Create a Sim (CAS) Catalog Instance",
    0x545ac67a: "Simdata",
    0x738e6c56: "Topic"
}

RESOURCES_TYPES_BY_NAME = {
    "cas_catalog_instance": 0x034aeecb,
    "simdata": 0x545ac67a,
    "topic": 0x738e6c56
}
