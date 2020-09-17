class InvalidConsoleLogPathError(Exception):
    """Raised when an invalid path was specified in the path.dat."""

    def __init__(self, path, message):
        self.path = path
        self.message = message


class NoPathFileError(Exception):
    """Raised when path.dat could not be found."""

    def __init__(self, expected_path, message):
        self.expected_path = expected_path
        self.message = message
