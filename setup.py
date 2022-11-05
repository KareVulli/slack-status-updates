import os

USER_OAUTH_TOKEN = os.environ.get("USER_OAUTH_TOKEN")
REQUEST_URL = "https://slack.com/api/users.profile.set"
DISCORD_ID = os.environ.get("DISCORD_ID")
REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL")) # in seconds

emojis = {
    "music": ":musical_note:",
    "code": ":vscode:",
    "pycharm": ":pycharm:",
    "osu": ":osu:",
    "beat_saber": ":crossed_swords:",
    "in_game": ":video_game:",
    "default": ""
}

default_status_message = ""
