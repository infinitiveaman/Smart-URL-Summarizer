from flask import Flask, request, jsonify, redirect, render_template
from utils import generate_short_id, fetch_page_text, summarize_text, load_db, save_db

app = Flask(__name__)

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

    # Check if already exists
    for rec in db["records"]:
        if rec["original_url"] == url:
            return render_template('index.html', records=db["records"], message="URL already shortened!")

    # Fetch text & summarize
    text = fetch_page_text(url)
    summary = summarize_text(text)

    record = {
        "short_id": short_id,
        "original_url": url,
        "short_url": f"http://127.0.0.1:5000/{short_id}",
        "summary": summary,
        "clicks": 0
    }

    db["records"].append(record)
    save_db(db)

    return render_template('index.html', records=db["records"], message="URL shortened successfully!")

@app.route('/<short_id>')
def redirect_url(short_id):
    db = load_db()
    for rec in db["records"]:
        if rec["short_id"] == short_id:
            rec["clicks"] += 1
            save_db(db)
            return redirect(rec["original_url"])
    return "Short URL not found", 404

@app.route('/stats/<short_id>')
def stats(short_id):
    db = load_db()
    for rec in db["records"]:
        if rec["short_id"] == short_id:
            return jsonify(rec)
    return jsonify({"error": "Short URL not found"}), 404
@app.route('/delete/<short_id>')
def delete_record_route(short_id):
    db = load_db()
    new_records = [r for r in db["records"] if r["short_id"] != short_id]
    db["records"] = new_records
    save_db(db)
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

