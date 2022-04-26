from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest

from src import __version__
from src.core.deps import todays_word
from src.schemas import Conf, StatusEnum, TrialResponseElem


class TestGlobal:

    def test_version(self):
        assert __version__ == '0.1.0'

    def test_todays_word(self):
        _, word = todays_word(2)
        assert word == 'ballerine'


class TestAPIRoutes:

    def test_routes_exists(self, app: FastAPI, client: TestClient) -> None:
        res = client.get(app.url_path_for("confs:get-conf"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = client.post(app.url_path_for("trials:post-trial"), json={'word': 'test'})
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestAPIConf:

    def test_get_conf(self, app: FastAPI, client: TestClient):
        res = client.get(app.url_path_for("confs:get-conf"))
        assert res.status_code == status.HTTP_200_OK

        conf = Conf(**res.json())
        assert conf.number_of_letters is not None
        assert conf.day_number is not None

        res = client.get(app.url_path_for("confs:get-conf"), params={'day_number': 2})
        assert res.status_code == status.HTTP_200_OK

        conf = Conf(**res.json())
        assert conf.number_of_letters == 9
        assert conf.day_number == 2


class TestAPITrial:

    @pytest.mark.parametrize(
        "trial_word, first_letter_status, last_letter_status",
        (
            ("ballerine", StatusEnum.ok, StatusEnum.ok),
            ("ballerina", StatusEnum.ok, StatusEnum.ko),
            ("calleriny", StatusEnum.ko, StatusEnum.ko),
            ("acllaeinr", StatusEnum.present, StatusEnum.present)
        ),
    )
    def test_post_trial(
        self,
        app: FastAPI,
        client: TestClient,
        trial_word: str,
        first_letter_status: str,
        last_letter_status: str
    ):
        res = client.post(
            app.url_path_for("trials:post-trial"),
            json={'word': trial_word, 'day_number': 2}
        )
        assert res.status_code == status.HTTP_200_OK

        first_letter_checked = TrialResponseElem(**(res.json()[0]))
        last_letter_checked = TrialResponseElem(**(res.json()[-1]))

        assert first_letter_checked.letter == trial_word[0]
        assert last_letter_checked.letter == trial_word[-1]
        assert first_letter_checked.status == first_letter_status
        assert last_letter_checked.status == last_letter_status

    @pytest.mark.parametrize(
        "trial_word, status_",
        (
            ("ballerine", status.HTTP_200_OK),
            ("balle", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("ballerinette", status.HTTP_422_UNPROCESSABLE_ENTITY)
        ),
    )
    def test_post_trial_error(
        self,
        app: FastAPI,
        client: TestClient,
        trial_word: str,
        status_: int
    ):
        res = client.post(
            app.url_path_for("trials:post-trial"),
            json={'word': trial_word, 'day_number': 2}
        )
        assert res.status_code == status_
