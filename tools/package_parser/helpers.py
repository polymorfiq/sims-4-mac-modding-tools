from .constants import COMPRESSION_TYPES_BY_NAME, RESOURCES_TYPES_BY_NAME

def resource_type_by_name(type_name):
    return RESOURCES_TYPES_BY_NAME.get(type_name, None)

def compression_type_by_name(type_name):
    return COMPRESSION_TYPES_BY_NAME.get(type_name, None)

def pad_bytes_start(curr_bytes, desired_size):
    curr_array = bytearray(curr_bytes)
    while len(curr_array) < desired_size:
        curr_array[:0] = b'\x00'

    return bytes(curr_array)
