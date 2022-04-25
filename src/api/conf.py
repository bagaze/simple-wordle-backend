from fastapi.routing import APIRouter

from src.schemas import Conf
from src.core.deps import todays_word


router = APIRouter()


@router.get(
    "/",
    name="confs:get-conf",
    include_in_schema=False,
    response_model=Conf,
)
@router.get(
    "",
    name="confs:get-conf",
    include_in_schema=True,
    response_model=Conf,
)
def get_conf(
    day_number: int | None = None
) -> Conf:
    word = todays_word(day_number)
    return Conf(number_of_letters=len(word))
