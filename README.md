[![Coverage Status](https://coveralls.io/repos/github/tanwinn/covid-tracker-bot/badge.svg?branch=master)](https://coveralls.io/github/tanwinn/covid-tracker-bot?branch=master)

# Covid Tracker Chatbot
Testdrive Chatbot powered by [wit.ai](https://github.com/wit-ai/pywit) and Facebook Messenger for Covid tracker ([deployed API](https://covid-tracker-us.herokuapp.com/))

Deployed: https://covid-tracker-chatbot.herokuapp.com/

GitHub: https://github.com/tanwinn/covid-tracker-bot

Submission for [Facebook Messaging Hackathon](https://fbmessaging2.devpost.com/?ref_content=default&ref_feature=challenge&ref_medium=portfolio) & [AI hackathon](https://fbai2.devpost.com/?ref_content=default&ref_feature=challenge&ref_medium=portfolio)

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
WIT_TOKEN=your_wit_token  # Wit.ai parameters
FB_PAGE_TOKEN=your_page_token  # Messenger API parameters
FB_VERIFY_TOKEN=your_verify_token  # A user secret to verify webhook get request
```
Make sure to reset the pipenv shell to apply the change


### Dev workflow
```bash
pytest
bc fmt # formatting
prospector # linting TODO: fix bc config linting
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
