from detect_text import parse_screenshot, compress
from google_search import run_query_all
import os
import glob
import time
from watchdog.events import FileSystemEventHandler

compressed = True

class ParseSearchHandler(FileSystemEventHandler):

    def on_created(self, event):
        start = time.time()
        # by default, mac saves ss on desktop
        all_img = glob.glob('/Users/jpchen/Desktop/*.png')
        # get the last ss
        latest_img = max(all_img, key=os.path.getctime)
        if compressed:
            latest_img = compress(latest_img)
        negative_q = ' not ' in question.lower() or "isn ' t " in question.lower() or ' never ' in question.lower()
        try:
            q_and_a = parse_screenshot(latest_img, should_launch=True, compressed=compressed)
            (question, results) = run_query_all(q_and_a['question'], q_and_a['answers'], is_negative=negative_q)
        except:
            pass
        end = time.time()
        try:
            # read aloud the most likely answer
#             confidence = max_score / total_score * 100
#             if negative_q:
#                 confidence = 100 - confidence
            os.system('say "{} is the most likely answer."'.format(best_answer))
            print("ANSWER: {} -- {} %".format(best_answer))
            print('Elapsed wall time: {} seconds', end - start)
        except:
            # something went wrong
            os.system('say fuck if i know')
