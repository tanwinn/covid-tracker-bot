# QA Testing strategy
## Error:
1. Tracker API down:
- Chatbot replies with a text telling API is down. Potentially: ask for handover protocal to tell the mod

2. Giving giberrish country:
- "Give me cases of asldkjlkas" --> JHU doesn't support `gibberish`

3. Gibberish:
- "aiksdulkasd" --> Giving instructions of `getting started`

3. Giving unresolved country by wit:
- "Give me cases of holland" --> Still give the correct info depends if the country is listed in the country_code.json. Tech needs to make sure the lookup strategy is all lowercase

4. Giving valid country with invalid date
- "Give me cases of Japan next year" --> Give the latest case of Japan

5. Giving locations and multiple times:
- "japan and thailand and USA yesterday and two days ago" -> give the latest info of the locations