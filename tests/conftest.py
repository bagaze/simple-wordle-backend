import pytest
import os


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session", autouse=True)
def session_config():
    os.environ["TESTING"] = "1"
