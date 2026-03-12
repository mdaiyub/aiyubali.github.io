#!/usr/bin/env python3
"""
Serve the `site/` directory at the server root.

Usage:
  python3 serve_site.py [PORT]

This script maps requests for `/...` to `site/...` so the site is available
directly at http://localhost:PORT/ without moving files or adding redirects.
"""
import http.server
import socketserver
import os
import sys


class SiteRootHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Remove query and fragment
        path = path.split('?', 1)[0].split('#', 1)[0]
        # Map root or / to site/index.html
        if path == '/' or path == '':
            rel = 'index.html'
        else:
            rel = path.lstrip('/')
        site_dir = os.path.join(os.getcwd(), 'site')
        full_path = os.path.join(site_dir, rel)
        return full_path


def run(port=8000):
    handler = SiteRootHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        sa = httpd.socket.getsockname()
        print(f"Serving site/ at http://{sa[0] or 'localhost'}:{sa[1]}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down')
            httpd.server_close()


if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run(port)
