from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, parse_qs
from datetime import datetime, timezone
import json
import os
from main import OPENAPI_SPEC, SWAGGER_HTML_TEMPLATE
from models.user import User
from models.announcement import Announcement
from models.job_posting import JobPosting
from views.view import View
from routes import get_configured_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure Unified MVC Router (Web & API routes)
router = get_configured_router()


def get_html_content(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().encode('utf-8')
    if filename == 'index.html':
        return b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Main</title></head><body><h1>Temporary Main Page</h1><p>temporary one main page</p></body></html>"
    return b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>About</title></head><body><h1>About Page</h1><p>temporary about page</p></body></html>"


class SimpleHandler(BaseHTTPRequestHandler):
    def _send(self, status, content_type, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        """Reads body supporting both application/json and application/x-www-form-urlencoded."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}, None
        try:
            raw_body = self.rfile.read(content_length).decode('utf-8')
            content_type = self.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return json.loads(raw_body), None
            elif 'application/x-www-form-urlencoded' in content_type:
                parsed = parse_qs(raw_body)
                return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}, None
            else:
                try:
                    return json.loads(raw_body), None
                except Exception:
                    parsed = parse_qs(raw_body)
                    if parsed:
                        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}, None
                    return {}, None
        except Exception as e:
            return None, f"İstek gövdesi okunamadı: {str(e)}"

    def do_GET(self):
        # 1. Ana Sayfa: GET / -> index.html (Temporary Main Page)
        if self.path in ['/', '', '/main', '/index.html']:
            self._send(200, 'text/html', get_html_content('index.html'))
            return

        # 'ok' endpointi: GET /ok veya GET /alumni -> 'ok'
        if self.path in ['/ok', '/ok/', '/alumni', '/alumni/']:
            self._send(200, 'text/plain', b'ok')
            return

        # 5. About Sayfası: GET /about -> about.html
        if self.path in ['/about', '/about/', '/aout', '/aout/', '/about.html']:
            self._send(200, 'text/html', get_html_content('about.html'))
            return

        # 4. Task: GET /sum/{nm1}/{nm2} -> nm1 + nm2 toplamı
        if self.path.startswith('/sum/'):
            parts = [p for p in unquote(self.path).strip('/').split('/') if p]
            if len(parts) == 3:
                try:
                    n1 = float(parts[1])
                    n2 = float(parts[2])
                    total = int(n1 + n2) if (n1 + n2).is_integer() else (n1 + n2)
                    self._send(200, 'text/plain', str(total))
                except ValueError:
                    self._send(400, 'text/plain', 'Lutfen gecerli sayilar girin')
            else:
                self._send(400, 'text/plain', 'Kullanim: /sum/{sayi1}/{sayi2}')
            return

        # 2. Task: GET /hello -> 'hello world!'
        if self.path in ['/hello', '/hello/']:
            self._send(200, 'text/plain', 'hello world!')
            return

        # 3. Task: GET /hello/{name} -> 'hello, {name}'
        if self.path.startswith('/hello/'):
            name = unquote(self.path[len('/hello/'):].strip('/'))
            if name:
                self._send(200, 'text/plain', f"hello, {name}")
            else:
                self._send(200, 'text/plain', 'hello world!')
            return

        # Swagger UI Dokümantasyon Arayüzü: GET /api/swagger
        if self.path in ['/api/swagger', '/api/swagger/']:
            self._send(200, 'text/html', SWAGGER_HTML_TEMPLATE)
            return

        # Swagger / OpenAPI JSON Spesifikasyonu: GET /api/swagger.json veya /api/openapi.json
        if self.path in ['/api/swagger.json', '/api/openapi.json']:
            self._send(200, 'application/json', json.dumps(OPENAPI_SPEC, ensure_ascii=False, indent=2))
            return

        # 6. Task: GET /api/health -> JSON
        if self.path in ['/api/health', '/api/health/', '/health', '/health/']:
            health_response = json.dumps({
                "status": "UP",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, ensure_ascii=False, indent=2)
            self._send(200, 'application/json', health_response)
            return

        if self.path == '/favicon.ico':
            self._send(204, 'text/plain', b'')
            return

        # Dispatch through MVC Router:
        # Route 1: GET /users -> listing (R) -> UserController.index() -> View.render_users_index()
        # Route 2: GET /users/{id} -> detail -> UserController.show() -> View.render_users_show()
        # API Routes: GET /api/users, GET /api/users/{id}
        clean_path = self.path.split('?')[0]
        route_match = router.dispatch("GET", clean_path)
        if route_match:
            handler, params = route_match
            result = handler(params)
            # View Layer returns HTML string directly
            if isinstance(result, str):
                self._send(200, 'text/html', result)
                return
            # ApiUserController returns (status_code, dict)
            elif isinstance(result, tuple) and len(result) == 2:
                status, data = result
                self._send(status, 'application/json', json.dumps(data, ensure_ascii=False, indent=2))
                return
            elif isinstance(result, dict):
                self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                return

        self._send(404, 'text/plain', '404 Not Found')

    def do_POST(self):
        # Dispatch through MVC Router:
        # Route: POST /users -> creating (C) -> UserController.store(data) -> View.render_users_index()
        # Route: POST /api/users -> ApiUserController.store(data)
        clean_path = self.path.split('?')[0]
        route_match = router.dispatch("POST", clean_path)
        if route_match:
            handler, params = route_match
            data, err = self._read_body()
            if err and self.path.startswith('/api/'):
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": err
                }, ensure_ascii=False, indent=2))
                return

            result = handler(params, data or {})
            # View Layer returns HTML string directly
            if isinstance(result, str):
                self._send(200, 'text/html', result)
                return
            elif isinstance(result, tuple) and len(result) == 2:
                status, res = result
                self._send(status, 'application/json', json.dumps(res, ensure_ascii=False, indent=2))
                return
            elif isinstance(result, dict):
                if "redirect" in result:
                    self.send_response(302)
                    self.send_header('Location', result['redirect'])
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    return
                self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                return

        self._send(404, 'application/json', json.dumps({
            "error": "NotFound",
            "message": "Endpoint bulunamadı"
        }, ensure_ascii=False, indent=2))

    def do_PUT(self):
        # Dispatch through MVC Router
        clean_path = self.path.split('?')[0]
        route_match = router.dispatch("PUT", clean_path)
        if route_match:
            handler, params = route_match
            data, err = self._read_body()
            if err and self.path.startswith('/api/'):
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": err
                }, ensure_ascii=False, indent=2))
                return

            result = handler(params, data or {})
            if isinstance(result, str):
                self._send(200, 'text/html', result)
                return
            elif isinstance(result, tuple) and len(result) == 2:
                status, res = result
                self._send(status, 'application/json', json.dumps(res, ensure_ascii=False, indent=2))
                return
            elif isinstance(result, dict):
                self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                return

        self._send(404, 'application/json', json.dumps({
            "error": "NotFound",
            "message": "Endpoint bulunamadı. Kullanım: PUT /api/users/{id} veya PUT /users/{id}"
        }, ensure_ascii=False, indent=2))

    def do_PATCH(self):
        # Dispatch through MVC Router
        clean_path = self.path.split('?')[0]
        route_match = router.dispatch("PATCH", clean_path)
        if route_match:
            handler, params = route_match
            data, err = self._read_body()
            if err and self.path.startswith('/api/'):
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": err
                }, ensure_ascii=False, indent=2))
                return

            result = handler(params, data or {})
            if isinstance(result, str):
                self._send(200, 'text/html', result)
                return
            elif isinstance(result, tuple) and len(result) == 2:
                status, res = result
                self._send(status, 'application/json', json.dumps(res, ensure_ascii=False, indent=2))
                return
            elif isinstance(result, dict):
                self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                return

        self._send(404, 'application/json', json.dumps({
            "error": "NotFound",
            "message": "Endpoint bulunamadı. Kullanım: PATCH /api/users/{id} veya PATCH /users/{id}"
        }, ensure_ascii=False, indent=2))

    def do_DELETE(self):
        # Dispatch through MVC Router
        clean_path = self.path.split('?')[0]
        route_match = router.dispatch("DELETE", clean_path)
        if route_match:
            handler, params = route_match
            result = handler(params)
            if isinstance(result, str):
                self._send(200, 'text/html', result)
                return
            elif isinstance(result, tuple) and len(result) == 2:
                status, res = result
                self._send(status, 'application/json', json.dumps(res, ensure_ascii=False, indent=2))
                return
            elif isinstance(result, dict):
                self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                return

        self._send(404, 'application/json', json.dumps({
            "error": "NotFound",
            "message": "Endpoint bulunamadı. Kullanım: DELETE /api/users/{id} veya DELETE /users/{id}"
        }, ensure_ascii=False, indent=2))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    # Ensure database connection & verify entities exist
    try:
        user_count = len(User.find_all())
        announcement_count = len(Announcement.find_all())
        job_count = len(JobPosting.find_all())
        print(f"[DB] Baglanti saglandi. Mevcut kayitlar: {user_count} Kullanici, {announcement_count} Duyuru, {job_count} Is Ilani.")
    except Exception as e:
        print(f"[DB] Uyari: Veritabani baglantisi sirasinda hata: {e}")

    port = 80
    try:
        server = ThreadingHTTPServer(('0.0.0.0', 80), SimpleHandler)
        print("Sunucu calisiyor: http://localhost")
    except Exception:
        port = 8000
        server = ThreadingHTTPServer(('0.0.0.0', 8000), SimpleHandler)
        print("Sunucu calisiyor: http://localhost:8000")

    print("\n--- DIRECT ROUTES (Resource-Level) ---")
    print("-> GET /users                          -> Web HTML Kullanici Listesi")
    print("-> GET /announcements                  -> Web HTML Duyuru Yonetim Paneli")
    print("-> GET /jobs                           -> Web HTML Is & Staj Ilanlari Paneli")
    print("-> GET /api/users                      -> REST API Kullanicilar Listesi")
    print("-> GET /api/announcements              -> REST API Duyurular Listesi")
    print("-> GET /api/jobs                       -> REST API Is Ilanlari Listesi")
    print("-> GET /api/swagger                    -> Swagger UI Dokümantasyon")
    print("\n--- NESTED ROUTES (Hierarchical Relations) ---")
    print("-> GET /users/{id}/jobs                -> Web HTML Belirli Kullanicinin Ilanlari")
    print("-> GET /api/users/{id}/jobs            -> REST API Belirli Kullanicinin Ilanlari")
    print("-> POST /api/users/{id}/jobs           -> REST API Kullaniciya Bagli Ilan Ekle")
    print("-> GET /api/users/{id}/announcements   -> REST API Kullaniciya Bagli Duyurular")
    print("-> GET /api/users/{id}/profile         -> REST API Kullanici Detay Profili")
    print("-> GET /api/jobs/{id}/author           -> REST API Ilani Yayinlayan Mezun Profili\n")
    server.serve_forever()
