# URL Shortener

A backend service built using Flask that converts long URLs into short links and tracks usage analytics.

## 🚀 Features
- Short URL generation
- Redirection system
- SQLite database storage
- Click tracking (analytics)
- Stats API to view usage

## 🧠 How it works
1. User sends a long URL
2. System generates a unique short code
3. URL is stored in database
4. Accessing short link redirects to original URL
5. Click count is tracked and stored

## 🔗 APIs

### Create Short URL
POST /shorten

### Redirect
GET /<short_code>

### Get Stats
GET /stats/<short_code>

## 🛠 Tech Stack
- Python
- Flask
- SQLite