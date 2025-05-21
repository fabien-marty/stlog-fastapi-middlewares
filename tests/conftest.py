import pytest
import stlog
import io
from stlog.output import StreamOutput
from stlog.formatter import JsonFormatter


@pytest.fixture
def log_output() -> io.StringIO:
    LOG_STREAM = io.StringIO()
    OUTPUT = StreamOutput(formatter=JsonFormatter(), stream=LOG_STREAM)
    stlog.setup(outputs=[OUTPUT], extra_levels={"httpx": "CRITICAL"})
    return LOG_STREAM
