from dotenv import load_dotenv
load_dotenv()

import requests, setup, json, time, atexit

headers = {
    'Host': 'slack.com',
    'Content-type': 'application/json; charset=utf-8',
    'Authorization': 'Bearer ' + setup.USER_OAUTH_TOKEN
}

def get_status(discord_presence_data):
    if discord_presence_data['data']['listening_to_spotify']:
        return ["music", "Listening to " + discord_presence_data['data']['spotify']['song'] + " by " + discord_presence_data['data']['spotify']['artist']]
    else:
        activities = discord_presence_data['data']['activities']
        for activity in activities:
            if activity["name"] == "Visual Studio Code":
                if activity.get("state") is not None and activity.get("details") is not None:
                    return ["code", activity["details"] + " in " + activity["state"]]
                elif activity.get("details") is not None:
                    return ["code", activity["details"]]
                return ["code", "Visual Studio Code - Idle"]
            
            elif activity["name"] == "PyCharm Professional":
                if activity.get("state") is not None and activity.get("details") is not None:
                    return ["pycharm", activity["state"] + " in " + activity["details"]]
                elif activity.get("details") is not None:
                    return ["pycharm", activity["details"]]
                return ["pycharm", "PyCharm Professional - Idle"]
            
            elif activity["name"] == "Android Studio":
                if activity.get("state") is not None and activity.get("details") is not None:
                    return ["android_studio", activity["state"] + " in " + activity["details"]]
                elif activity.get("details") is not None:
                    return ["android_studio", activity["details"]]
                return ["android_studio", "Android Studio - Idle"]
            
            elif activity["name"] == "osu!":
                if activity.get("state") is not None and activity.get("details") is not None:
                    return ["osu", activity["state"] + " - " + activity["details"]]
                elif activity.get("state") is not None:
                    return ["osu", activity["name"] + " - " + activity["state"]]
            
            elif activity["name"] == "Beat Saber":
                if activity.get("state") is not None and activity.get("details") is not None:
                    return ["beat_saber", activity["name"] + ": " + activity["details"] + " [" + activity["state"]  + "]"]
                elif activity.get("details") is not None:
                    return ["beat_saber", activity["name"] + " - " + activity["details"]]
                
            elif activity["name"] == "Visual Studio":
                if activity.get("state") is not None and activity.get("details") is not None:
                    details = activity["details"]
                    if details.startswith("File"):
                        details = details.replace("File", "Editing", 1)
                    elif details == "No active file":
                        return ["vs", "Visual Studio 2022 - Idle"]
                    return ["vs", details + " in " + activity["state"].replace("Solution ", "", 1)]
                return ["vs", "Visual Studio 2022 - Idle"]

        if len(activities) > 0:
            activity = activities[0]
            return ["in_game", "Playing " + activity["name"]]

        return ["default", setup.default_status_message]
    
old_text = None
old_emoji = None

def exit_handler():
    print(f"Please wait while clearing custom status from Slack...")
    requests.post(setup.REQUEST_URL, headers=headers, data=json.dumps({
        'profile': {
            "status_text": "",
            "status_emoji": "",
            "status_expiration": 0
        }
    }))

atexit.register(exit_handler)

while True:
    response = None
    try:
        response = requests.get("https://api.lanyard.rest/v1/users/" + setup.DISCORD_ID).json()
    except requests.ConnectionError as e:
        print(f"Connection error when getting Discord status. Retrying in {setup.REFRESH_INTERVAL} seconds...")
    except requests.Timeout as e:
        print(f"Connection timed out when getting Discord status. Retrying in {setup.REFRESH_INTERVAL} seconds...")

    if response is not None:
        status = get_status(response)
        new_text = status[1]
        new_emoji = setup.emojis[status[0]]
        if new_text != old_text or new_emoji != old_emoji: 
            data = {
                'profile': {
                    "status_text": (new_text[:97] + '...') if len(new_text) > 100 else new_text,
                    "status_emoji": new_emoji,
                    "status_expiration": 0 # never expire
                }   
            }
            print(f"Sending status \"{new_emoji} {new_text}\" to Slack")
            try:
                requests.post(setup.REQUEST_URL, headers=headers, data=json.dumps(data))
            except requests.ConnectionError as e:
                print(f"Connection error when sending status to Slack.")
            except requests.Timeout as e:
                print(f"Connection timed out when sending status to Slack.")
                    
            old_emoji = new_emoji
            old_text = new_text

    time.sleep(setup.REFRESH_INTERVAL)
