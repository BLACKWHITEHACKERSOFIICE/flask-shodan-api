import shodan
from flask import Flask, request, jsonify
import shodan

app = Flask(__name__)

SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY")
if not SHODAN_API_KEY:
    raise SystemExit("Set environment variable SHODAN_API_KEY sebelum menjalankan.")

api = shodan.Shodan(SHODAN_API_KEY)

@app.route("/")
def index():
    return "Flask + Shodan example. Use /search?q=QUERY"

@app.route("/search")
def search():
    q = request.args.get("q")
    if not q:
        return jsonify({"error": "Berikan parameter q, contoh: /search?q=nginx"}), 400

    try:
        res = api.search(q)
        return jsonify({
            "query": q,
            "total": res.get("total"),
            "matches_preview": [
                {
                    "ip": m.get("ip_str"),
                    "port": m.get("port"),
                    "data": (m.get("data") or "")[:200]
                }
                for m in res.get("matches", [])[:10]
            ]
        })
    except shodan.APIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF
