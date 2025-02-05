from types import TracebackType
from typing import Any, Optional, Protocol

from httpx import AsyncClient, codes


class DataFetcher(Protocol):

    """Interface for fetching data from an external source."""

    async def fetch_data(self) -> dict[str, Any]:
        """
        Fetches data from an external source.

        :return: A dictionary containing the fetched data.
        """
        ...


class GithubDataFetcher:

    """Fetches data from the GitHub API."""

    def __init__(self, username: str) -> None:
        self.username = username
        self._url = f"https://api.github.com/users/{self.username}"
        self._client: AsyncClient

    async def __aenter__(self) -> DataFetcher:
        """Async context manager entry point."""
        self._client = AsyncClient()
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type: Optional[type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        """Async context manager exit point."""
        await self._client.__aexit__(exc_type, exc_value, traceback)
        await self._client.aclose()

    async def fetch_data(self) -> dict[str, Any]:
        """
        Fetches data from an external source.

        :return: A dictionary containing the fetched data.
        """
        response = await self._client.get(self._url)
        if response.status_code != codes.OK:
            return {}
        data: dict[str, Any] = response.json()
        return data
