from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3

def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open("signup.html", "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/signup":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            form_data = urllib.parse.parse_qs(post_data.decode("utf-8"))

            username = form_data.get("username", [""])[0]
            email = form_data.get("email", [""])[0]
            password = form_data.get("password", [""])[0]

            # data database me save karna
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            conn.commit()
            conn.close()

            # browser response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            message = f"""
            <html><body>
            <h2>Signup Successful!</h2>
            <p>Welcome, {username}</p>
            <a href="/">Go Back</a>
            </body></html>
            """
            self.wfile.write(message.encode("utf-8"))
        else:
            self.send_error(404, "Path not found")

def run():
    setup_database()  # pehle database aur table bana lo
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running at: http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
