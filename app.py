from flask import Flask, render_template, request, redirect
import json, uuid, os
from utils import summarize_with_t5

app = Flask(__name__)

DB_FILE = "database.json"

# Load DB
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Save DB
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET"])
def index():
    records = load_db()
    return render_template("index.html", records=records)

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "")
    if not text.strip():
        return redirect("/")

    summary = summarize_with_t5(text)

    short_id = str(uuid.uuid4())[:8]
    records = load_db()
    records.append({
        "short_id": short_id,
        "text": text,
        "summary": summary
    })
    save_db(records)

    return redirect("/")

@app.route("/delete/<short_id>")
def delete(short_id):
    records = load_db()
    records = [x for x in records if x["short_id"] != short_id]
    save_db(records)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
