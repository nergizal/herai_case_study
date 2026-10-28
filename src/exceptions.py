class DeviceAnalysisError(Exception):
    pass

class FileFormatError(DeviceAnalysisError):
    pass

class SchemaValidationError(DeviceAnalysisError):
    pass

class InvalidDataContentError(DeviceAnalysisError):
    pass

class APICommunicationError(DeviceAnalysisError, RuntimeError):
    pass