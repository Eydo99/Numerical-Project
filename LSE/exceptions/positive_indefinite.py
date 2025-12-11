class PositiveIndefiniteException(Exception):
    """Exception raised for invalid input values."""
    
    def __init__(self):
        # Call the base class constructor with the message
        super().__init__(f"Matrix is not positive definite")