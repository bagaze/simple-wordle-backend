from fastapi.routing import APIRouter

from src.schemas import TrialRequest, TrialResponse
from src.core.deps import todays_word, compare_words


router = APIRouter()


@router.post(
    "/",
    name="trials:post-trial",
    include_in_schema=False,
    response_model=TrialResponse,
)
@router.post(
    "",
    name="trials:post-trial",
    include_in_schema=True,
    response_model=TrialResponse,
)
async def post_trial(
    trial_request: TrialRequest
) -> TrialResponse:
    day_number, word = todays_word(trial_request.day_number)
    status, results = compare_words(
        trial_word=trial_request.word,
        todays_word=word
    )
    return TrialResponse(day_number=day_number, status=status, results=results)
