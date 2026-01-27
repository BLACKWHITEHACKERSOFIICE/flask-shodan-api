import os
from flask import Flask, request
from flask import render_template
import shodan

app = Flask(__name__)

SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY")
api = shodan.Shodan(SHODAN_API_KEY)

@app.route("/ui")
def ui():
    return render_template("index.html")

@app.route("/")
def index():
    return "OK Flask + Shodan"

@app.route("/search")
def search():
    q = request.args.get("q", "nginx")
    r = api.search(q)
    return {
        "query": q,
        "total": r["total"],
        "matches": r["matches"][:5]
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
