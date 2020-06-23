import pytest

nesting_level_input = 1
raw_data_input = []
nested_result = {}


@pytest.mark.parametrize(
    "raw_data, nesting_level, nested",
    [(raw_data_input, nesting_level_input, nested_result)],
)
def test_convert_list_of_dicts_to_nested_dict_empty_raw_data(file_handler, raw_data, nesting_level, nested):
    assert file_handler.convert_list_of_dicts_to_nested_dict(raw_data, nesting_level) == nested


nesting_level_input = 0
raw_data_input = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100
    },
    {
        "country": "US",
        "city": "New York",
        "currency": "USD",
        "amount": 300
    }
]
nested_result = {}


@pytest.mark.parametrize(
    "raw_data, nesting_level, nested",
    [(raw_data_input, nesting_level_input, nested_result)],
)
def test_convert_list_of_dicts_to_nested_dict_nesting_level_0(file_handler, raw_data, nesting_level, nested):
    assert file_handler.convert_list_of_dicts_to_nested_dict(raw_data, nesting_level) == nested


nesting_level_input = 2
raw_data_input = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100
    },
    {
        "country": "FR",
        "city": "Paris",
        "currency": "EUR",
        "amount": 20
    }
]
nested_result = {"USD": {"US": [{"city": "Boston", "amount": 100}]}, "EUR": {"FR": [{"city": "Paris", "amount": 20}]}}


@pytest.mark.parametrize(
    "raw_data, nesting_level, nested",
    [(raw_data_input, nesting_level_input, nested_result)],
)
def test_convert_list_of_dicts_to_nested_dict_nesting_level_2(file_handler, raw_data, nesting_level, nested):
    assert file_handler.convert_list_of_dicts_to_nested_dict(raw_data, nesting_level) == nested


nesting_level_input = 3
raw_data_input = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100
    },
    {
        "country": "US",
        "city": "New York",
        "currency": "USD",
        "amount": 300
    },
    {
        "country": "FR",
        "city": "Paris",
        "currency": "EUR",
        "amount": 20
    }
]
nested_result = {
    "USD": {"US": {"Boston": [{"amount": 100}], "New York": [{"amount": 300}]}},
    "EUR": {"FR": {"Paris": [{"amount": 20}]}}
}


@pytest.mark.parametrize(
    "raw_data, nesting_level, nested",
    [(raw_data_input, nesting_level_input, nested_result)],
)
def test_convert_list_of_dicts_to_nested_dict_nesting_level_3(file_handler, raw_data, nesting_level, nested):
    assert file_handler.convert_list_of_dicts_to_nested_dict(raw_data, nesting_level) == nested


nesting_level_input = 4
raw_data_input = [
    {
        "country": "US",
        "city": "Boston",
        "currency": "USD",
        "amount": 100
    },
    {
        "country": "US",
        "city": "New York",
        "currency": "USD",
        "amount": 300
    }
]
nested_result = {
    "USD": {"US": {"Boston": [{"amount": 100}], "New York": [{"amount": 300}]}}
}


@pytest.mark.parametrize(
    "raw_data, nesting_level, nested",
    [(raw_data_input, nesting_level_input, nested_result)],
)
def test_convert_list_of_dicts_to_nested_dict_nesting_level_4(file_handler, raw_data, nesting_level, nested):
    assert file_handler.convert_list_of_dicts_to_nested_dict(raw_data, nesting_level) == nested
