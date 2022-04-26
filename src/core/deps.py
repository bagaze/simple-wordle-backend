from datetime import datetime
from fastapi import status as http_status
from fastapi.exceptions import HTTPException

from src.schemas import LetterStatusEnum, WordStatusEnum, TrialResponseElem

WORDS_FPATH = './src/data/words.txt'


def todays_word(day: int | None = None) -> str:
    with open(WORDS_FPATH, 'r') as f:
        word_list = [word.rstrip('\n') for word in f]
        day_num = day if day else datetime.now().timetuple().tm_yday

        return (day_num, word_list[day_num % len(word_list) - 1])


def compare_words(*, trial_word: str, todays_word: str) -> list[TrialResponseElem]:
    # First, raise an error of the length of words does not match
    if (len(trial_word) != len(todays_word)):
        raise HTTPException(
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Length of words does not match'
        )

    # Then check for every letter if the position is correct
    remaining_letters = [char.upper() for char in todays_word]
    res: list[TrialResponseElem] = []
    for (idx, letter) in enumerate(trial_word):
        if letter.upper() == todays_word[idx].upper():
            res.append(TrialResponseElem(letter=letter, status=LetterStatusEnum.ok))
            remaining_letters[idx] = ''
        else:
            res.append(TrialResponseElem(letter=letter, status=LetterStatusEnum.ko))

    # For remaining letters, check if there are present in the remaining letters
    for el in filter(
        lambda el: el.status == LetterStatusEnum.ko,
        res
    ):
        try:
            idx = remaining_letters.index(el.letter.upper())
            remaining_letters[idx] = ''
            el.status = LetterStatusEnum.present
        except ValueError:
            pass

    status = all(el.status == LetterStatusEnum.ok for el in res)
    status = WordStatusEnum.ok if status else WordStatusEnum.ko

    return status, res
