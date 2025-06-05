from RetailerApi import RetailerApi
import requests
import os
from generate_code_challenge import generate_code_challenge


keystring = os.getenv("etsykeystring")
sharedsecret = os.getenv("etsysharedsecret")

class Etsy(RetailerApi):
    def retrieve_access_token():
        try:
            response = requests.post("https://api.etsy.com/v3/public/oauth/token",
                                     headers={"Content-Type': 'application/x-www-form-urlencoded"},
                                     data = {"grant_type":"client_credentials",
                                             "scope":"listings_r",
                                             "client_id":f"{keystring}",
                                             "code_challenge":f"{generate_code_challenge}",
                                             "code_challenge_method":"S256"
                                     }
                                             
            )
            if(response.status_code == 200):
                data = response.json()
        except Exception as e:
            raise e
        
    def retrieve_response(): return
    # TODO: when application gets approved
    # use the auth token you get from etsy