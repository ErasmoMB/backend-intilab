from fastapi import HTTPException

class APIException(HTTPException):
    def __init__(self, message, status_code=500, payload=None):
        self.message = message
        self.payload = payload
        super().__init__(status_code=status_code, detail=message)

class ValidationError(HTTPException):
    def __init__(self, message, payload=None):
        super().__init__(status_code=400, detail=message)

class NotFoundError(HTTPException):
    def __init__(self, message="Recurso no encontrado", payload=None):
        super().__init__(status_code=404, detail=message)

class UnauthorizedError(HTTPException):
    def __init__(self, message="No autorizado", payload=None):
        super().__init__(status_code=401, detail=message)

