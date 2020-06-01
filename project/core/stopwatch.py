import time

class StopWatch:
    '''
    Provide rudimentary millisecond stopwatch
    for benchmarking purposes.
    '''
    def __init__(self, label):
        self.label = label

    def start(self):
        self.start_time = time.thread_time_ns()

    def stop(self):
        self.stop_time = time.thread_time_ns()
        self.elapsed_ms = (self.stop_time - self.start_time) / 1000000

    def show_results(self):
        print(f'{self.label} = {self.elapsed_ms}')
