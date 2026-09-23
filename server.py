from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    def do_GET(self):
        # 1. Ana Sayfa (Gerçek HTML Sayfası): GET / -> index.html
        if self.path in ['/', '', '/main', '/index.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html_content('index.html'))

        # 5. About Sayfası (Gerçek HTML Sayfası): GET /about -> about.html
        elif self.path in ['/about', '/about/', '/aout', '/aout/', '/about.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html_content('about.html'))

        # 'ok' endpointi: GET /ok veya GET /alumni -> 'ok'
        elif self.path in ['/ok', '/ok/', '/alumni', '/alumni/']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'ok')

        # 4. Task: GET /sum/{nm1}/{nm2} -> nm1 + nm2 toplamı
        elif self.path.startswith('/sum/'):
            parts = [p for p in unquote(self.path).strip('/').split('/') if p]
            if len(parts) == 3:
                try:
                    n1 = float(parts[1])
                    n2 = float(parts[2])
                    total = int(n1 + n2) if (n1 + n2).is_integer() else (n1 + n2)
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(str(total).encode('utf-8'))
                except ValueError:
                    self.send_response(400)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(b'Lutfen gecerli sayilar girin')
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'Kullanim: /sum/{sayi1}/{sayi2}')

        # 3. Task: GET /hello/{name} -> 'hello {name}'
        elif self.path.startswith('/hello/'):
            name = unquote(self.path[len('/hello/'):].strip('/'))
            if name:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"hello {name}".encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'hello world')

        # 2. Task: GET /hello -> 'hello world'
        elif self.path == '/hello':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'hello world')

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

if __name__ == '__main__':
    try:
        server = HTTPServer(('localhost', 80), SimpleHandler)
        print("Sunucu calisiyor: http://localhost")
        print("-> GET /                       -> index.html (Gercek Web Sayfasi)")
        print("-> GET /about                  -> about.html (Gercek Web Sayfasi)")
        print("-> GET /ok                     -> ok")
        print("-> GET /hello                  -> hello world")
        print("-> GET /hello/zehra            -> hello zehra")
        print("-> GET /sum/5/9                -> 14")
        server.serve_forever()
    except Exception as e:
        server = HTTPServer(('localhost', 8000), SimpleHandler)
        print("Sunucu calisiyor: http://localhost:8000")
        server.serve_forever()
