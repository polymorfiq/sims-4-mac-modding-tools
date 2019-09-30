class StringTableFile:
    def __init__(self):
        self.headers = None
        self.strings = []

    def to_bytearray(self):
        byte_data = bytearray([])

        byte_data.extend(self.headers.to_bytearray())
        for string in self.strings:
            byte_data.extend(string.to_bytearray())

        return byte_data
