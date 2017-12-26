import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from assets_compile import compile_assets


class MyHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(
            patterns=["*.js", "*.css"],
            ignore_patterns=["./gem/web/static/app/*"])

    def on_any_event(self, event):
        print(event)
        compile_assets()


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
