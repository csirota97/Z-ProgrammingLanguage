class OpenGiving(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnexpectedPeriod(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)