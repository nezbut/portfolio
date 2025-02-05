from pydantic import BaseModel


class GithubData(BaseModel):

    """Schema for GitHub data."""

    public_repos: int
    followers: int
    following: int
