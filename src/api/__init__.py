from fastapi.routing import APIRouter

from . import conf, trial


api_router = APIRouter()
api_router.include_router(conf.router, prefix="/conf", tags=["config"])
api_router.include_router(trial.router, prefix="/trial", tags=["config"])
