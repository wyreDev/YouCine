#!/usr/bin/env python3
import json
import os
import sqlite3
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

STATIC_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(STATIC_DIR, 'backend.db')
DB_TIMEOUT = 10


class BackendHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

SAMPLE_VIDEOS = [
    ('Wednesday sn2_Netflix-Original series', 'wyreDev', '100k views · 5hrs ago', 'andons/Wednesday__Season_2___Official_Trailer___Netflix(720p).mp4', 'series'),
    ('peacemaker sn2_Netflix-Original series', 'wyreDev', '15.5k views · 4hrs ago', 'andons/peacemaker_s2_netflix.mp4', 'series'),
    ('Twelve sn1 _Netflix-Original series', 'wyreDev', '150k views · 4hrs ago', 'andons/Twelve_s1_netflix.mp4', 'series'),
    ('Murderbot sn1 _Netflix-Original series', 'wyreDev', '180k views · 3hrs ago', 'andons/Murderbot_s1_netflix.mp4', 'series'),
    ("Wu-Tang Feat Redman, Inspectah Deck - Lesson Learn's (prod by Mathematics)", 'wyreDev', '1.1m views · 9months ago', 'andons/Wu_Tang_Feat_Redman__Inspectah_Deck_-_Lesson_Learn_s__prod_by_Mathematics_.mp4', 'music'),
    ('Method Man & Redman - Heavy ft. 50 Cent (Official Music Video)', 'wyreDev', '490k views · 2yrs ago', 'andons/Method_Man___Redman_-_Heavy_ft__50_Cent__Official_Music_Video_.mp4', 'music'),
    ('DJ wyre - #fresh-street_vibes Best of Future 2025 Trap Mix', 'wyreDev', '27.8k views · 2weeks ago', 'thumbnails/BEST_OF_FUTURE_MIX_-_2025_TRAP_HIP_HOP_LIT_MIX(720p).mp4', 'music'),
    ('Wu-Tang Clan - Winter Warz #onlyGod-can_judge-me', 'wyreDev', '206k views · 4months ago', 'thumbnails/wu_tang_clan_-_Winter_warz(0).mp4', 'music'),
    ('TOXIC_LYRIKALI_-_BACKBENCHER__Official_Video', 'wyreDev', '860k views · 1yr ago', 'andons/TOXIC_LYRIKALI_-_BACKBENCHER__Official_Video_(480p).mp4', 'music'),
    ('Future - Low Life (Official Music Video) ft. The Weeknd', '>>Scorpio<<', '7.2k views · 10months ago', 'thumbnails/Future_-_Low_Life__Official_Music_Video__ft._The_Weeknd(1080p).mp4', 'music'),
    ('Chris Brown - Under the Influence (Official Video)', 'wyreDev', '305k views · 3yrs ago', 'thumbnails/chris.mp4.mp4', 'music'),
    ("Wu-Tang Clan - Ron O'Neal (2014)", 'wyreDev', '208k views · 3months ago', 'thumbnails/wu_tang_clan_-_Ron_O_Neal__2014_.mp4', 'music'),
    ("Wu-Tang Clan - Y'all Been Warned (HD)", 'wyreDev', '68.9k views · 1yr ago', 'thumbnails/Wu-Tang_Clan_-_Y_all_Been_Warned__HD_(0).mp4', 'music'),
]


def get_db_connection():
    return sqlite3.connect(DB_FILE, timeout=DB_TIMEOUT)


def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, title TEXT, author TEXT, description TEXT, src TEXT, category TEXT)'
        )
        cursor.execute('INSERT OR IGNORE INTO users(username, password) VALUES (?, ?)', ('ADMIN', '58905572'))
        cursor.executemany(
            'INSERT OR IGNORE INTO videos(title, author, description, src, category) VALUES (?, ?, ?, ?, ?)',
            SAMPLE_VIDEOS,
        )


class BackendRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/login':
            self.handle_login()
        elif self.path == '/api/register':
            self.handle_register()
        elif self.path == '/api/videos':
            self.handle_video_upload()
        else:
            super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/videos'):
            self.handle_video_search()
        else:
            super().do_GET()

    def handle_login(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({'success': False, 'message': 'Invalid request payload'}, status=400)
            return

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()

        if user:
            self.send_json({'success': True, 'message': 'Login successful'})
        else:
            self.send_json({'success': False, 'message': 'Invalid username or password'}, status=401)

    def handle_register(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({'success': False, 'message': 'Invalid request payload'}, status=400)
            return

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            self.send_json({'success': False, 'message': 'Username and password are required'}, status=400)
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
            self.send_json({'success': True, 'message': 'Registration successful'})
        except sqlite3.IntegrityError:
            self.send_json({'success': False, 'message': 'Username already exists'}, status=409)
        except Exception:
            self.send_json({'success': False, 'message': 'Unable to register user'}, status=500)

    def handle_video_upload(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({'success': False, 'message': 'Invalid request payload'}, status=400)
            return

        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        description = data.get('description', '').strip()
        src = data.get('src', '').strip()
        category = data.get('category', '').strip() or 'other'

        if not title or not author or not src:
            self.send_json({'success': False, 'message': 'Title, author, and video source are required'}, status=400)
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO videos(title, author, description, src, category) VALUES (?, ?, ?, ?, ?)',
                    (title, author, description, src, category),
                )
            self.send_json({'success': True, 'message': 'Video metadata uploaded successfully'})
        except Exception:
            self.send_json({'success': False, 'message': 'Unable to save video metadata'}, status=500)

    def handle_video_search(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        q = params.get('query', [''])[0].strip().lower()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            if q:
                pattern = f'%{q}%'
                cursor.execute(
                    'SELECT title, author, description, src, category FROM videos WHERE lower(title) LIKE ? OR lower(author) LIKE ? OR lower(description) LIKE ?',
                    (pattern, pattern, pattern),
                )
            else:
                cursor.execute('SELECT title, author, description, src, category FROM videos')
            rows = cursor.fetchall()

        videos = [
            {
                'title': row[0],
                'author': row[1],
                'description': row[2],
                'src': row[3],
                'category': row[4],
            }
            for row in rows
        ]
        self.send_json({'videos': videos})

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    os.chdir(STATIC_DIR)
    init_db()
    server = BackendHTTPServer(('0.0.0.0', 8000), BackendRequestHandler)
    print('Starting backend server on http://localhost:8000')
    server.serve_forever()
