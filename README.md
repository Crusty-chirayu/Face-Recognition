# FaceGate — Face Recognition API

> A production-ready face recognition and attendance tracking backend built with FastAPI.

---

## Overview

FaceGate is a FastAPI-powered backend system that combines secure authentication, facial recognition, and automated attendance tracking into a single cohesive API. Built for organizations that need reliable identity verification without the complexity of third-party SaaS solutions.

---

## Features

| Feature | Description |
|---|---|
| 🔐 JWT Authentication | Secure token-based auth with role management |
| 👤 User Management | Full CRUD for user profiles and accounts |
| 🧠 Face Recognition | Embedding-based facial matching via `face_recognition` |
| 📸 Image Upload | Profile image ingestion and preprocessing |
| 📊 Attendance Tracking | Automated check-in/check-out via face match |

---

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.11
- **ORM:** SQLAlchemy (Async)
- **Database:** SQLite
- **Vision:** OpenCV + face-recognition (dlib)

---

## Getting Started

### Prerequisites

- Python 3.11+
- `pip`
- `cmake` (required by dlib for face-recognition)

### Installation

```bash
# Clone the repository
git clone https://github.com/Crusty-chirayu/Face-Recognition.git
cd Face-Recognition/facegate/backend

# Create and activate virtual environment
python3.11 -m venv venv311
source venv311/bin/activate        # bash/zsh
# source venv311/bin/activate.fish # fish shell

# Install dependencies
pip install -r requirements.txt

# Start the development server
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Default Admin Credentials

```
Email:    admin@gmail.com
Password: AdminPass123!
```

> ⚠️ Change these credentials immediately in any non-development environment.

---

## API Reference

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Obtain a JWT access token |
| `GET` | `/auth/me` | Retrieve the authenticated user's profile |

### Face Management

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/faces/` | Register a new face entry |
| `POST` | `/faces/{id}/upload` | Upload an image for a registered face |
| `POST` | `/faces/{id}/embed` | Generate a face embedding from the uploaded image |
| `POST` | `/faces/match` | Match an incoming image against stored embeddings |

---

## Workflow

```
1. Register face     →  POST /faces/
2. Upload image      →  POST /faces/{id}/upload
3. Generate embedding →  POST /faces/{id}/embed
4. Match face        →  POST /faces/match
```

For attendance use cases, run step 4 at check-in/check-out time. The system returns the matched user's ID and a confidence score.

---

## Project Structure

```
facegate/
└── backend/
    ├── app/
    │   ├── main.py          # FastAPI app entry point
    │   ├── models/          # SQLAlchemy ORM models
    │   ├── routers/         # Route handlers (auth, faces)
    │   ├── schemas/         # Pydantic request/response schemas
    │   ├── services/        # Business logic (face matching, embedding)
    │   └── core/            # Config, security, database session
    ├── requirements.txt
    └── README.md
```

---

## Roadmap

- [ ] PostgreSQL support
- [ ] Multi-face detection per image
- [ ] Attendance report export (CSV / PDF)
- [ ] Docker + Docker Compose setup
- [ ] WebSocket real-time attendance feed

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is open source. See [LICENSE](LICENSE) for details.

---

## Author

**Chirayu**  
GitHub: [@Crusty-chirayu](https://github.com/Crusty-chirayu)
