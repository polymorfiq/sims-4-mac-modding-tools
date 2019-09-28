class PackageFileHeader:
    def __init__(self):
        # Magic Number - Should always = 'DBPF' in .package files
        self.mnFileIdentifier = None
        self.mnFileVersion = None
        self.mnUserVersion = None
        self.unused1 = None

        # Typically not set
        self.mnCreationTime = None

        # Typically not set
        self.mnUpdatedTime = None

        self.unused2 = None
        self.mnIndexRecordEntryCount = None
        self.mnIndexRecordPositionLow = None
        self.mnIndexRecordSize = None
        self.unused3 = None

        # Always 3 for historical purposes
        self.unused4 = None

        self.mnIndexRecordPosition = None
        self.unused5 = None
        self.flags = None

    def __str__(self):
        return ("Package Headers:\n" +
        f"  mnFileIdentifier: {self.mnFileIdentifier}\n" +
        f"  mnFileVersion: {self.mnFileVersion}\n" +
        f"  mnUserVersion: {self.mnUserVersion}\n" +
        f"  unused1: {self.unused1}\n" +
        f"  mnCreationTime: {self.mnCreationTime}\n" +
        f"  mnUpdatedTime: {self.mnUpdatedTime}\n" +
        f"  unused2: {self.unused2}\n" +
        f"  mnIndexRecordEntryCount: {self.mnIndexRecordEntryCount}\n" +
        f"  mnIndexRecordPositionLow: {self.mnIndexRecordPositionLow}\n" +
        f"  mnIndexRecordSize: {self.mnIndexRecordSize}\n" +
        f"  unused3: {self.unused3}\n" +
        f"  unused4: {self.unused4}\n" +
        f"  mnIndexRecordPosition: {self.mnIndexRecordPosition}\n" +
        f"  unused5: {self.unused5}\n" +
        f"  flags: {self.flags}\n")
