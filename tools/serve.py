"""Local preview server with the same clean URLs as .htaccess on Hostinger (/x and /en/x).
    python3 tools/serve.py            (http://127.0.0.1:8765/trangchu)
"""
import http.server, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = next((int(a) for a in sys.argv[1:] if a.isdigit()), 8765)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _redirect(self, to):
        self.send_response(301)
        self.send_header('Location', to)
        self.end_headers()

    def do_GET(self):
        path, _, query = self.path.partition('?')
        q = ('?' + query) if query else ''
        if path in ('/', ''):
            return self._redirect('/trangchu' + q)
        if path == '/index.html':
            return self._redirect('/trangchu' + q)
        m = re.fullmatch(r'/([a-z0-9-]+)\.html', path)
        if m:
            return self._redirect('/' + m.group(1) + q)
        if re.match(r'/(tools|data|\.git)(/|$)', path):
            return self.send_error(403)
        if path in ('/en', '/en/', '/en/trangchu', '/en/trangchu/'):
            return self._redirect('/en/home' + q)
        m = re.fullmatch(r'/(en/)?([a-z0-9-]+)\.html', path)
        if m and m.group(1):
            return self._redirect('/en/' + m.group(2) + q)
        m = re.fullmatch(r'/(en/)?([a-z0-9-]+)/?', path)
        if m:
            name = 'index' if m.group(2) == 'trangchu' and not m.group(1) else m.group(2)
            if os.path.isfile(os.path.join(ROOT, (m.group(1) or '') + name + '.html')):
                self.path = '/' + (m.group(1) or '') + name + '.html' + q
        return super().do_GET()


if __name__ == '__main__':
    print(f'http://127.0.0.1:{PORT}/trangchu')
    http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
