# 🕸️ Python Mini HTTP Server — From Scratch

This project shows how to build an HTTP server **from scratch** in Python using just `socket` — step by step, without any external frameworks.  
The goal: to deeply understand **HTTP**, **sockets**, and how real web servers work under the hood.

📁 The project is split into **4 levels**, each in its own folder, with increasing complexity and features.

---

## 📚 Project Structure

```

.
├── level0/   # Simplest possible HTTP server: 1 file, 1 connection
├── level1/   # Basic HTTP server: handle requests, respond manually
├── level2/   # Multi-client support with threads + cleaner routing
├── level3/   # Routing system + static file serving (HTML, CSS)
├── level4/   # Form handling, POST support, basic templating

````

---

## 🧩 Level-by-Level Overview

---

### 🟣 Level 0 — The Bare Minimum Server

📄 `level0/server.py`

> This is the absolute simplest HTTP server you can write in Python.

- Listens on `localhost:9000`
- Accepts only one connection at a time
- Reads the HTTP request and prints it
- Responds with hardcoded HTML (`<h1>Hello from scratch!</h1>`)
- No error handling, no routing, no file serving — just pure socket logic

**Key code:**

```python
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
try:
    server_socket.bind(('localhost', 9000))
    server_socket.listen(50)

    while True:
        client_connection, address = server_socket.accept()
        request = client_connection.recv(5000).decode()
        print("\n--- Request Received ---")
        print(request)

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Hello from scratch!</h1></body></html>"
        )
        client_connection.sendall(response.encode())
        client_connection.close()
except KeyboardInterrupt:
    print("\nShutting down the server...")
    server_socket.close()
````

---

### 🟢 Level 1 — Minimal HTTP Server

> The most basic HTTP server, written with raw sockets.

- Listens on `localhost:9000`
- Accepts one request at a time
- Responds with a hardcoded HTML string
- No routing, no files — just returns "Hello World" or similar

**Key Code:**
```python
request = client_connection.recv(1024).decode()
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "\r\n"
    "<h1>Hello, world!</h1>"
)
client_connection.sendall(response.encode())
````

---

### 🟡 Level 2 — Multithreading & Clean Code

> Adds support for **multiple clients** using threads and organizes logic into functions.

* Handles multiple clients concurrently (one thread per client)
* Extracts path and method from the HTTP request
* Adds a `handle_client()` function
* Logs each request to the console

**Key Concepts:**

* `threading.Thread(...)` to allow multiple connections
* Modular functions: `parse_request()`, `handle_request()`, etc.

```python
threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
```

---

### 🟠 Level 3 — Static Files + Mini Router

> Now it's feeling like a real web server!

* Adds a **decorator-based router**: `@route('/about')`
* Serves **static files** (HTML, CSS) from a `/public` folder
* Detects MIME types (text/html, text/css, images…)

**Key Features:**

* `mimetypes.guess_type()` to auto-detect Content-Type
* File-based responses from disk
* Serves paths like `/static/style.css` or `/about`

**Key Code:**

```python
@route('/about')
def about():
    return serve_file('about.html')
```

```python
if path.startswith('/static/'):
    filename = path.replace('/static/', '')
    response = serve_file(filename)
```

---

### 🔴 Level 4 — Forms, POST, and Templates

> This level introduces **user interaction** and dynamic content.

* Handles `POST` requests and reads form data
* Implements **HTML templating** with `{{variable}}` injection
* Renders a thank-you page after form submission
* Uses `/templates` for HTML files and `/public` for CSS

**Key Code:**

```python
def contact_submit(form_data):
    name = form_data.get('name', 'anonymous')
    return render_template('thankyou.html', {'name': name})
```

```html
<!-- thankyou.html -->
<h1>Thank you, {{name}}!</h1>
```

---

## 🔧 How to Run

Each level can be run separately:

```bash
cd level_1-..  # or level_2, level_3, level_4
python server.py
```

Then open your browser at [http://localhost:9000](http://localhost:9000)

---

## 🌟 Why This Project?

This project is:

* A **learning playground** — see what’s behind Flask or FastAPI
* A **resume-worthy repo** — shows core networking & HTTP understanding
* A **solid foundation** if you want to write your own lightweight web framework

---

## 🚀 Ideas for Next Levels (might get back to it later)

* ✅ Save form data to `.txt` or `.json`
* ✅ Add session tracking using cookies
* 🧠 Build an `/api/messages` REST endpoint
* 🛡️ Add input validation & error pages
* 📦 Eventually switch to `asyncio` for non-blocking I/O

---

## 👨‍💻 Author

Made with ❤️ by Mohammad Bensaid
Feel free to fork, star, and experiment!
