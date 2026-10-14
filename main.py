import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

# Bellekte tutulacak veri listesi
users_db = []
current_id = 1

# OpenAPI / Swagger Spesifikasyonu
OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Alumni API Documentation",
        "version": "1.0.0",
        "description": "Alumni projesi için in-memory RESTful CRUD API ve Swagger arayüzü."
    },
    "paths": {
        "/api/health": {
            "get": {
                "tags": ["Sistem"],
                "summary": "Sağlık Kontrolü",
                "description": "Sunucu durumunu ve bellekteki kullanıcı sayısını döner.",
                "responses": {
                    "200": {
                        "description": "Sunucu çalışır durumda",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "UP",
                                    "timestamp": "2026-09-30T07:45:00Z",
                                    "totalUsersInMemory": 0
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/users": {
            "get": {
                "tags": ["API Users (/api/users)"],
                "summary": "Tüm Kullanıcıları Listele (ApiUserController.index)",
                "responses": {
                    "200": {
                        "description": "Kullanıcı listesi başarıyla getirildi",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "count": 1,
                                    "data": [
                                        {
                                            "id": 1,
                                            "name": "Zehra Yasar",
                                            "email": "zehra@example.com",
                                            "createdAt": "2026-09-30T07:40:00Z",
                                            "updatedAt": "2026-09-30T07:40:00Z"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["API Users (/api/users)"],
                "summary": "Yeni Kullanıcı Oluştur (ApiUserController.store)",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name", "email"],
                                "properties": {
                                    "name": {"type": "string", "example": "Zehra Yasar"},
                                    "email": {"type": "string", "example": "zehra@example.com"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Kullanıcı başarıyla oluşturuldu"},
                    "400": {"description": "Eksik veya geçersiz alanlar"},
                    "409": {"description": "E-posta adresi zaten mevcut"}
                }
            }
        },
        "/api/users/{id}": {
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                    "description": "Kullanıcı ID'si",
                    "example": 1
                }
            ],
            "get": {
                "tags": ["API Users (/api/users)"],
                "summary": "Tekil Kullanıcı Bilgisi Getir (ApiUserController.show)",
                "responses": {
                    "200": {"description": "Kullanıcı bulundu"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            },
            "put": {
                "tags": ["API Users (/api/users)"],
                "summary": "Kullanıcıyı Tam Güncelle (ApiUserController.update)",
                "description": "Kullanıcının name ve email alanlarını günceller.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name", "email"],
                                "properties": {
                                    "name": {"type": "string", "example": "Zehra Yasar (Guncellendi)"},
                                    "email": {"type": "string", "example": "zehra.yeni@example.com"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Kullanıcı başarıyla güncellendi"},
                    "400": {"description": "Eksik alan"},
                    "404": {"description": "Kullanıcı bulunamadı"},
                    "409": {"description": "E-posta çakışması"}
                }
            },
            "patch": {
                "tags": ["API Users (/api/users)"],
                "summary": "Kullanıcıyı Kısmen Güncelle (ApiUserController.update partial)",
                "description": "Yalnızca gönderilen alanları günceller.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "example": "Sadece Isim Degisti"},
                                    "email": {"type": "string", "example": "zehra.yeni@example.com"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Kullanıcı başarıyla kısmen güncellendi"},
                    "400": {"description": "Hiçbir alan gönderilmedi"},
                    "404": {"description": "Kullanıcı bulunamadı"},
                    "409": {"description": "E-posta çakışması"}
                }
            },
            "delete": {
                "tags": ["API Users (/api/users)"],
                "summary": "Kullanıcıyı Sil (ApiUserController.destroy)",
                "responses": {
                    "200": {"description": "Kullanıcı başarıyla silindi"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            }
        },
        "/users": {
            "get": {
                "tags": ["Web Users (/users)"],
                "summary": "Tüm Kullanıcıları Listele (UserController.index)",
                "description": "UserController.index() tarafından işlenir. Kullanıcıları HTML listesi olarak sunar.",
                "responses": {
                    "200": {
                        "description": "HTML web arayüzü"
                    }
                }
            },
            "post": {
                "tags": ["Web Users (/users)"],
                "summary": "Yeni Kullanıcı Oluştur (UserController.store)",
                "description": "UserController.store() tarafından işlenir. Web formundan kullanıcı kaydı oluşturur.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name", "email"],
                                "properties": {
                                    "name": {"type": "string", "example": "Web User"},
                                    "email": {"type": "string", "example": "webuser@example.com"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Kullanıcı başarıyla oluşturuldu"},
                    "400": {"description": "Eksik alanlar"}
                }
            }
        },
        "/users/create": {
            "get": {
                "tags": ["Web Users (/users)"],
                "summary": "Yeni Kullanıcı Oluşturma Formu (UserController.create)",
                "description": "HTML kullanıcı kayıt formunu döner [Create (C)].",
                "responses": {
                    "200": {"description": "HTML Kullanıcı Oluşturma Sayfası"}
                }
            }
        },
        "/users/{id}/edit": {
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                    "description": "Kullanıcı ID'si",
                    "example": 1
                }
            ],
            "get": {
                "tags": ["Web Users (/users)"],
                "summary": "Kullanıcı Düzenleme Formu (UserController.edit)",
                "description": "Mevcut kullanıcı bilgileriyle doldurulmuş düzenleme formunu döner [Update (U)].",
                "responses": {
                    "200": {"description": "HTML Kullanıcı Düzenleme Sayfası"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            }
        },
        "/users/{id}": {
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                    "description": "Kullanıcı ID'si",
                    "example": 1
                }
            ],
            "get": {
                "tags": ["Web Users (/users)"],
                "summary": "Tekil Kullanıcı Detayı (UserController.show)",
                "description": "UserController.show() tarafından işlenir.",
                "responses": {
                    "200": {"description": "HTML Kullanıcı Profil Sayfası"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            },
            "put": {
                "tags": ["Web Users (/users)"],
                "summary": "Kullanıcı Güncelle (UserController.update)",
                "responses": {
                    "200": {"description": "Kullanıcı güncellendi"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            },
            "delete": {
                "tags": ["Web Users (/users)"],
                "summary": "Kullanıcıyı Sil (UserController.destroy)",
                "responses": {
                    "200": {"description": "Kullanıcı silindi"},
                    "404": {"description": "Kullanıcı bulunamadı"}
                }
            }
        }
    }
}

SWAGGER_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Alumni API - Swagger UI</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  <style>
    body { margin: 0; padding: 0; background: #fafafa; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        spec: %s,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
""" % json.dumps(OPENAPI_SPEC)


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, status_code, data):
        response_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response_bytes)
        self.wfile.flush()

    def _send_html_response(self, status_code, html_str):
        response_bytes = html_str.encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response_bytes)
        self.wfile.flush()

    def _read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return None, "İstek gövdesi (body) boş olamaz"
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            return json.loads(body), None
        except Exception:
            return None, "Geçersiz JSON formatı"

    def _match_user_id(self):
        match = re.match(r'^/api/users/(\d+)$', self.path)
        if match:
            return int(match.group(1))
        return None

    # 1. GET İstekleri
    def do_GET(self):
        # Swagger UI Dokümantasyon Arayüzü
        if self.path in ('/api/swagger', '/api/swagger/'):
            self._send_html_response(200, SWAGGER_HTML_TEMPLATE)
            return

        # Swagger / OpenAPI JSON Spesifikasyonu
        if self.path in ('/api/swagger.json', '/api/openapi.json'):
            self._send_json_response(200, OPENAPI_SPEC)
            return

        # 1. Task: GET / -> 'ok'
        if self.path in ('/', '', '/ok'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', '2')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(b'ok')
            self.wfile.flush()
            return

        # 2. Task: GET /hello -> 'hello world!'
        if self.path in ('/hello', '/hello/'):
            msg = b'hello world!'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(msg)))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(msg)
            self.wfile.flush()
            return

        # 3. Task: GET /hello/{name} -> 'hello, {name}'
        if self.path.startswith('/hello/'):
            from urllib.parse import unquote
            name = unquote(self.path[len('/hello/'):].strip('/'))
            msg = f"hello, {name}".encode('utf-8') if name else b'hello world!'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(msg)))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(msg)
            self.wfile.flush()
            return

        # 4. Task: GET /sum/{nm1}/{nm2} -> nm1 + nm2
        if self.path.startswith('/sum/'):
            from urllib.parse import unquote
            parts = [p for p in unquote(self.path).strip('/').split('/') if p]
            if len(parts) == 3:
                try:
                    n1 = float(parts[1])
                    n2 = float(parts[2])
                    total = int(n1 + n2) if (n1 + n2).is_integer() else (n1 + n2)
                    msg = str(total).encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Content-Length', str(len(msg)))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.wfile.write(msg)
                    self.wfile.flush()
                    return
                except ValueError:
                    msg = b'Lutfen gecerli sayilar girin'
                    self.send_response(400)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Content-Length', str(len(msg)))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.wfile.write(msg)
                    self.wfile.flush()
                    return

        if self.path == '/api/health':
            self._send_json_response(200, {
                "status": "UP",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "totalUsersInMemory": len(users_db)
            })
            return

        if self.path == '/api/users':
            self._send_json_response(200, {
                "success": True,
                "count": len(users_db),
                "data": users_db
            })
            return

        user_id = self._match_user_id()
        if user_id is not None:
            user = next((u for u in users_db if u["id"] == user_id), None)
            if not user:
                self._send_json_response(404, {"error": "NotFound", "message": f"{user_id} ID'li kullanıcı bulunamadı"})
                return
            self._send_json_response(200, {"success": True, "data": user})
            return

        self._send_json_response(404, {"error": "NotFound", "message": "Endpoint bulunamadı"})

    # 2. POST İstekleri (Yeni Kullanıcı Ekleme)
    def do_POST(self):
        global current_id
        if self.path == '/api/users':
            data, err = self._read_json_body()
            if err:
                self._send_json_response(400, {"error": "BadRequest", "message": err})
                return

            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if not name or not email or not password:
                self._send_json_response(400, {
                    "error": "BadRequest",
                    "message": "name, email ve password alanları zorunludur"
                })
                return

            if any(u["email"].lower() == email.lower() for u in users_db):
                self._send_json_response(409, {
                    "error": "Conflict",
                    "message": "Bu e-posta adresiyle kayıtlı bir kullanıcı zaten var"
                })
                return

            new_user = {
                "id": current_id,
                "name": name,
                "email": email,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }
            current_id += 1
            users_db.append(new_user)
            self._send_json_response(201, {"success": True, "data": new_user})
            return

        self._send_json_response(404, {"error": "NotFound", "message": "Endpoint bulunamadı"})

    # 3. PUT İstekleri (Tam Güncelleme)
    def do_PUT(self):
        user_id = self._match_user_id()
        if user_id is None:
            self._send_json_response(404, {"error": "NotFound", "message": "Geçerli bir kullanıcı ID belirtmelisiniz (örn: /api/users/1)"})
            return

        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send_json_response(404, {"error": "NotFound", "message": f"{user_id} ID'li kullanıcı bulunamadı"})
            return

        data, err = self._read_json_body()
        if err:
            self._send_json_response(400, {"error": "BadRequest", "message": err})
            return

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            self._send_json_response(400, {
                "error": "BadRequest",
                "message": "PUT isteğinde tüm alanlar (name, email, password) eksiksiz gönderilmelidir"
            })
            return

        if any(u["email"].lower() == email.lower() and u["id"] != user_id for u in users_db):
            self._send_json_response(409, {
                "error": "Conflict",
                "message": "Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor"
            })
            return

        user["name"] = name
        user["email"] = email
        user["updatedAt"] = datetime.now(timezone.utc).isoformat()

        self._send_json_response(200, {
            "success": True,
            "message": "Kullanıcı başarıyla güncellendi (PUT)",
            "data": user
        })

    # 4. PATCH İstekleri (Kısmi Güncelleme)
    def do_PATCH(self):
        user_id = self._match_user_id()
        if user_id is None:
            self._send_json_response(404, {"error": "NotFound", "message": "Geçerli bir kullanıcı ID belirtmelisiniz (örn: /api/users/1)"})
            return

        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send_json_response(404, {"error": "NotFound", "message": f"{user_id} ID'li kullanıcı bulunamadı"})
            return

        data, err = self._read_json_body()
        if err:
            self._send_json_response(400, {"error": "BadRequest", "message": err})
            return

        if not data:
            self._send_json_response(400, {"error": "BadRequest", "message": "Güncellenecek en az bir alan göndermelisiniz"})
            return

        if "name" in data:
            user["name"] = data["name"]

        if "email" in data:
            new_email = data["email"]
            if any(u["email"].lower() == new_email.lower() and u["id"] != user_id for u in users_db):
                self._send_json_response(409, {
                    "error": "Conflict",
                    "message": "Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor"
                })
                return
            user["email"] = new_email

        user["updatedAt"] = datetime.now(timezone.utc).isoformat()

        self._send_json_response(200, {
            "success": True,
            "message": "Kullanıcı başarıyla kısmen güncellendi (PATCH)",
            "data": user
        })

    # 5. DELETE İstekleri (Kullanıcı Silme)
    def do_DELETE(self):
        global users_db
        user_id = self._match_user_id()
        if user_id is None:
            self._send_json_response(404, {"error": "NotFound", "message": "Geçerli bir kullanıcı ID belirtmelisiniz"})
            return

        user = next((u for u in users_db if u["id"] == user_id), None)
        if not user:
            self._send_json_response(404, {"error": "NotFound", "message": f"{user_id} ID'li kullanıcı bulunamadı"})
            return

        users_db = [u for u in users_db if u["id"] != user_id]
        self._send_json_response(200, {
            "success": True,
            "message": f"{user_id} ID'li kullanıcı başarıyla silindi"
        })

def run(port=3000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f"Sunucu calisiyor: http://localhost:{port}", flush=True)
    print(f"Swagger UI Dokumantasyonu: http://localhost:{port}/api/swagger", flush=True)
    print("Durdurmak icin: CTRL+C", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run(3000)
