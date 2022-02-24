class ServiceRequest:

    def __init__(self, sr_number, sr_type):
        self.sr_number = sr_number 
        self.sr_type = sr_type

    def __str__(self):
        return f"SR_Number={self.sr_number}\nSR_Type={self.sr_type}"