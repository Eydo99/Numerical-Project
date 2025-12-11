
class openMethodStepRecorder :
    def __init__(self, enabled : bool):
        self.enabled = enabled
        self.steps : list = []
    
    def record(self, step) :
        if(self.enabled) :
            self.steps.append(step)