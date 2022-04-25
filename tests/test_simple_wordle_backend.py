from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src import __version__
from src.schemas import Conf
from src.core.deps import todays_word


class TestGlobal:

    def test_version(self):
        assert __version__ == '0.1.0'

    def test_todays_word(self):
        word = todays_word(1)
        assert word == 'ballerine'


class TestAPIRoutes:

    def test_routes_exists(self, app: FastAPI, client: TestClient) -> None:
        res = client.get(app.url_path_for("confs:get-conf"))
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestAPIConf:

    def test_get_conf(self, app: FastAPI, client: TestClient):
        res = client.get(app.url_path_for("confs:get-conf"))
        assert res.status_code == status.HTTP_200_OK

        conf = Conf(**res.json())
        assert conf.number_of_letters is not None

        res = client.get(app.url_path_for("confs:get-conf"), params={'day_number': 1})
        assert res.status_code == status.HTTP_200_OK

        conf = Conf(**res.json())
        assert conf.number_of_letters == 9
