from fastapi.routing import APIRouter

from src.schemas import TrialRequest, TrialResponseElem
from src.core.deps import todays_word, compare_words


router = APIRouter()


@router.post(
    "/",
    name="trials:post-trial",
    include_in_schema=False,
    response_model=list[TrialResponseElem],
)
@router.post(
    "",
    name="trials:post-trial",
    include_in_schema=True,
    response_model=list[TrialResponseElem],
)
def post_trial(
    trial_request: TrialRequest
) -> list[TrialResponseElem]:
    return compare_words(
        trial_word=trial_request.word,
        todays_word=todays_word(trial_request.day_number)
    )
