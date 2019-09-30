class SimdataTableData:
    def __init__(self):
        self.rows = []

    def to_bytearray(self):
        byte_data = bytearray([])

        for row in self.rows:
            byte_data.extend(row.to_bytearray())

        return byte_data
