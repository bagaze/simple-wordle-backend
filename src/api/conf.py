from fastapi.routing import APIRouter

from src.core.deps import todays_word
from src.schemas import DayNumber, Conf


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
async def get_conf(
    day_number: DayNumber | None = None
) -> Conf:
    day_num, word = todays_word(day_number)
    return Conf(day_number=day_num, number_of_letters=len(word))
