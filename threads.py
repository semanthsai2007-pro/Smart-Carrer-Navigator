"""
threads.py
----------
MODULE 11 - Multithreading

Runs slow tasks (scraping, chart generation) on a background thread
so the Tkinter GUI never freezes. Uses a queue so results can be
picked up safely on the main thread (Tkinter is not thread-safe on
its own).
"""

import threading
import queue


class BackgroundTask:
    """
    Wraps any function call in a thread + queue.
    GUI usage:
        task = BackgroundTask(scraper.run_scrape_and_save, html)
        task.start()
        # then periodically call task.poll() from a GUI .after() loop
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result_queue = queue.Queue()
        self._thread = None

    def _worker(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.result_queue.put(("success", result))
        except Exception as e:
            self.result_queue.put(("error", str(e)))

    def start(self):
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def poll(self):
        """Non-blocking check. Returns (status, result) or None if not done yet."""
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

    def is_alive(self) -> bool:
        return self._thread is not None and self._thread.is_alive()


def run_parallel(tasks: list) -> list:
    """
    Run several zero-arg callables in parallel threads and wait for all to finish.
    Returns results in the same order as tasks: [("success", result) | ("error", msg), ...]
    """
    results = [None] * len(tasks)
    thread_list = []

    def wrapper(index, func):
        try:
            results[index] = ("success", func())
        except Exception as e:
            results[index] = ("error", str(e))

    for i, task in enumerate(tasks):
        t = threading.Thread(target=wrapper, args=(i, task))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    return results
