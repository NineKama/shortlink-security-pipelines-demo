# ShortLink

Website rút gọn link đơn giản, dùng làm ứng dụng mẫu cho demo DevSecOps.

- **Backend:** Python Flask + SQLite (`backend/`)
- **Frontend:** HTML/JS thuần, phục vụ bằng nginx (`frontend/`)

## Chạy bằng Docker

```bash
docker compose up --build
```

Mở http://localhost:8080

## Chạy backend không cần Docker

```bash
cd backend
pip install -r requirements.txt pytest
pytest            # chạy test
python app.py     # API ở http://127.0.0.1:5000
```

## API

| Method | Đường dẫn      | Mô tả                                  |
|--------|----------------|----------------------------------------|
| POST   | `/api/shorten` | Body `{"url": "https://..."}`, trả về mã |
| GET    | `/api/links`   | 20 link mới nhất                       |
| GET    | `/r/<code>`    | Chuyển hướng tới link gốc              |
| GET    | `/api/health`  | Kiểm tra trạng thái                    |

## Cấu trúc

```
backend/   app.py, test_app.py, requirements.txt, Dockerfile
frontend/  index.html, app.js, nginx.conf, Dockerfile
docker-compose.yml
```
