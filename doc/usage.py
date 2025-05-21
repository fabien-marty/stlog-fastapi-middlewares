import stlog
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from stlog_fastapi_middlewares import (
    AccessLogMiddleware,
    CustomExceptionHandlingMiddleware,
    LogContextMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    stlog.setup()
    yield


logger = stlog.getLogger(__name__)
app = FastAPI(lifespan=lifespan)
app.add_middleware(CustomExceptionHandlingMiddleware, logger=logger)
app.add_middleware(AccessLogMiddleware, logger=logger)
app.add_middleware(LogContextMiddleware, logger=logger)


@app.get("/")
async def root():
    return {"message": "Hello World"}
