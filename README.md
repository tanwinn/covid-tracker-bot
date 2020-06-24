[![Coverage Status](https://coveralls.io/repos/github/tanwinn/covid-tracker-bot/badge.svg?branch=thanh)](https://coveralls.io/github/tanwinn/covid-tracker-bot?branch=thanh)

# Covid Tracker Chatbot
Messenger Chatbot powered by [wit.ai](https://github.com/wit-ai/pywit) and Facebook Messenger for [Covid Tracker API](https://github.com/ExpDev07/coronavirus-tracker-api). Submission for [Facebook Wit AI Hackathon 2020](https://devpost.com/software/covid-tracker-bot).

Facebook Messenger Chatbot (InDev): [m.me/CovidTrackerChatbot](https://www.facebook.com/CovidTrackerChatbot/)

Wit.AI ID: 271193027527308

Deployed bot: https://covid-tracker-chatbot.herokuapp.com/ | https://github.com/tanwinn/covid-tracker-bot

Tracking API: https://covid-tracker-us.herokuapp.com/ | https://github.com/ExpDev07/coronavirus-tracker-api

Demo video: https://youtu.be/GWIwydrHSQw

![Chatbot_demo](https://raw.githubusercontent.com/tanwinn/covid-tracker-bot/master/chatbot-demo.png)


## Dev setup

### Requirement
Python 3.8 or higher & PyPI pipenv for venv management

### Getting started

```bash
git clone git@github.com:tanwinn/covid_tracker_bot.git
cd covid-tracker-bot
pipenv shell  # activate venv
pipenv sync --dev # sync the dependencies packages
# Do dev stuff
exit # exit out of the venv
```

### Env configuration

Create a .env file in project root to store the following info
__.env file__
```bash
TRACKER_API=https://covid-tracker-api-chatbot.herokuapp.com/v2
WIT_TOKEN=your_wit_token  # Wit.ai parameters
FB_PAGE_TOKEN=your_page_token  # Messenger API parameters
FB_VERIFY_TOKEN=your_verify_token  # A user secret to verify webhook get request
```
Make sure to reset the pipenv shell to apply the change


### Dev workflow
```bash
pytest
bc fmt # formatting
prospector
```

## Run the App
```bash
uvicorn api.main:APP --reload  # Run the APP
```

## Additional Resources

Pip, Virtual environment & Pipenv: 
- https://realpython.com/what-is-pip/
- https://realpython.com/effective-python-environment/#pipenv 
- https://realpython.com/pipenv-guide/

FastApi: https://fastapi.tiangolo.com/

Facebook Messenger Devhub: 
- https://developers.facebook.com/docs/messenger-platform
- https://developers.facebook.com/docs/messenger-platform/webhook

Wit: 
- https://wit.ai/docs/quickstart
- https://wit.ai/docs/recipes#integrate-with-facebook-messenger

Stackoverflow:
- https://stackoverflow.com/questions/37220796/how-does-facebook-messenger-connect-with-wit-ai-bot-engine
