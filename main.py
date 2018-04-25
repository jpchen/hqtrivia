# will take screenshot => output/screenshot.png
from detect_text import parse_screenshot
from google_search import run_query_all
from event import ParseSearchHandler
from utils import logit
import os
import glob
import time
from watchdog.observers import Observer

START_FULL = time.time()

def main():
    event_handler = ParseSearchHandler()
    observer = Observer()
    observer.schedule(event_handler, '/Users/jpchen/Desktop')
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
    END_FULL = time.time()
    logit("FULL", START_FULL, time.time())
