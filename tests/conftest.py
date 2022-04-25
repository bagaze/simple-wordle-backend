import pytest
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient

from typing import Generator


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session", autouse=True)
def session_config():
    os.environ["TESTING"] = "1"


# Create a new application for testing
@pytest.fixture
def app() -> FastAPI:
    from src.app import get_application
    return get_application()


# Make requests in our tests
@pytest.fixture
def client(app: FastAPI) -> Generator:
    with TestClient(app) as c:
        yield c
