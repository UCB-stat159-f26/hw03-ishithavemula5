from unittest.mock import patch, Mock
from tennis_career.data import _download_match_data
import pytest
import pandas as pd
import requests

from tennis_career.data import (
    _parse_match_data,
    _calculate_opponent_age,
    _clean_match_data,
)


female_js = """
var morematchmx = [
    ["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC",
     "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R",
     "19770119", "", "USA"],
    ["19970804", "Manhattan Beach", "Hard", "W", "W", "", "", "WC",
     "Q3", "6-3 6-4", "3", "Amanda Basica", "100", "", "", "R",
     "19780620", "", "USA"]
];
"""


def test_parse_female_matches():
    matches = _parse_match_data(female_js)
    assert len(matches) == 2
    assert matches.iloc[0, 11] == "Anne Miller"


def test_female_opponent_age():
    age = _calculate_opponent_age("19951030", "19770119")
    assert age == pytest.approx(18.78, abs=0.1)


def test_clean_female_matches():
    matches = _parse_match_data(female_js)
    cleaned = _clean_match_data(matches, "19810926")
    assert len(cleaned) == 2
    assert "age_diff" in cleaned.columns
    assert cleaned.iloc[0]["result"] == "L"


male_js = """
var morematchmx = [
    ["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC",
     "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "",
     "", "R", "22.264202601", "", "ESP"],
    ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC",
     "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "",
     "Q", "U", "18.7597535934", "", "ESP"]
];
"""


def test_parse_male_matches():
    matches = _parse_match_data(male_js)
    assert len(matches) == 2
    assert matches.iloc[0, 11] == "Guillermo Platel"


def test_male_opponent_age():
    age = _calculate_opponent_age("20010910", "22.264202601")
    assert age == pytest.approx(22.2642, abs=0.001)


def test_clean_male_matches():
    matches = _parse_match_data(male_js)
    cleaned = _clean_match_data(matches, "19860603")
    assert len(cleaned) == 2
    assert cleaned.iloc[0]["result"] == "L"
    assert cleaned.iloc[1]["result"] == "W"
    assert cleaned.iloc[0]["age_diff"] < 0

from tennis_career.data import _format_player_name, _calculate_player_age


def test_empty_player_name():
    with pytest.raises(ValueError, match="valid player name"):
        _format_player_name("")


def test_invalid_player_name_type():
    with pytest.raises(ValueError, match="valid player name"):
        _format_player_name(123)


def test_missing_opponent_age():
    age = _calculate_opponent_age("19951030", "")
    assert pd.isna(age)


def test_invalid_birthdate():
    age = _calculate_player_age("19951030", "invalid")
    assert pd.isna(age)

def test_unknown_player():
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    with patch("tennis_career.data.requests.get", return_value=response):
        with pytest.raises(ValueError, match="Could not find career data"):
            _download_match_data("GastonSanchez")