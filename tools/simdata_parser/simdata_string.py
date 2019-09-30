class SimdataString:
    def __init__(self, position, contents):
        self.position = position
        self.contents = contents

    def to_bytearray(self):
        return self.contents.encode('ascii')
