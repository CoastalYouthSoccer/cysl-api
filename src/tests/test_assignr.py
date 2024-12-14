import pytest
from unittest.mock import patch, MagicMock
from app.assignr.assignr import Assignr, get_match_count, get_referees, get_game_information

@pytest.fixture
def mock_payload():
    return {
        "id": "123",
        "localized_date": "2023-10-05",
        "localized_time": "10:00 AM",
        "start_time": "9:55 AM",
        "home_team": "Team A",
        "away_team": "Team B",
        "age_group": "U10",
        "league": "Youth League",
        "venue": "Field A",
        "gender": "Mixed",
        "subvenue": "Field A - Section 1",
        "game_type": "League",
        ".officials.0.name": "Referee A",
        ".officials.0.position": "Referee",
    }

@pytest.fixture
def mock_assignr():
    return Assignr(
        client_id="test_client_id",
        client_secret="test_client_secret",
        client_scope="test_scope",
        base_url="https://api.example.com",
        auth_url="https://auth.example.com"
    )

def test_get_match_count(mock_payload):
    pattern = r'\.officials\.\d+\.position'
    count = get_match_count(mock_payload, pattern)
    assert count == 1

def test_get_referees(mock_payload):
    referees = get_referees(mock_payload)
    assert len(referees) == 3
    assert referees[0]["name"] == "Referee A"
    assert referees[0]["position"] == "Referee"
    assert referees[1]["name"] == "Not Assigned"
    assert referees[1]["position"] == "Asst. Referee"

def test_get_game_information(mock_payload):
    game_info = get_game_information(mock_payload)
    assert game_info["id"] == "123"
    assert game_info["home_team"] == "Team A"
    assert game_info["away_team"] == "Team B"


@patch("app.assignr.assignr.requests.post")
def test_authenticate(mock_post, mock_assignr):
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_post.return_value = mock_response

    mock_assignr.authenticate()
    assert mock_assignr.token == "test_token"

#@patch("app.assignr.assignr.requests.get")
#def test_get_site_id(mock_get, mock_assignr):
#    mock_response = MagicMock()
#    mock_response.json.return_value = {
#    "page": {
#        "records": 1,
#        "pages": 1,
#        "current_page": 1,
#        "limit": 50
#    },
#    "_embedded": {
#        "sites": [
#            {
#                "id": 100,
#                "name": "Some Site",
#                "show_game_requests": "false",
#                "show_unassigned_games": "true",
#                "show_all_games": "false",
#                "show_game_reports": "true",
#                "forms_enabled": "true",
#                "sports": [
#                    "soccer"
#                ]
#            }
#        ]
#    }
#}
#    mock_get.return_value = mock_response
#    mock_assignr.token = "some_token"
#    mock_assignr.get_site_id()
#    assert mock_assignr.site_id == 100
#
#@patch("app.assignr.assignr.requests.get")
#def test_get_venues(mock_get, mock_assignr):
#    mock_response = MagicMock()
#    mock_response.json.return_value = {
#        "page": {"pages": 1},
#        "_embedded": {"venues": [{"id": "1", "name": "Field A", "city": "City A"}]}
#    }
#    mock_get.return_value = mock_response
#
#    venues = mock_assignr.get_venues()
#    assert len(venues) == 1
#    assert venues[0]["name"] == "Field A"
#
#@patch("app.assignr.assignr.requests.get")
#def test_get_games_venue(mock_get, mock_assignr, mock_payload):
#    mock_response = MagicMock()
#    mock_response.json.return_value = {
#        "page": {"pages": 1},
#        "_embedded": {"games": [mock_payload]}
#    }
#    mock_get.return_value = mock_response
#
#    games = mock_assignr.get_games_venue("2023-10-01", "2023-10-10", "Field A")
#    assert "Field A - Section 1" in games
#    assert "10:00 AM" in games["Field A - Section 1"]
#    assert games["Field A - Section 1"]["10:00 AM"]["home_team"] == "Team A"
#