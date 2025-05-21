import stlog
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from stlog_fastapi_middlewares import (
    CustomExceptionHandlingMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    stlog.setup()
    yield


logger = stlog.getLogger(__name__)
app = FastAPI(lifespan=lifespan)
app.add_middleware(CustomExceptionHandlingMiddleware, logger=logger)


@app.get("/exception")
async def exception():
    raise Exception("test")
