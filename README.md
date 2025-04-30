#  Least-Connections Load Balancer (HTTP-based web service with a front-end load balancer distributing REST API calls)

This project is implementation of load balancer with the Least Connections algorithm. It distributes HTTP requests from 
frontend among different backend servers using Python sockets. This application configured on local machine, 
all instances run on different ports.

## 📁 Project Structure

```
least-connections_load_balancer/
│
├── balancer/
│   ├── balancer.py
│   ├── requirements.txt
│   └── traffic_visualizer.py
│
├── frontend-app/
│   ├── index.html
│   ├── main.js
│   ├── styles.css
│   └── icon.ico
│
├── server/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── image1.jpg
│       ├── image2.jpg
│       ├── image3.jpg
│       └── image4.jpg
│
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project

### 1. Start the Frontend

Use a **Live Server** (e.g. [Live Server extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)) or Python's built-in HTTP server:

```
cd frontend-app
python -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

---

### 2. Start Backend Servers

You can start multiple backend servers on different ports. Example for two:

```
python server/app/main.py 8002
python server/app/main.py 8003
```

---

### 3. Start the Load Balancer

Pass all backend server addresses to the load balancer:

```
python balancer/balancer.py 127.0.0.1:8002 127.0.0.1:8003
```

By default, it runs on `127.0.0.1:8001`.

---

### 4. Use the Frontend

Now you can send requests from the frontend UI — they will be routed to backend servers via the load balancer.

---

## 🛠️ Requirements

- Python 3.x
- Modern web browser
- Live Server (extension or Python's `http.server`)

---

## ✅ Example Workflow

```
# Terminal 1: Backend servers
python server/app/main.py 8002
python server/app/main.py 8003

# Terminal 2: Load balancer
python balancer/balancer.py 127.0.0.1:8002 127.0.0.1:8003

# Terminal 3: Frontend
cd frontend-app
python -m http.server 8080

# Open http://localhost:8080 in browser
```

---

## 📌 Notes

- All components run on `localhost`. You can configure them to run on different hosts or ports if needed.
- Use as many servers as you like — just add them to the load balancer command.
