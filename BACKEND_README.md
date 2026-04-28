# YouCine Backend Integration

This workspace now includes a simple backend server using Python and SQLite.

## Files Added

- `backend.py` - Python HTTP server with API endpoints and SQLite database initialization.
- `backend.db` - Created automatically when `backend.py` runs.
- `.gitignore` - Ignores `backend.db` and Python cache files.
- `register.html` - User registration page.
- `upload.html` - Video metadata upload page.

## API Endpoints

- `POST /api/login`
  - Request JSON: `{ "username": "ADMIN", "password": "58905572" }`
  - Response: `{ "success": true, "message": "Login successful" }`

- `POST /api/register`
  - Request JSON: `{ "username": "newuser", "password": "password123" }`
  - Response: `{ "success": true, "message": "Registration successful" }`

- `GET /api/videos`
  - Returns all videos from the database.

- `GET /api/videos?query=...`
  - Filters videos by title, author, or description.

- `POST /api/videos`
  - Request JSON: `{ "title": "Song Title", "author": "Artist", "description": "Details", "src": "andons/song.mp4", "category": "music" }`
  - Response: `{ "success": true, "message": "Video metadata uploaded successfully" }`

## Running the Backend

From the workspace root, run:

```bash
python3 backend.py
```

The backend uses SQLite with a write timeout and WAL journaling for more reliable concurrent access.

Then open your browser at:

```text
http://localhost:8000/index.html
```

The backend server serves the static website and provides the API for login and video search.
