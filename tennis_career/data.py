import json
import re
import pandas as pd
import requests

def _format_player_name(player_name):
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Please enter a valid player name.")

    name = player_name.strip()
    if " " in name:
        return "".join(word.capitalize() for word in name.split())

    return name[0].upper() + name[1:]

def _download_match_data(player_name):
    formatted_name = _format_player_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{formatted_name}Career.js"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.HTTPError as error:
        raise ValueError(
            f"Could not find career data for '{player_name}'. "
            "Please check the player's name."
        ) from error
    except requests.RequestException as error:
        raise ConnectionError(
            "Could not connect to Tennis Abstract. Please try again."
        ) from error

    return response.text

def _parse_match_data(js_text):
    match = re.search(r"var\s+morematchmx\s*=\s*(\[[\s\S]*?\])\s*;", js_text)
    if not match:
        raise ValueError("Could not find match data in the JavaScript file.")

    matches = json.loads(match.group(1))
    return pd.DataFrame(matches)

def _calculate_opponent_age(match_date, opponent):
    if pd.isna(opponent) or opponent == "":
        return float("nan")

    value = str(opponent)
    if len(value) == 8 and value.isdigit():
        birthdate = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        match_date = pd.to_datetime(str(match_date), format="%Y%m%d", errors="coerce")
        if pd.isna(birthdate) or pd.isna(match_date):
            return float("nan")
        return (match_date - birthdate).days / 365.25

    return pd.to_numeric(value, errors="coerce")

def _calculate_player_age(match_date, birthdate):
    match_date = pd.to_datetime(str(match_date), format="%Y%m%d", errors="coerce")
    birthdate = pd.to_datetime(str(birthdate), format="%Y%m%d", errors="coerce")

    if pd.isna(match_date) or pd.isna(birthdate):
        return float("nan")

    return (match_date - birthdate).days / 365.25

def _get_player_birthdate(player_name):
    name = _format_player_name(player_name)
    for player_type in ["wplayer", "player"]:
        url = f"https://www.tennisabstract.com/cgi-bin/{player_type}.cgi"
        response = requests.get(url, params={"p": name}, timeout=15)
        response.raise_for_status()
        match = re.search(r"var\s+dob\s*=\s*['\"]?(\d{8})", response.text)
        if match:
            return match.group(1)

    raise ValueError(f"Could not find birthdate for '{player_name}'.")


def _clean_match_data(matches, birthdate):
    df = matches[[0, 4, 11, 16]].copy()
    df.columns = ["match_date", "result", "opponent", "opponent_info"]
    df["player_age"] = df["match_date"].apply(
        lambda date: _calculate_player_age(date, birthdate))
    df["opponent_age"] = df.apply(
        lambda row: _calculate_opponent_age(row["match_date"], row["opponent_info"]),
        axis=1)
    df["age_diff"] = df["player_age"] - df["opponent_age"]
    df = df[df["result"].isin(["W", "L"])]
    df = df.dropna(subset=["player_age", "opponent_age", "age_diff"])
    return df[["match_date", "opponent", "player_age", "opponent_age", "age_diff", "result"]]

def get_player_matches(player_name):
    js_text = _download_match_data(player_name)
    matches = _parse_match_data(js_text)
    birthdate = _get_player_birthdate(player_name)
    return _clean_match_data(matches, birthdate)

