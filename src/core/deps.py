from datetime import datetime
from fastapi import status
from fastapi.exceptions import HTTPException

from src.schemas import StatusEnum, TrialResponseElem

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
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Length of words does not match'
        )

    # Then check for every letter if the position is correct
    remaining_letters = [char.upper() for char in todays_word]
    res: list[TrialResponseElem] = []
    for (idx, letter) in enumerate(trial_word):
        if letter.upper() == todays_word[idx].upper():
            res.append(TrialResponseElem(letter=letter, status=StatusEnum.ok))
            remaining_letters[idx] = ''
        else:
            res.append(TrialResponseElem(letter=letter, status=StatusEnum.ko))

    # For remaining letters, check if there are present in the remaining letters
    for el in filter(
        lambda el: el.status == StatusEnum.ko,
        res
    ):
        try:
            idx = remaining_letters.index(el.letter.upper())
            remaining_letters[idx] = ''
            el.status = StatusEnum.present
        except ValueError:
            pass

    return res
