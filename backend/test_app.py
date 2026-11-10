import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

from app import app  # noqa: E402


def test_shorten_and_redirect():
    c = app.test_client()
    r = c.post("/api/shorten", json={"url": "https://example.com/a"})
    assert r.status_code == 201
    code = r.get_json()["code"]
    r = c.get(f"/r/{code}")
    assert r.status_code == 302
    assert r.headers["Location"] == "https://example.com/a"
    assert c.get("/api/links").get_json()[0]["clicks"] == 1


def test_rejects_bad_url():
    c = app.test_client()
    for bad in ["", "javascript:alert(1)", "ftp://x.com", "abc"]:
        assert c.post("/api/shorten", json={"url": bad}).status_code == 400


def test_unknown_code():
    assert app.test_client().get("/r/nope00").status_code == 404
