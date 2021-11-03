"""Test covers 1) output or 2) control flow"""
import pytest
import requests


def compose_earnest_text():
    json_response = requests.get(f"https://randomuser.me/api/").json()  # IO
    (result,) = json_response["results"]
    if result.get("gender") != "female":
        return
    else:
        print("=== See Text Below ===")  # IO
        print(f'Hey {result["name"]["first"]}, will you date geeks?')  # IO


"""Sample Structure of a Unit Test

# @fixtures (setup and teardown)
def test_<function_name>_<two_of_the_Ws>([mocks], [fixture]):
    # mocks
    # <function_name> is called
    # assertions (input/ouput, control flow)
"""


# output + actual requests
def test1_compose_earnest_text_return_none():
    assert compose_earnest_text() == None
    # return 'result was male'


# output + mocked requests + female returns none
def test2_compose_earnest_text_returns_string_if_male(mocker):
    mock_get = mocker.patch("requests.get", autospec=True)
    mock_get.return_value.json.return_value = {"results": [{"gender": "male"}]}
    assert compose_earnest_text() == None


# output + control flow (result is male)
def test3_compose_earnest_never_prints_for_male(mocker):
    mock_print = mocker.patch("builtins.print")
    mock_get = mocker.patch("requests.get", autospec=True)
    mock_get.return_value.json.return_value = {
        "results": [{"gender": "male", "name": {"first": "Jay"}}]  # female
    }
    assert compose_earnest_text() == None
    mock_print.assert_not_called()

# output + control flow (result is female)
def test4_compose_earnest_text_prints_for_female(mocker):
    mock_print = mocker.patch("builtins.print")
    mock_get = mocker.patch("requests.get", autospec=True)
    mock_get.return_value.json.return_value = {
        "results": [{"gender": "female", "name": {"first": "Sara"}}]
    }
    assert compose_earnest_text() == None
    assert mock_print.call_args_list == [
        mocker.call("=== See Text Below ==="),
        mocker.call("Hey Sara, will you date geeks?"),
    ]


@pytest.fixture()
def mock_request_and_print(mocker):
    mock_print = mocker.patch("builtins.print")
    mock_get = mocker.patch("requests.get", autospec=True)
    return mock_get, mock_print


def test5_compose_earnest_text_prints_for_female(mocker, mock_request_and_print):
    request_user, any_print_calls = mock_request_and_print
    request_user.return_value.json.return_value = {
        "results": [{"gender": "female", "name": {"first": "FemaleName!"}}]
    }
    assert compose_earnest_text() == None
    assert any_print_calls.call_args_list == [
        mocker.call("=== See Text Below ==="),
        mocker.call("Hey FemaleName!, will you date geeks?"),
    ]

# control flow only for no male condition
def test6_compose_earnest_text_never_prints_for_male(mock_request_and_print):
    request_user, any_print_calls = mock_request_and_print
    request_user.return_value.json.return_value = {"results": [{"gender": "male"}]}
    compose_earnest_text()  # remove redundant assertion for return
    any_print_calls.assert_not_called()




