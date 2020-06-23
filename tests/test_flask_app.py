import unittest
from main import app
import base64
from config import prod
import pytest

nesting_level_input = "wrong_input"


def test_get_nesting_level_wrong_input(data_handler):
    with pytest.raises(ValueError):
        assert data_handler.get_nesting_level(nesting_level_input)


nesting_level_i = "nesting_level_0"
level_result = 0


@pytest.mark.parametrize(
    "nesting_level, result", [(nesting_level_i, level_result)],
)
def test_get_nesting_level_example_level(data_handler, nesting_level, result):
    assert data_handler.get_nesting_level(nesting_level) == result


def test_get_data_from_file_wrong_input(file_handler_wrong_input):
    with pytest.raises(FileNotFoundError):
        assert file_handler_wrong_input.get_data_from_file()


class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    @staticmethod
    def get_correct_auth_header():
        message_bytes = (prod.local_user + ":" + prod.local_password).encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        headers = {"Authorization": f"Basic {base64_message}"}
        return headers

    def post_data_specified_level(self, level):
        return self.app.post(
            f"/data?nesting_level=nesting_level_{level}",
            headers=self.get_correct_auth_header(),
        )

    def post_data_incorrect_auth_header(self):
        message_bytes = (prod.local_user + ":" + prod.local_password + "wrong").encode(
            "ascii"
        )
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        headers = {"Authorization": f"Basic {base64_message}"}
        return self.app.post(f"/data?nesting_level=test", headers=headers)

    def post_data(self):
        return self.app.post(f"/data", headers=self.get_correct_auth_header())

    def get_data(self):
        return self.app.post(f"/data", headers=self.get_correct_auth_header())

    def test_incorrect_auth(self):
        response = self.post_data_incorrect_auth_header()
        self.assertEqual(response.status_code, 401)

    def test_no_query_params_post(self):
        response = self.post_data()
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'{"message":"Please specify nesting_level in params"}', response.data
        )

    def test_post_data_with_wrong_level(self):
        response = self.post_data_specified_level("wrong_level")
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'{"message":"Please provide nesting level in correct format"}',
            response.data,
        )

    def test_get_data_not_handled_method(self):
        response = self.get_data()
        self.assertEqual(response.status_code, 405)
        self.assertIn(
            b'{"message":"The method is not allowed for the requested URL."}',
            response.data,
        )
