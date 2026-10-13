from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
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
    def _send(self, status, content_type, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(data)

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

        elif self.path == '/favicon.ico':
            self._send(204, 'text/plain', b'')

        else:
            self._send(404, 'text/plain', '404 Not Found')

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
    server.serve_forever()
