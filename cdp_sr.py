from sodapy import Socrata
from servicerequest import ServiceRequest

def _decode_sr_data(dct):
    #First check that all required attributes are inside the dictionary 
    if all (key in dct for key in ["sr_number","sr_type"]):
        return ServiceRequest(dct["sr_number"],dct["sr_type"])
    return dct

class DataPortalCollector: 

    # api_url = "data.cityofchicago.org"
    # api_token = "6tRoBirkYQMdr8MMFR8FzgBXq"

    def __init__(self):
        self.client = Socrata("data.cityofchicago.org", "6tRoBirkYQMdr8MMFR8FzgBXq", username="v4vigtory@gmail.com", password="311_TeamVeam")
        
    def extract_sr(self, limit):
        service_reqs = [] 
        results = self.client.get("v6vf-nfxy",limit=limit)
        for sr_dict in results: 
            service_req = _decode_sr_data(sr_dict)
            service_reqs.append(service_req)

        return service_reqs

