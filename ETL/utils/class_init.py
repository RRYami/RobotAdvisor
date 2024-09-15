class InitClass:
    """
    Class representing an initialization class.
    Attributes:
        api_key (str): The API key.
        tickers (list[str]): The list of tickers.
    Methods:
        __str__(): Returns a string representation of the class.
        __repr__(): Returns a string representation of the class.
        __init__(): Initializes the class.
    """

    def __str__(self) -> str:
        return f"InitClass({self.api_key!r}, {self.tickers!r})"

    def __repr__(self) -> str:
        return f"InitClass({self.api_key!r}, {self.tickers!r})"

    def __init__(self):
        self._api_key = ""
        self._tikers = []

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        if not value:
            raise ValueError("No API key provided")
        self._api_key = value

    @property
    def tickers(self) -> list[str]:
        return self._tikers

    @tickers.setter
    def tickers(self, value: list[str]) -> None:
        if len(value) == 0:
            raise ValueError("No tickers provided")
        self._tikers = value
