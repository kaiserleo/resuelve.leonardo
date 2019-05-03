class ResuelveFCError(Exception):
    """Base class for other exceptions"""
    pass

class LevelNotFoundException(ResuelveFCError):
    pass

class ZeroPlayersReceivedException(ResuelveFCError):
    pass

class MissingFieldsException(ResuelveFCError):
    pass

class NonValidFieldsException(ResuelveFCError):
    pass

class ArrayExpectedException(ResuelveFCError):
    pass

class InvalidPlayerFormatException(ResuelveFCError):
    pass

class InvalidDataTypeFormatException(ResuelveFCError):
    pass

class InvalidPlayerFormatException(ResuelveFCError):
    pass

class InvalidRangeNumberException(ResuelveFCError):
    pass

class JSONDecodeException(ResuelveFCError):
    pass
