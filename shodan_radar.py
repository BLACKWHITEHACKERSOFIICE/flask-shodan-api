import os
import shodan
from flask import Flask, request, jsonify

app = Flask(__name__)

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

@app.route("/")
def home():
    return {"status": "Shodan Radar Online 🚀"}

@app.route("/radar")
def radar():
    if not SHODAN_API_KEY:
        return {"error": "Shodan API key belum di-set"}, 500

    query = request.args.get("q", "nginx")
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        results = api.search(query)
        return jsonify({
            "query": query,
            "total": results["total"],
            "matches": results["matches"][:5]
        })
    except shodan.APIError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
