class UuidException(Exception):
    def __init__(self):
        self.value = "Provide correct uuid"


class ThisIsNotCorrectTokenException(Exception):
    def __init__(self, value: str):
        self.value = f"This is not correct token: {value}"


class TokenExpireException(Exception):
    pass
