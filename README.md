HQ Trivia Hack
===============

**This is for recreational use. Using it in a cash game may be against HQ Trivia's TOS. Use at your own risk**.

Inspired by [this medium post](https://hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365) but uses Pillow for screenshotting and Google Vision API for OCR parsing instead.

## TODO:
- android support
- better filtering

## Usage:
1. Download a credentials.json service credentials file from a Google Vision-enabled Cloud Platform project (see OCR section below),
then create config.json following config.json.sample

2. connect iphone to Mac

3. position quicktime player at top left -> select New Movie Recording

4. open recording button dropdown -> switch Movie recording to iphone

5. `python main.py`

### 1 - Grab screenshot

USAGE: `from screengrab import screenshot`

- Quicktime player must be positioned at top left of screen, on iPhone recording
- Uses PILLOW imagegrab - bounding box grabs only question + the multiple choice answers

### 2 - OCR detect text

USAGE: `from detect_text import parse_screenshot`

- Processes screenshot into question + answers
- Launches browser to google search of the question

This uses Google Cloud Vision api, so make sure you've downloaded a service account file from a Google Cloud project that has [enabled Google Cloud Vision](https://cloud.google.com/vision/docs/before-you-begin). See "using a service account": https://cloud.google.com/vision/docs/auth

Then add the path of that service account json file `config.json` as `CREDENTIALS_PATH`.

`py detect_text.py` returns a dict:
```
{
    question: 'After Texas , what U . S . state produces the most crude oil ?'
    answers: ['Oklahoma', 'North Dakota', 'Alaska']
}
```
### 3 - Using Google Custom search, run three custom searches with question + answer.

USAGE: `from google_search import run_query_all`

https://developers.google.com/custom-search/json-api/v1/overview

Compare the total num results for each answer:
```
answer: Oklahoma === TOTAL: 1,180,000
answer: North Dakota === TOTAL: 1,360,000
answer: Alaska === TOTAL: 1,330,000
