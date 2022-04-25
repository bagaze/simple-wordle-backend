

from datetime import datetime


WORDS_FPATH = './src/data/words.txt'


def todays_word(day=None):
    with open(WORDS_FPATH, 'r') as f:
        word_list = [word.rstrip('\n') for word in f]
        day_num = day if day else datetime.now().timetuple().tm_yday

        return word_list[day_num % len(word_list)]
