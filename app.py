from flask import Flask, request, jsonify, redirect
from db import get_db_connection
import random
import string

app = Flask(__name__)

# Generate short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/")
def home():
    return "URL Shortener Running 🚀"


# CREATE SHORT URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]

    conn = get_db_connection()

    # 🔥 Generate unique short code
    while True:
        short_code = generate_short_code()
        
        existing = conn.execute(
            "SELECT 1 FROM urls WHERE short_code = ?",
            (short_code,)
        ).fetchone()
        
        if existing is None:
            break

    # Save to DB
    conn.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "short_code": short_code,
        "original_url": original_url
    })


# REDIRECT + CLICK TRACKING
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = get_db_connection()

    result = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    if result is None:
        conn.close()
        return jsonify({"error": "URL not found"}), 404

    original_url = result["original_url"]

    # 🔥 Increase click count
    conn.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
        (short_code,)
    )
    conn.commit()
    conn.close()

    return redirect(original_url)


@app.route("/stats/<short_code>")
def get_stats(short_code):
    conn = get_db_connection()

    result = conn.execute(
        "SELECT original_url, click_count FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "original_url": result["original_url"],
        "click_count": result["click_count"]
    })


if __name__ == "__main__":
    app.run(debug=True)