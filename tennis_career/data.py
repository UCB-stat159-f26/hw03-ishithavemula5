def _format_player_name(player_name):
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("Please enter a valid player name.")

    name = player_name.strip()
    if " " in name:
        return "".join(word.capitalize() for word in name.split())

    return name[0].upper() + name[1:]
