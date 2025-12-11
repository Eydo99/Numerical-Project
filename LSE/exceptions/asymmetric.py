class AsymmetricMatrixException(Exception):
    """Exception raised for invalid input values."""
    
    def __init__(self):
        # Store the error details

        # Call the base class constructor with the message
        super().__init__(f"Matrix is asymmetric")