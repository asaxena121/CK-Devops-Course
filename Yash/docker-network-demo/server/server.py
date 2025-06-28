from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = "Hello from the Python Server!"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode())

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
