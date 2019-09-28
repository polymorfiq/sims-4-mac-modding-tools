class PackageVersion:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __str__(self):
        return f"{self.major}.{self.minor}"
