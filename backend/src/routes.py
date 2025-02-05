from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.fetcher import DataFetcher
from src.schemas import GithubData

router = APIRouter(prefix="/github", tags=["github"])


@router.get("/")
@inject
async def get_github_info(fetcher: Depends[DataFetcher]) -> GithubData:
    """Get GitHub data."""
    data = await fetcher.fetch_data()
    return GithubData.model_validate(data)
