from flask import Flask, jsonify, request
import os
import shodan

app = Flask(__name__)

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

if not SHODAN_API_KEY:
    raise RuntimeError("SHODAN_API_KEY belum diset")
if not API_AUTH_TOKEN:
    raise RuntimeError("API_AUTH_TOKEN belum diset")

api = shodan.Shodan(SHODAN_API_KEY)

def check_auth(req):
    return req.headers.get("X-API-KEY") == API_AUTH_TOKEN

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Flask + Shodan API running"
    })

@app.route("/search")
def search():
    if not check_auth(request):
        return jsonify({"error": "unauthorized"}), 401

    q = request.args.get("q")
    if not q:
        return jsonify({"error": "parameter q wajib"}), 400

    try:
        result = api.search(q, limit=5)
        data = []

        for m in result["matches"]:
            data.append({
                "ip": m.get("ip_str"),
                "port": m.get("port"),
                "org": m.get("org"),
                "country": m.get("location", {}).get("country_name")
            })

        return jsonify({
            "query": q,
            "total": result["total"],
            "results": data
        })

    except shodan.APIError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
