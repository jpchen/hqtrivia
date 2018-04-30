import time
import io
import os
import webbrowser
from profilehooks import profile

# load config
import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Service credentials
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    data["GOOGLE"]["CREDENTIALS_PATH"])
scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# The name of the image file to annotate
from screengrab import screenshot

# List of words to clean from the question during google search
WORDS_TO_STRIP = [
    'who', 'what', 'where', 'when', 'of', 'and', 'that', 'have', 'for',
    'on', 'with', 'as', 'this', 'by', 'from', 'they', 'a', 'an', 'and', 'my',
    'did', 'do', 'in', 'to', '?', ',', 'these'
]

# Instantiates a Google Vision client with explicit creds
client = vision.ImageAnnotatorClient(credentials=scoped_credentials)

def parse_screenshot(path, should_launch=True):
    # 2. Parse for the block texts
    texts_and_bounds = detect_text_with_bounds(path)
    # 3. Parse into questions and answers
    questions_and_answers = get_questions_and_answers(*texts_and_bounds, should_launch=should_launch)
    return questions_and_answers

def take_screenshot(path):
    screenshot(path)

def get_questions_and_answers(block_texts, block_bounds, should_launch=True):
    """
    - return a dict with `question` and array of `answers` (attempt to get 3)
    - launches the question in web browser
    """
    # launch in browser cause until we solve AI you need a human for some of these things
    if (should_launch):
        launch_web(block_texts[0])

    print('Q: ' + block_texts[0])
    question = prune_question(block_texts.pop(0))

    # cash show puts extra text for cash questions
    if('Prize for this question' in block_texts[0]):
        del block_texts[0]

    return {'question': question, 'answers': block_texts}

def prune_question(question):
    words = question.split()
    words = [word for word in words if word.lower() not in WORDS_TO_STRIP]
    pruned_question = " ".join(words)
    return pruned_question

def launch_web(question):
    url = "https://www.google.com.tr/search?q={}".format(question)
    webbrowser.open_new_tab(url)

@profile
def detect_text_with_bounds(path):
    """
    Detects text in the file with bounds.
    Returns a tuple of the block texts and block bounds
    This is slow and inconsistent AF:
    https://github.com/GoogleCloudPlatform/google-cloud-python/issues/5261
    """

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.document_text_detection(image=image) # <-- this line is the bottleneck
    document = response.full_text_annotation

    block_bounds = []
    block_texts = []
    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
            block_words_mapped = list(map(map_words, block_words))

            block_text = ' '.join(block_words_mapped)
            block_texts.append(block_text)
            block_bounds.append(block.bounding_box)

    return (block_texts, block_bounds)

def is_question_block(bounding_box):
    """incredibly quick-and-dirty check to see if this is probably a question"""
    top_left = bounding_box.vertices[0]
    bottom_right = bounding_box.vertices[3]
    return bottom_right.y - top_left.y > 100

def map_words(word):
    characters = list(map(lambda symbol: symbol.text, word.symbols))
    return ''.join(characters)


if __name__ == '__main__':
    # Get the questions and answers
    questions_and_answers = parse_screenshot(None)
