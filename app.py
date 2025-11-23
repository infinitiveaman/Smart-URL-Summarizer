import os
from flask import Flask, request, jsonify, redirect, render_template
from utils import (
    generate_short_id, 
    fetch_page_text, 
    summarize_text, 
    load_db, 
    save_db
)

app = Flask(__name__)

# Auto-detect base URL (local or Render)
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")

@app.route('/')
def home():
    db = load_db()
    return render_template('index.html', records=db['records'])

@app.route('/shorten', methods=['POST'])
def shorten_url():
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    short_id = generate_short_id(url)
    db = load_db()

    # Already exists
    for rec in db["records"]:
        if rec["original_url"] == url:
            return render_template(
                'index.html',
                records=db["records"],
                message="URL already exists!"
            )

    # Fetch & summarize content
    text = fetch_page_text(url)
    summary = summarize_text(text)

    record = {
        "short_id": short_id,
        "original_url": url,
        "summary": summary,
        "clicks": 0
    }

    db["records"].append(record)
    save_db(db)

    return render_template(
        'index.html',
        records=db["records"],
        message="URL shortened!"
    )

@app.route('/<short_id>')
def redirect_url(short_id):
    db = load_db()
    for rec in db["records"]:
        if rec["short_id"] == short_id:
            rec["clicks"] += 1
            save_db(db)
            return redirect(rec["original_url"])
    return "Short URL not found", 404

@app.route('/delete/<short_id>')
def delete_record(short_id):
    db = load_db()
    db["records"] = [r for r in db["records"] if r["short_id"] != short_id]
    save_db(db)
    return redirect('/')

@app.route('/stats/<short_id>')
def stats(short_id):
    db = load_db()
    for rec in db["records"]:
        if rec["short_id"] == short_id:
            computed_url = (
                BASE_URL if BASE_URL else request.host_url.rstrip("/")
            ) + "/" + short_id
            
            return jsonify({
                **rec,
                "short_url": computed_url
            })
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
