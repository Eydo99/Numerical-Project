class InvalidIntervalException(Exception):
    
    def __init__(self):
        
        super().__init__("No roots exist in the given interval")