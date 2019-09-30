
ALL_TYPES = [
    'BOOL',
    'CHAR8',
    'INT8',
    'UINT8',
    'INT16',
    'UINT16',
    'INT32',
    'UINT32',
    'INT64',
    'UINT64',
    'FLOAT',
    'STRING8',
    'HASHEDSTRING8',
    'OBJECT',
    'VECTOR',
    'FLOAT2',
    'FLOAT3',
    'FLOAT4',
    'TABLESETREFERENCE',
    'RESOURCEKEY',
    'LOCKEY',
    'UNDEFINED'
]

TYPE_ALIGNMENTS = {
    'BOOL': 1,
    'CHAR8': 1,
    'INT8': 1,
    'UINT8': 1,
    'INT16': 2,
    'UINT16': 2,
    'INT32': 4,
    'UINT32': 4,
    'INT64': 8,
    'UINT64': 8,
    'FLOAT': 4,
    'STRING8': 4,
    'HASHEDSTRING8': 4,
    'OBJECT': 4,
    'VECTOR': 4,
    'FLOAT2': 4,
    'FLOAT3': 4,
    'FLOAT4': 4,
    'TABLESETREFERENCE': 8,
    'RESOURCEKEY': 8,
    'LOCKEY': 4,
    'UNDEFINED': 1
}

TYPE_UNPACKS = {
    'BOOL': '<?',
    'CHAR8': '<c',
    'INT8': '<b',
    'UINT8': '<B',
    'INT16': '<h',
    'UINT16': '<H',
    'INT32': '<i',
    'UINT32': '<I',
    'INT64': '<q',
    'UINT64': '<Q',
    'FLOAT': '<f',
    'STRING8': '<cccc',
    'HASHEDSTRING8': '<cccc',
    'OBJECT': '<cccc',
    'VECTOR': '<bbbb',
    'FLOAT2': '<f',
    'FLOAT3': '<f',
    'FLOAT4': '<f',
    'TABLESETREFERENCE': '<BBBBBBBB',
    'RESOURCEKEY': '<BBBBBBBB',
    'LOCKEY': '<BBBB',
    'UNDEFINED': '<c'
}

def alignment_for_type(data_type):
    if data_type < len(ALL_TYPES):
        return TYPE_ALIGNMENTS.get(ALL_TYPES[data_type])
    else:
        return 1

def unpack_for_type(data_type):
    return TYPE_UNPACKS.get(ALL_TYPES[data_type])
