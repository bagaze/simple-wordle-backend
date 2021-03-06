from enum import Enum
from pydantic import BaseModel, constr, conint
from pydantic.types import ConstrainedInt


class DayNumber(ConstrainedInt):
    '''
    Number of the day of the year
    '''
    ge = 1
    le = 365


class TrialRequest(BaseModel):
    '''
    Trial input
    '''
    word: constr(
        min_length=5,
        max_length=10,
        regex='^[a-zA-Z]+$'  # noqa: F722
    )
    day_number: DayNumber | None


class LetterStatusEnum(str, Enum):
    ok = 'ok'
    ko = 'ko'
    present = 'present'


class WordStatusEnum(str, Enum):
    ok = 'ok'
    ko = 'ko'


class TrialResponseElem(BaseModel):
    '''
    Trial response element
    '''
    letter: constr(
        min_length=1,
        max_length=1,
        regex='^[A-Z]+$'  # noqa: F722
    )
    status: LetterStatusEnum


class TrialResponse(BaseModel):
    '''
    Trial response
    '''
    day_number: DayNumber
    status: WordStatusEnum
    results: list[TrialResponseElem]


class Conf(BaseModel):
    '''
    Config of today
    '''
    number_of_letters: conint(ge=5, le=10)
    day_number: DayNumber
