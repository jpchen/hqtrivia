from detect_text import parse_screenshot
from google_search import run_query_all
from event import ParseSearchHandler
import os
import glob
from watchdog.observers import Observer

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
