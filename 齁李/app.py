
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, json, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
PAGES_DIR = os.path.join(STATIC_DIR, "pages")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

def _load_json(fname, default):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return default

def _save_json(fname, data):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def root():
    return send_from_directory(PAGES_DIR, "index.html")

@app.route("/pages/<path:filename>")
def pages(filename):
    return send_from_directory(PAGES_DIR, filename)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

# ---- Customers ----
@app.route("/api/customers", methods=["GET", "POST"])
def customers():
    data = _load_json("data_customers.json", {})
    if request.method == "GET":
        return jsonify(list(data.values()))
    else:
        # upsert
        body = request.get_json(force=True, silent=True) or {}
        cid = body.get("customer_id")
        if not cid:
            return jsonify({"error": "customer_id required"}), 400
        data[cid] = body
        _save_json("data_customers.json", data)
        return jsonify({"ok": True, "customer": body})

@app.route("/api/customers/<cid>")
def customer(cid):
    data = _load_json("data_customers.json", {})
    if cid in data:
        return jsonify(data[cid])
    return jsonify({"error": "not found"}), 404

# ---- Packages ----
@app.route("/api/packages", methods=["GET", "POST"])
def packages():
    data = _load_json("data_packages.json", {})
    if request.method == "GET":
        return jsonify(list(data.values()))
    else:
        body = request.get_json(force=True, silent=True) or {}
        trk = body.get("tracking_number")
        if not trk:
            return jsonify({"error": "tracking_number required"}), 400
        data[trk] = body
        _save_json("data_packages.json", data)
        return jsonify({"ok": True, "package": body})

@app.route("/api/packages/<trk>")
def package(trk):
    data = _load_json("data_packages.json", {})
    if trk in data:
        return jsonify(data[trk])
    return jsonify({"error": "not found"}), 404

# ---- Tracking ----
@app.route("/api/tracking/<trk>", methods=["GET", "POST"])
def tracking(trk):
    data = _load_json("data_tracking.json", {})
    if request.method == "GET":
        return jsonify(data.get(trk, []))
    else:
        body = request.get_json(force=True, silent=True) or {}
        lst = data.get(trk, [])
        lst.append(body)
        data[trk] = lst
        _save_json("data_tracking.json", data)
        return jsonify({"ok": True, "events": lst})

# ---- Billing ----
@app.route("/api/billing")
def billing():
    bills = _load_json("data_billing.json", [])
    customer = request.args.get("customer")
    period = request.args.get("period")
    result = [b for b in bills if (not customer or b.get("customerAccount")==customer) and (not period or b.get("period")==period)]
    # Build a tiny demo 'items' to show in the table
    items = []
    # In a real app this would query packages; here we just create some sample rows
    for i, b in enumerate(result, 1):
        items.append({
            "tracking_number": f"TRK-DEMO-{i:03d}",
            "date": f"{b.get('period', '2025-12')}-{:02d}".format(5+i),
            "service": b.get("method", "月結"),
            "amount": b.get("amount", 0)
        })
    return jsonify({
        "summary": result,
        "items": items
    })

# Convenience route to help find pages quickly
@app.route("/go/<page>")
def go(page):
    filename = f"{page}.html"
    return send_from_directory(PAGES_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
