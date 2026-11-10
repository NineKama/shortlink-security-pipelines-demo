"""ShortLink backend: API rút gọn link bằng Flask + SQLite."""
import os
import secrets
import sqlite3
import string
from urllib.parse import urlparse

from flask import Flask, abort, g, jsonify, redirect, request

DB_PATH = os.environ.get("DB_PATH", "shortlink.db")
ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_URL_LENGTH = 2048

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """CREATE TABLE IF NOT EXISTS links (
               code       TEXT PRIMARY KEY,
               url        TEXT NOT NULL,
               clicks     INTEGER NOT NULL DEFAULT 0,
               created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
           )"""
    )
    db.commit()
    db.close()


def is_valid_url(url):
    """Chỉ chấp nhận http/https và phải có tên miền."""
    if not isinstance(url, str) or not url or len(url) > MAX_URL_LENGTH:
        return False
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def new_code():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/shorten")
def shorten():
    data = request.get_json(silent=True)
    url = data.get("url") if isinstance(data, dict) else None
    url = url.strip() if isinstance(url, str) else ""
    if not is_valid_url(url):
        return jsonify(error="Link không hợp lệ. Link phải bắt đầu bằng http:// hoặc https://"), 400

    db = get_db()
    for _ in range(5):  # thử lại nếu trùng mã
        code = new_code()
        try:
            db.execute("INSERT INTO links (code, url) VALUES (?, ?)", (code, url))
            db.commit()
            return jsonify(code=code, url=url), 201
        except sqlite3.IntegrityError:
            continue
    return jsonify(error="Không tạo được mã, hãy thử lại"), 500


@app.get("/api/links")
def list_links():
    rows = get_db().execute(
        "SELECT code, url, clicks, created_at FROM links ORDER BY rowid DESC LIMIT 20"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/r/<code>")
def follow(code):
    db = get_db()
    row = db.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        abort(404)
    db.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
    db.commit()
    return redirect(row["url"], code=302)


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
