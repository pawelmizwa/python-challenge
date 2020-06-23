import pytest
from helpers.files_handler import FileHandler
from config import prod
from main import Data


@pytest.fixture(name="file_handler")
def file_handler_fixture():
    file_handler = FileHandler(input_path=prod.input_path,
                               output_path=prod.output_path,
                               nesting_keys=prod.nesting_keys)

    return file_handler


@pytest.fixture(name="data_handler")
def data_fixture():
    data_handler = Data()
    return data_handler


@pytest.fixture(name="file_handler_wrong_input")
def file_handler_wrong_input_fixture():
    file_handler_wrong_input = FileHandler(input_path="wrong_input",
                                           output_path=prod.output_path,
                                           nesting_keys=prod.nesting_keys)

    return file_handler_wrong_input
