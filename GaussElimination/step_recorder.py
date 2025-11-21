import copy

class StepRecorder:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps= []

    def record(self, A, b, message=""):
        if self.enabled:
            self.steps.append((copy.deepcopy(A),copy.deepcopy(b), message))