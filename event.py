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
        q_and_a = parse_screenshot(latest_img, should_launch=True, compressed=compressed)
        (question, results) = run_query_all(q_and_a['question'], q_and_a['answers'])
        negative_q = ' not ' in question.lower() or "isn ' t " in question.lower()
        max_score = 1e12 if negative_q else 0
        best_answer = None
        total_score = 0
        for (answer, total) in results:
            score = int(total.replace(',', ''))
            total_score += score
            if negative_q:
                if max_score > score:
                    max_score = score
                    best_answer = answer
            else:
                if max_score < score:
                    max_score = score
                    best_answer = answer
            print("{} === SCORE: {}".format(answer, total))
        end = time.time()
        if best_answer:
            # read aloud the most likely answer
            confidence = max_score / total_score * 100
            if negative_q:
                confidence = 100 - confidence
            os.system('say "{} is the most likely answer at {:.1f} percent confidence"'.format(best_answer, confidence))
            print("ANSWER: {} -- {} %".format(best_answer, confidence))
            print('Elapsed wall time: {} seconds', end - start)
        else:
            # something went wrong
            os.system('say fuck if i know')
