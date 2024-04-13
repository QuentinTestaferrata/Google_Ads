from google.oauth2 import id_token
from google.auth.transport import requests
from google.cloud import secretmanager
from google import *
import google_crc32c

_CLIENT_ID = "77597726964-8bb63iabsbir536rgjh4391iilquqmj1.apps.googleusercontent.com"
_PROJECT_ID = "alpine-inkwell-419712"
_PROJECT_NUMBER = "77597726964"

class Secret:

    def __init__(self, token):
        #get id from token
        self.id = self.validate_token_get_id(token);
        self.client = secretmanager.SecretManagerServiceClient()

    def validate_token_get_id(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), _CLIENT_ID)
            return idinfo['sub']
        except ValueError:
            #invalid token
            pass

    def create_secret_version(self, refresh_token):
        #check if secret exists
        if self.does_secret_exist() is False:
            #if not create secret  
            parent = f"projects/{_PROJECT_ID}"

            #Create the secret
            response = self.client.create_secret(
                request = {
                    "parent": parent,
                    "secret_id": self.id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )

        #create secret version under secret
        parent = self.client.secret_path(_PROJECT_ID, self.id)

        payload = refresh_token.encode("UTF-8")
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload)

        self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload, "data_crc32": int(crc32c.hexdigest(), 16)},
            }
        )


    def does_secret_exist(self):
        parent = f"projects/{_PROJECT_ID}"

        for secret in self.client.list_secrets(request={"parent": parent}):
            secret_name = f"projects/{_PROJECT_NUMBER}/secrets/{self.id}"
            if secret.name == secret_name:
                return True
        
        return False
    
    def get_secret_version(self):
        name = f"projects/{_PROJECT_ID}/secrets/{self.id}/versions/latest"
        response = self.client.access_secret_version(request={"name":name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected")
            return response
        
        return response.payload.data.decode("UTF-8")