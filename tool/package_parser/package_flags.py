from .helpers import to_hex

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

    def __str__(self):
        return ("(" +
        f"constantType: {self.constantType}, " +
        f"constantGroup: {self.constantGroup}, " +
        f"constantInstanceEx: {self.constantInstanceEx}, " +
        f"reserved: {self.reserved}, " +
        f"constantTypeId: " + to_hex(self.constantTypeId) + ", " +
        f"constantGroupId: " + to_hex(self.constantGroupId) + ", " +
        f"constantInstanceIdEx: " + to_hex(self.constantInstanceIdEx) +
        ")")
