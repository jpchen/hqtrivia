# will take screenshot => output/screenshot.png
from detect_text import parse_screenshot, IMAGE_PATH
from google_search import run_query_all
from utils import logit
import os
import time

START_FULL = time.time()

def main():
    q_and_a = parse_screenshot(IMAGE_PATH)
    # START_QUERY_ALL = time.time()
    (question, results) = run_query_all(q_and_a['question'], q_and_a['answers'])

    # END_QUERY_ALL = time.time()
    # logit("QUERY ALL", START_QUERY_ALL, END_QUERY_ALL)
    negative_q = True if 'not' in question.lower() else False
    max_score = 0
    best_answer = 'Dont know'
    for (answer, total) in results:
        if negative_q:
            max_score = total if total < max_score else max_score
            best_answer = answer if total < max_score else best_answer
        else:
            max_score = total if total > max_score else max_score
            best_answer = answer if total > max_score else best_answer
        print("answer: {} === TOTAL: {}".format(answer, total))
    # read aloud the most likely answer
    os.system('say "{} is the most likely answer"'.format(best_answer))

if __name__ == '__main__':
    main()

    END_FULL = time.time()
    logit("FULL", START_FULL, time.time())
