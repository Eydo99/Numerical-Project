import copy
from .models import SolStep, StepType

class GaussStepRecorder:
    def __init__(self, enabled=False):
        self.enabled = enabled
        self.steps = []

    def record(self, A, b, step_type):
        if self.enabled:
            self.steps.append(SolStep(copy.deepcopy(A),copy.deepcopy(b), step_type))