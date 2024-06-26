from flask import Flask, redirect, session, request
from server.auth.auth import authorize, oauth2callback
#from auth.auth import authorize, oauth2callback

_CLIENT_URL = "http://localhost:4200"

app = Flask(__name__)
app.secret_key = "SECRET KEY"

@app.route("/authorize")
def authorize_endpoint():
    token = request.args.get("token")
    session["token"] = token
    auth_info = authorize()
    passthrough_val = auth_info["passthrough_val"]
    session["passthrough_val"] = passthrough_val
    url = auth_info["authorization_url"]
    return redirect(url)

@app.route("/oauth2callback")
def oauth2callback_endpoint():
    token = session["token"]
    passthrough_val = session["passthrough_val"]
    state = request.args.get("state")
    code = request.args.get("code")
    oauth2callback(passthrough_val, state, code, token)
    return redirect(_CLIENT_URL)