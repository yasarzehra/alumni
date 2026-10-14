from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from datetime import datetime, timezone
import json
import os
from main import OPENAPI_SPEC, SWAGGER_HTML_TEMPLATE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Bellekte tutulacak veri listesi (in-memory, veritabanı yok)
users_db = []
current_user_id = 1

def get_html_content(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().encode('utf-8')
    # Dosya bulunamazsa yedek HTML
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

    def _read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return None, "İstek gövdesi (body) boş olamaz"
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(body), None
        except Exception:
            return None, "Geçersiz JSON formatı"

    def do_GET(self):
        # 1. Ana Sayfa: GET / -> index.html (Temporary Main Page)
        if self.path in ['/', '', '/main', '/index.html']:
            self._send(200, 'text/html', get_html_content('index.html'))

        # 'ok' endpointi: GET /ok veya GET /alumni -> 'ok'
        elif self.path in ['/ok', '/ok/', '/alumni', '/alumni/']:
            self._send(200, 'text/plain', b'ok')

        # 5. About Sayfası: GET /about -> about.html
        elif self.path in ['/about', '/about/', '/aout', '/aout/', '/about.html']:
            self._send(200, 'text/html', get_html_content('about.html'))

        # 4. Task: GET /sum/{nm1}/{nm2} -> nm1 + nm2 toplamı
        elif self.path.startswith('/sum/'):
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

        # 2. Task: GET /hello -> 'hello world!'
        elif self.path in ['/hello', '/hello/']:
            self._send(200, 'text/plain', 'hello world!')

        # 3. Task: GET /hello/{name} -> 'hello, {name}'
        elif self.path.startswith('/hello/'):
            name = unquote(self.path[len('/hello/'):].strip('/'))
            if name:
                self._send(200, 'text/plain', f"hello, {name}")
            else:
                self._send(200, 'text/plain', 'hello world!')

        # Swagger UI Dokümantasyon Arayüzü: GET /api/swagger
        elif self.path in ['/api/swagger', '/api/swagger/']:
            self._send(200, 'text/html', SWAGGER_HTML_TEMPLATE)

        # Swagger / OpenAPI JSON Spesifikasyonu: GET /api/swagger.json veya /api/openapi.json
        elif self.path in ['/api/swagger.json', '/api/openapi.json']:
            self._send(200, 'application/json', json.dumps(OPENAPI_SPEC, ensure_ascii=False, indent=2))

        # 6. Task: GET /api/health -> JSON
        elif self.path in ['/api/health', '/api/health/', '/health', '/health/']:
            health_response = json.dumps({
                "status": "UP",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, ensure_ascii=False, indent=2)
            self._send(200, 'application/json', health_response)

        # GET /api/users -> In-memory kullanıcı listesi
        elif self.path in ['/api/users', '/api/users/']:
            self._send(200, 'application/json', json.dumps({
                "success": True,
                "count": len(users_db),
                "data": users_db
            }, ensure_ascii=False, indent=2))

        # GET /api/users/{id} -> Tekil kullanıcı
        elif self.path.startswith('/api/users/'):
            import re
            match = re.match(r'^/api/users/(\d+)$', self.path)
            if not match:
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": "Geçerli bir kullanıcı ID giriniz (örn: /api/users/1)"
                }, ensure_ascii=False, indent=2))
                return
            user_id = int(match.group(1))
            user = next((u for u in users_db if u["id"] == user_id), None)
            if not user:
                self._send(404, 'application/json', json.dumps({
                    "error": "NotFound",
                    "message": f"{user_id} ID'li kullanıcı bulunamadı"
                }, ensure_ascii=False, indent=2))
            else:
                self._send(200, 'application/json', json.dumps({
                    "success": True,
                    "data": user
                }, ensure_ascii=False, indent=2))

        elif self.path == '/favicon.ico':
            self._send(204, 'text/plain', b'')

        else:
            self._send(404, 'text/plain', '404 Not Found')

    def do_POST(self):
        global current_user_id
        # POST /api/users -> Yeni kullanıcı oluştur (In-Memory, veritabanı yok)
        if self.path in ['/api/users', '/api/users/']:
            data, err = self._read_json_body()
            if err:
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": err
                }, ensure_ascii=False, indent=2))
                return

            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                self._send(400, 'application/json', json.dumps({
                    "error": "BadRequest",
                    "message": "name ve email alanları zorunludur"
                }, ensure_ascii=False, indent=2))
                return

            if any(u.get("email", "").lower() == email.lower() for u in users_db):
                self._send(409, 'application/json', json.dumps({
                    "error": "Conflict",
                    "message": "Bu e-posta adresiyle kayıtlı bir kullanıcı zaten var"
                }, ensure_ascii=False, indent=2))
                return

            new_user = {
                "id": current_user_id,
                "name": name,
                "email": email,
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
            # Varsa diğer alanları da ekleyelim (örn. password)
            for k, v in data.items():
                if k not in new_user:
                    new_user[k] = v

            current_user_id += 1
            users_db.append(new_user)

            self._send(201, 'application/json', json.dumps({
                "success": True,
                "message": "Kullanıcı başarıyla oluşturuldu",
                "data": new_user
            }, ensure_ascii=False, indent=2))
            return

        self._send(404, 'application/json', json.dumps({
            "error": "NotFound",
            "message": "Endpoint bulunamadı"
        }, ensure_ascii=False, indent=2))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_PUT(self):
        import re
        match = re.match(r'^/api/users/(\d+)$', self.path)
        if not match:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": "Endpoint bulunamadı. Kullanım: PUT /api/users/{id}"
            }, ensure_ascii=False, indent=2))
            return

        user_id = int(match.group(1))
        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }, ensure_ascii=False, indent=2))
            return

        data, err = self._read_json_body()
        if err:
            self._send(400, 'application/json', json.dumps({
                "error": "BadRequest",
                "message": err
            }, ensure_ascii=False, indent=2))
            return

        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            self._send(400, 'application/json', json.dumps({
                "error": "BadRequest",
                "message": "PUT isteğinde name ve email alanları zorunludur"
            }, ensure_ascii=False, indent=2))
            return

        if any(u["email"].lower() == email.lower() and u["id"] != user_id for u in users_db):
            self._send(409, 'application/json', json.dumps({
                "error": "Conflict",
                "message": "Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor"
            }, ensure_ascii=False, indent=2))
            return

        user["name"] = name
        user["email"] = email
        user["updatedAt"] = datetime.now(timezone.utc).isoformat()

        self._send(200, 'application/json', json.dumps({
            "success": True,
            "message": "Kullanıcı başarıyla güncellendi",
            "data": user
        }, ensure_ascii=False, indent=2))

    def do_PATCH(self):
        import re
        match = re.match(r'^/api/users/(\d+)$', self.path)
        if not match:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": "Endpoint bulunamadı. Kullanım: PATCH /api/users/{id}"
            }, ensure_ascii=False, indent=2))
            return

        user_id = int(match.group(1))
        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }, ensure_ascii=False, indent=2))
            return

        data, err = self._read_json_body()
        if err:
            self._send(400, 'application/json', json.dumps({
                "error": "BadRequest",
                "message": err
            }, ensure_ascii=False, indent=2))
            return

        if not data:
            self._send(400, 'application/json', json.dumps({
                "error": "BadRequest",
                "message": "Güncellenecek en az bir alan gönderilmelidir"
            }, ensure_ascii=False, indent=2))
            return

        # Sadece gönderilen alanları güncelle
        if "name" in data:
            user["name"] = data["name"]

        if "email" in data:
            new_email = data["email"]
            if any(u["email"].lower() == new_email.lower() and u["id"] != user_id for u in users_db):
                self._send(409, 'application/json', json.dumps({
                    "error": "Conflict",
                    "message": "Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor"
                }, ensure_ascii=False, indent=2))
                return
            user["email"] = new_email

        user["updatedAt"] = datetime.now(timezone.utc).isoformat()

        self._send(200, 'application/json', json.dumps({
            "success": True,
            "message": "Kullanıcı başarıyla kısmen güncellendi",
            "data": user
        }, ensure_ascii=False, indent=2))

    def do_DELETE(self):
        global users_db
        import re
        match = re.match(r'^/api/users/(\d+)$', self.path)
        if not match:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": "Endpoint bulunamadı. Kullanım: DELETE /api/users/{id}"
            }, ensure_ascii=False, indent=2))
            return

        user_id = int(match.group(1))
        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send(404, 'application/json', json.dumps({
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }, ensure_ascii=False, indent=2))
            return

        users_db = [u for u in users_db if u["id"] != user_id]

        self._send(200, 'application/json', json.dumps({
            "success": True,
            "message": f"{user_id} ID'li kullanıcı başarıyla silindi"
        }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    port = 80
    try:
        server = ThreadingHTTPServer(('0.0.0.0', 80), SimpleHandler)
        print("Sunucu calisiyor: http://localhost")
    except Exception:
        port = 8000
        server = ThreadingHTTPServer(('0.0.0.0', 8000), SimpleHandler)
        print("Sunucu calisiyor: http://localhost:8000")

    print("-> GET /                       -> index.html (Temporary Main Page)")
    print("-> GET /about                  -> about.html (Gercek Web Sayfasi)")
    print("-> GET /ok                     -> ok")
    print("-> GET /hello                  -> hello world!")
    print("-> GET /hello/zehra            -> hello, zehra")
    print("-> GET /sum/5/9                -> 14")
    print("-> GET /api/health             -> JSON {\"status\": \"UP\", ...}")
    print("-> GET /api/swagger            -> Swagger UI Dokümantasyon")
    print("-> POST /api/users             -> JSON (Yeni kullanıcı ekleme)")
    print("-> GET /api/users              -> JSON (Kullanıcı listesi)")
    server.serve_forever()
