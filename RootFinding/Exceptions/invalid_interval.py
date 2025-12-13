class InvalidIntervalException(Exception):
    
    def __init__(self):
        
        super().__init__("No sign change on the endpoints of the interval")