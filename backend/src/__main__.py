import asyncio
import types
from typing import Optional

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src
from src.di import FetcherProvider
from src.routes import router as github_router

try:
    import uvloop
    uvloop_module: Optional[types.ModuleType] = uvloop
except ImportError:
    uvloop_module = None

loop = uvloop_module.new_event_loop(
) if uvloop_module is not None else asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(
        title="NezbuT Portfolio",
        version=src.__version__,
        description=src.__description__,
        root_path="/api/",
        docs_url="/docs/",
        redoc_url="/redoc/",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )
    app.include_router(github_router)
    container = make_async_container(FetcherProvider())
    setup_dishka(container, app)
    return app
