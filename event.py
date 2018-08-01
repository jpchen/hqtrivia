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
        try:
            q_and_a = parse_screenshot(latest_img, should_launch=True, compressed=compressed)
            question, answer = q_and_a['question'], q_and_a['answers']
            negative_q = ' not ' in question.lower() or "isn ' t " in question.lower() or ' never ' in question.lower()
            answer = run_query_all(question, answer, is_negative=negative_q)
        except:
            pass
        end = time.time()
        try:
            # read aloud the answer
            os.system('say "{} is the most likely answer."'.format(answer))
            print('Elapsed wall time: {} seconds', end - start)
        except:
            # something went wrong
            os.system('say fuck if i know')
