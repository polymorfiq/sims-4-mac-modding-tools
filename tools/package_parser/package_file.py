import struct

class PackageFile:
    def __init__(self):
        self.headers = None
        self.index_entries = None
        self.records = None


    def __str__(self):
        my_str = str(self.headers) + "\n\n\n"

        for entry in self.index_entries:
            my_str += str(entry) + "\n\n"

        return my_str
