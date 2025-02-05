import os
from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from src.fetcher import DataFetcher, GithubDataFetcher


class FetcherProvider(Provider):

    """A provider for DataFetcher instances."""

    @provide(scope=Scope.APP)
    async def get_fetcher(self) -> AsyncIterable[DataFetcher]:
        """Provides a DataFetcher instance."""
        username = os.getenv("GITHUB_USERNAME", "nezbut")
        async with GithubDataFetcher(username) as fetcher:
            yield fetcher
