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