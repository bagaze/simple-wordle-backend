from enum import Enum
from pydantic import BaseModel, constr, conint


class TrialRequest(BaseModel):
    '''
    Trial input
    '''
    word: constr(min_length=5, max_length=10)


class StatusEnum(str, Enum):
    ok = 'ok'
    ko = 'ko'
    present = 'present'


class TrialWordcheckResponse(BaseModel):
    '''
    Trial Response
    '''
    letter: constr(min_length=1, max_length=1)
    status: StatusEnum


class Conf(BaseModel):
    '''
    Config of today
    '''
    number_of_letters: conint(ge=5, le=10)
