COMPRESSION_TYPES = {
    0x0000: "Uncompressed",
    0xfffe: "Streamable compression",
    0xffff: "Internal compression",
    0xffe0: "Deleted record",
    0x5a42: "ZLIB"
}

RESOURCE_TYPES = {
    0x034aeecb: "Create a Sim (CAS) Catalog Instance",
    0x545ac67a: "Simdata"
}

RESOURCES_TYPES_BY_NAME = {
    "cas_catalog_instance": 0x034aeecb,
    "simdata": 0x545ac67a
}
