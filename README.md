# slack status updates ⚡️
### updates your slack status based on your discord rich presence using the data from the lanyard service

#### setup:
1) Join the [lanyard discord server](https://discord.gg/WScAm7vNGF) - this will expose your discord presence to a restful api which the bot will use to fetch your activity data
2) Create a new slack application and give it access to the ```users.profile:write``` scope - this will give the bot the permission to update your profile, which includes your status
3) Create a copy of `.env.example` and name it `.env`
4) In `.env` file, update:
   1) `USER_OAUTH_TOKEN` with your **Bot User OAuth Token** - this is given by Slack when you create a new application
   2) `DISCORD_ID` field with your discord id (don't confuse this with your username)
   3) OPTIONAL: `REFRESH_INTERVAL` to what you would like (in seconds)
5) the only changes you will need to make in the code are to the [setup.py](setup.py) file:
   1) update ```emojis``` with valid slack emoji ids (e.x. `:smile:`) for all of the fields (`default`, `code`, `pycharm`, `osu`, `music` or it will not work. Right now it only supports these, but more may be added later.
   2) update ```default_status_message``` with what you want your status to be when there are no activities in your discord presence
    
