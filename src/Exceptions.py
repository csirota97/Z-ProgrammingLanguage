class OpenGiving(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnexpectedPeriod(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnknownValue(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnknownFunction(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class EvaluationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BadNameError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MissingParametersError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnterminatedQuoteError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
