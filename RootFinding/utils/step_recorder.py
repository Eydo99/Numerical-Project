from .models import SecantStep 
class SecantMethodStepRecorder :
    def __init__(self, enabled : bool):
        self.enabled = enabled
        self.steps : list[SecantStep] = []
    
    def record(self, step : SecantStep) :
        if(self.enabled) :
            self.steps.append(step)