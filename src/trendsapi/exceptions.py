"""Exceptions raised by the Trends API client."""


class TrendsAPIError(Exception):
    """Raised when the Trends API returns an error response.

    Attributes:
        status: HTTP status code (e.g. 429, 401, 400).
        code: Machine-readable error code string.
        message: Human-readable error message.
    """

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message

    def __repr__(self) -> str:
        return (
            f"TrendsAPIError(status={self.status}, code={self.code!r}, "
            f"message={self.message!r})"
        )
