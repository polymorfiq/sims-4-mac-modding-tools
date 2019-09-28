import struct

class PackageFlags:
    def __init__(self, constantType, constantGroup, constantInstanceEx, reserved):
        self.constantType = constantType
        self.constantGroup = constantGroup
        self.constantInstanceEx = constantInstanceEx
        self.reserved = reserved

        # Set if flags.constantType != 0
        self.constantTypeId = None

        # Set if flags.constantGroup != 0
        self.constantGroupId = None

        # Set if flags.constantInstanceEx != 0
        self.constantInstanceIdEx = None

    def size(self):
        flag_size = 4
        if self.constantType != 0: flag_size += 4
        if self.constantGroup != 0: flag_size += 4
        if self.constantInstanceEx != 0: flag_size += 4

        return flag_size

    def to_bytearray(self):
        raw_data = bytearray([])
        flags = self.constantType | (self.constantGroup << 1) | (self.constantInstanceEx << 2) | (self.reserved << 3)
        raw_data.extend(struct.pack('<I', flags))

        if self.constantType: raw_data.extend(struct.pack('<I', headers.flags.constantTypeId))
        if self.constantGroup: raw_data.extend(struct.pack('<I', headers.flags.constantGroupId))
        if self.constantInstanceEx: raw_data.extend(struct.pack('<I', headers.flags.constantInstanceIdEx))

        return raw_data

    def __str__(self):
        return ("(" +
        f"constantType: {self.constantType}, " +
        f"constantGroup: {self.constantGroup}, " +
        f"constantInstanceEx: {self.constantInstanceEx}, " +
        f"reserved: {self.reserved}, " +
        f"constantTypeId: " + (hex(self.constantTypeId) if self.constantTypeId is not None else 'None') + ", " +
        f"constantGroupId: " + (hex(self.constantGroupId) if self.constantGroupId is not None else 'None') + ", " +
        f"constantInstanceIdEx: " + (hex(self.constantInstanceIdEx) if self.constantInstanceIdEx is not None else 'None') +
        ")")
