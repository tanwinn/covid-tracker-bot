# Covid Tracker Chatbot
Testdrive Chatbot powered by [wit.ai](https://github.com/wit-ai/pywit) and Facebook Messenger for Covid tracker ([deployed API](https://covid-tracker-us.herokuapp.com/))

Deployed: TBA

GitHub: https://github.com/tanwinn/covid-tracker-bot

Submission of [Facebook Messaging Hackathon](https://fbmessaging2.devpost.com/?ref_content=default&ref_feature=challenge&ref_medium=portfolio)

## Dev setup

```bash
git clone git@github.com:tanwinn/covid_tracker_bot.git
cd covid-tracker-bot
pipenv shell  # activate venv
pipenv sync --dev # sync the dependencies packages
```

# Dev framework
```bash
pytest
bc fmt # formatting
prospector # linting TODO: fix bc config linting
```

## Run the App
```bash
uvicorn api.main:app --reload  # Run the app
```
