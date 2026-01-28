from flask import Flask, jsonify, request
import os
import shodan

app = Flask(__name__)

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

if not SHODAN_API_KEY:
    raise RuntimeError("SHODAN_API_KEY belum diset")

api = shodan.Shodan(SHODAN_API_KEY)

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Flask + Shodan API running"
    })

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "parameter q wajib"}), 400

    try:
        result = api.search(query, limit=5)
        data = []

        for match in result["matches"]:
            data.append({
                "ip": match.get("ip_str"),
                "port": match.get("port"),
                "org": match.get("org"),
                "country": match.get("location", {}).get("country_name")
            })

        return jsonify({
            "query": query,
            "total": result["total"],
            "results": data
        })

    except shodan.APIError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
