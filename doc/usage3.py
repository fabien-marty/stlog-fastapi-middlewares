import os
import stlog
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from stlog_fastapi_middlewares import (
    LogContextMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    stlog.setup()
    yield


logger = stlog.getLogger(__name__)
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    LogContextMiddleware,
    logger=logger,
    add_pid=True,
    add_request_id=True,
    envs_to_kvs={"FOO", "foo", "BAR", "bar"},
    headers_to_kvs={"X-Test-Id", "test_id"},
)

# Let's add some environment variables to test the middleware
os.environ["FOO"] = "foo2"
os.environ["BAR"] = "bar2"


@app.get("/")
async def root():
    logger.info("hello world")
    # => this call will output a log with the following extra keys:
    # - foo
    # - bar
    # - pid
    # - request_id
    # - test_id (if the call is made with a X-Test-Id header)
    return {"message": "Hello World"}
