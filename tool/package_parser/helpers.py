from .constants import RESOURCES_TYPES_BY_NAME

def to_hex(num):
    return 'None' if num is None else "0x{:02x}".format(num)

def resource_type_by_name(type_name):
    return RESOURCES_TYPES_BY_NAME.get(type_name, None)
