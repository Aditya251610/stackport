from http.server import BaseHTTPRequestHandler, HTTPServer


class TestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/hello":
            body = b"Hello from Stackport"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/echo":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        print(f"[APP] {format % args}", flush=True)


def main():
    server = HTTPServer(("127.0.0.1", 8000), TestHandler)

    print("Test application started on http://127.0.0.1:8000", flush=True)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("Test application stopping...", flush=True)

    finally:
        server.server_close()
        print("Test application stopped", flush=True)


if __name__ == "__main__":
    main()