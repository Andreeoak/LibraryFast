# LibraryFast - Digital Library API

**LibraryFast** is a modern RESTful API for managing a digital library, built with **FastAPI** and backed by **MongoDB Atlas**. It enables full CRUD operations and flexible filtering of books by title, author, category, and ratings.

## ✨ Features

* **CRUD Endpoints**: Create, read, update, and delete books
* **Dynamic Filtering**: Filter by title, author, category, and rating range
* **Data Validation**: Robust input validation using Pydantic
* **Modular Design**: Clean project structure with separation of concerns
* **MongoDB Atlas**: Cloud-hosted, scalable NoSQL database

## 🧰 Tech Stack

* Python 3.8+
* FastAPI
* MongoDB Atlas
* Pydantic
* pymongo
* python-dotenv
* Uvicorn (ASGI server)

## 📁 Project Structure

```
LibraryFast/
├── env/config/.env         # Environment variables
├── Database/ConnectDB.py   # MongoDB connection logic
├── Interfaces/ibook.py     # Book schema interfaces
├── Utils/validationRules.py# Validation rules
├── routes.py               # API endpoints
```

## ⚙️ Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/LibraryFast.git
   cd LibraryFast
   ```

2. **Create & activate virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # or env\Scripts\activate on Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`** in `env/config/.env`:

   ```env
   DB_USERNAME=your_user
   DB_PASSWORD=your_pass
   DB_CLUSTER=your_cluster
   DB_NAME=Library
   ```

5. **Run the app:**

   ```bash
   uvicorn routes:app --reload
   ```

## 📃 API Overview

### Create a Book

**POST** `/books/create/`

```json
{
  "title": "New Adventure",
  "author": "John Doe",
  "category": "Fiction",
  "description": "A thrilling tale.",
  "ratings": 4
}
```

### Get a Book by ID

**GET** `/books/{book_id}`

### Filter Books

**GET** `/books?title=...&author=...&category=...&min_rating=...&max_rating=...`

### Update a Book

**PUT** `/books/{book_id}/update/`

### Delete a Book

**DELETE** `/books/{book_id}/delete/`

## 🚀 Future Enhancements

* Add full-text indexes for faster filtering
* JWT-based user authentication
* Deployment with Gunicorn + Nginx

## ✍️ Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit and push: `git push origin feature/your-feature`
4. Open a Pull Request
