from flask import Flask, redirect, request
import requests

app = Flask(__name__)

CLIENT_ID = "ISI_CLIENT_ID_KAMU"
CLIENT_SECRET = "ISI_CLIENT_SECRET_KAMU"

@app.route("/")
def login():
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_>
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")

    token = requests.post(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_>,
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
        },
    ).json()["access_token"]

    user = requests.get(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_>
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    return f"<pre>{user}</pre>"
  f"https://github.com/login/oauth/authorize?client_id={CLIENT_>

app.run(port=8000)
