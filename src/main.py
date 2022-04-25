import uvicorn

from .app import app  # noqa: F401


def __main__():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
