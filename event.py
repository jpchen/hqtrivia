from detect_text import parse_screenshot
from google_search import run_query_all
from utils import logit
import os
import glob
import time
from watchdog.events import FileSystemEventHandler


class ParseSearchHandler(FileSystemEventHandler):

    def on_created(self, event):
        # by default, mac saves ss on desktop
        all_img = glob.glob('/Users/jpchen/Desktop/*.png')
        # get the last ss
        latest_img = max(all_img, key=os.path.getctime)
        q_and_a = parse_screenshot(latest_img)
        # START_QUERY_ALL = time.time()
        (question, results) = run_query_all(q_and_a['question'], q_and_a['answers'])

        # END_QUERY_ALL = time.time()
        # logit("QUERY ALL", START_QUERY_ALL, END_QUERY_ALL)
        negative_q = True if ' not ' in question.lower() else False
        max_score = 1e12 if negative_q else 0
        best_answer = 'Dont know'
        for (answer, total) in results:
            score = int(total.replace(',', ''))
            if negative_q:
                if max_score > score:
                    max_score = score
                    best_answer = answer
            else:
                if max_score < score:
                    max_score = score
                    best_answer = answer
            print("answer: {} === TOTAL: {}".format(answer, total))
        # read aloud the most likely answer
        os.system('say "{} is the most likely answer"'.format(best_answer))
