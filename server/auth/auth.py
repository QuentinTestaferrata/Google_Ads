from google_auth_oauthlib.flow import Flow
import hashlib
import os

from server.auth.secret import Secret

_CLIENT_SECRETS_PATH = "C:\\Users\\Quentin\\OneDrive\\Bureau\\google-ads\\client_secret_77597726964-8bb63iabsbir536rgjh4391iilquqmj1.apps.googleusercontent.com.json"
_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "127.0.0.1"
_PORT = 5000
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}/oauth2callback"

def authorize():
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=[_SCOPE])
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token as described here:
    # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )
    return {"authorization_url": authorization_url, "passthrough_val":passthrough_val}

def oauth2callback(passthrough_val, state, code, token):
    if passthrough_val != state:
        message = "State token does not match the expected state."
        raise ValueError(message)
    
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=None) #[_SCOPE] Hier heb ik None gezet omdat het anders niet werkt
    flow.redirect_uri = _REDIRECT_URI
    flow.fetch_token(code=code)
    refresh_token = flow.credentials.refresh_token
    secret = Secret(token)
    secret.create_secret_version
