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

class InvalidPlayerFormatExceptin(ResuelveFCError):
    pass

class InvalidDataTypeFormatException(ResuelveFCError):
    pass

class InvalidPlayerFormatException(ResuelveFCError):
    pass
