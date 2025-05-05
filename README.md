# 🔍 Cronos Search Engine

Cronos is a lightweight experimental search engine that crawls websites, stores page titles in a SQLite database, and enables basic keyword search. It was built as a learning project to explore Python, web scraping, and simple data search techniques.

This project consists of:
- A **Python crawler** and search logic
- A **Node.js Express server** to serve the search interface or run commands

---

## 📦 Features

- Crawl and store web page titles
- Basic keyword matching for search
- SQLite database for lightweight storage
- Node.js server integration (optional)

---

## 🛠️ Requirements

### Python

- Python 3.x
- `requests` library

Install dependencies:
```bash
pip install requests

### Node JS 
- npm install

Getting Started
 - Delete the Cronos Database within pythonscripts/database file if you want a clean start
 - Run the initialise.py in pythonscripts/database
 - Edit the crawler with your target website and run the crawler.py file. pythonscripts/crawler
 - On completion run the removedups.py in pythonscripts/database
 - Now you can run the node js webserver server/ - node server.js 
 - Go to localhost:3000/
