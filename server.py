from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, parse_qs
from datetime import datetime, timezone
import json
import os
from main import OPENAPI_SPEC, SWAGGER_HTML_TEMPLATE
from models.user import User
from models.announcement import Announcement
from models.job_posting import JobPosting
from models.job_application import JobApplication
from views.view import View
from routes import get_configured_router
from middlewares.logger_middleware import LoggerMiddleware
from middlewares.not_found_guardian_middleware import NotFoundGuardianMiddleware
from middlewares.server_error_guardian_middleware import ServerErrorGuardianMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure Unified MVC Router (Web & API routes)
router = get_configured_router()


def get_html_content(filename, replacements=None):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if replacements:
                for k, v in replacements.items():
                    content = content.replace(k, str(v))
            return content.encode('utf-8')
    if filename == 'index.html':
        return b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Main</title></head><body><h1>Temporary Main Page</h1><p>temporary one main page</p></body></html>"
    if filename == '404.html':
        return b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>Sayfa bulunamadi.</p><a href='/'>Ana Sayfa</a></body></html>"
    return b"<!DOCTYPE html><html><head><meta charset='utf-8'><title>About</title></head><body><h1>About Page</h1><p>temporary about page</p></body></html>"


class SimpleHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Default BaseHTTPRequestHandler logging suppressed in favor of LoggerMiddleware
        pass

    def _start_request_timer(self):
        if not hasattr(self, '_req_start_time'):
            self._req_start_time = LoggerMiddleware.start_timer()

    def _send(self, status, content_type, data):
        self._start_request_timer()
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(data)
        # Trigger Logger Middleware row output
        LoggerMiddleware.log(self.command, self.path, status, self._req_start_time)

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
        try:
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

            # Generic 404 Route: GET /404 -> 404.html
            if self.path in ['/404', '/404/']:
                self._send(404, 'text/html', get_html_content('404.html', {'{{REQUESTED_PATH}}': '404 - Sayfa Bulunamadı'}))
                return

            if self.path == '/favicon.ico':
                self._send(204, 'text/plain', b'')
                return

            # Dispatch through MVC Router:
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

            # 404 Guardian Middleware Handling
            status_code, ctype, err_body = NotFoundGuardianMiddleware.handle("GET", self.path, router=router)
            self._send(status_code, ctype, err_body)
        except Exception as e:
            status_code, ctype, err_body = ServerErrorGuardianMiddleware.handle(e, "GET", self.path)
            self._send(status_code, ctype, err_body)

    def do_POST(self):
        try:
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
                        LoggerMiddleware.log(self.command, self.path, 302, self._req_start_time)
                        return
                    self._send(200, 'application/json', json.dumps(result, ensure_ascii=False, indent=2))
                    return

            # 404 Guardian Middleware Handling
            status_code, ctype, err_body = NotFoundGuardianMiddleware.handle("POST", self.path, router=router)
            self._send(status_code, ctype, err_body)
        except Exception as e:
            status_code, ctype, err_body = ServerErrorGuardianMiddleware.handle(e, "POST", self.path)
            self._send(status_code, ctype, err_body)

    def do_PUT(self):
        try:
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

            # 404 Guardian Middleware Handling
            status_code, ctype, err_body = NotFoundGuardianMiddleware.handle("PUT", self.path, router=router)
            self._send(status_code, ctype, err_body)
        except Exception as e:
            status_code, ctype, err_body = ServerErrorGuardianMiddleware.handle(e, "PUT", self.path)
            self._send(status_code, ctype, err_body)

    def do_PATCH(self):
        try:
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

            # 404 Guardian Middleware Handling
            status_code, ctype, err_body = NotFoundGuardianMiddleware.handle("PATCH", self.path, router=router)
            self._send(status_code, ctype, err_body)
        except Exception as e:
            status_code, ctype, err_body = ServerErrorGuardianMiddleware.handle(e, "PATCH", self.path)
            self._send(status_code, ctype, err_body)

    def do_DELETE(self):
        try:
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

            # 404 Guardian Middleware Handling
            status_code, ctype, err_body = NotFoundGuardianMiddleware.handle("DELETE", self.path, router=router)
            self._send(status_code, ctype, err_body)
        except Exception as e:
            status_code, ctype, err_body = ServerErrorGuardianMiddleware.handle(e, "DELETE", self.path)
            self._send(status_code, ctype, err_body)

    def do_OPTIONS(self):
        self._start_request_timer()
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        LoggerMiddleware.log(self.command, self.path, 204, self._req_start_time)


if __name__ == '__main__':
    # Ensure database connection & verify entities exist
    try:
        user_count = len(User.find_all())
        announcement_count = len(Announcement.find_all())
        job_count = len(JobPosting.find_all())
        app_count = len(JobApplication.find_all())
        print(f"[DB] Baglanti saglandi. Mevcut kayitlar: {user_count} Kullanici, {announcement_count} Duyuru, {job_count} Is Ilani, {app_count} Basvuru.")
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
    print("-> GET /applications                   -> Web HTML Is Basvurulari Paneli")
    print("-> GET /api/users                      -> REST API Kullanicilar Listesi")
    print("-> GET /api/announcements              -> REST API Duyurular Listesi")
    print("-> GET /api/jobs                       -> REST API Is Ilanlari Listesi")
    print("-> GET /api/applications               -> REST API Is Basvurulari Listesi")
    print("-> GET /api/swagger                    -> Swagger UI Dokümantasyon")
    print("\n--- NESTED ROUTES (Hierarchical Relations) ---")
    print("-> GET /users/{id}/jobs                -> Web HTML Belirli Kullanicinin Ilanlari")
    print("-> GET /users/{id}/applications        -> Web HTML Belirli Kullanicinin Basvurulari")
    print("-> GET /jobs/{id}/applications         -> Web HTML Belirli Ilanin Basvurulari")
    print("-> GET /jobs/{id}/apply                -> Web HTML Ilan Basvuru Formu")
    print("-> GET /api/users/{id}/jobs            -> REST API Belirli Kullanicinin Ilanlari")
    print("-> POST /api/users/{id}/jobs           -> REST API Kullaniciya Bagli Ilan Ekle")
    print("-> GET /api/users/{id}/applications    -> REST API Kullanicinin Yaptigi Basvurular")
    print("-> GET /api/jobs/{id}/applications     -> REST API Ilana Gelen Basvurular")
    print("-> POST /api/jobs/{id}/applications    -> REST API Ilana Yeni Basvuru Yap")
    print("-> GET /api/jobs/{id}/author           -> REST API Ilani Yayinlayan Mezun Profili")
    print("-> GET /api/applications/{id}/job      -> REST API Basvurulan Ilan Detayi")
    print("-> GET /api/applications/{id}/applicant-> REST API Basvuran Aday Profili\n")
    server.serve_forever()
