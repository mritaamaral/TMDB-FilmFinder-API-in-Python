# 🎬 TMDB FilmFinder — Movie Search with Python & TMDB API

> An educational project for searching movies using the public The Movie Database (TMDB) API.

---

## 📖 About the Project

**TMDB FilmFinder** is a Python application that consumes the [TMDB API](https://www.themoviedb.org/documentation/api) to search and retrieve information about movies, such as title, overview, popularity, and poster. Built for educational purposes, this project serves as an introduction to consuming REST APIs with Python.

---

## ✨ Features

- 🔍 Search movies by title
- 📋 Display detailed information (title, overview, average rating, release date)
- 🖼️ Access movie poster paths
- 🌐 Integration with the TMDB REST API (v3)

---

## 🛠️ Technologies Used

| Technology | Description |
|---|---|
| Python 3 | Main programming language |
| Requests | HTTP requests library |
| TMDB API v3 | Movie data source |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher installed
- A [TMDB account](https://www.themoviedb.org/signup) to get a free API key

### 1. Clone the repository

```bash
git clone https://github.com/mritaamaral/TMDB-FilmFinder-API-in-Python.git
cd TMDB-FilmFinder-API-in-Python
```

### 2. Install dependencies

```bash
pip install requests
```

### 3. Set up your API key

Create a `.env` file or edit the configuration file with your key:

```python
API_KEY = "your_api_key_here"
```

> 💡 To get your free API key, visit [developer.themoviedb.org](https://developer.themoviedb.org/docs/getting-started) and follow the instructions.
Note: The .env file is listed in .gitignore and will not be uploaded to GitHub to protect your data.

### 4. Run the project

```bash
python main.py
```

---

## 📁 Project Structure

```
TMDB-FilmFinder-API-in-Python/
├── main.py          # Application entry point
├── README.md        # Project documentation
└── ...
```

---

## 📚 What I Learned

This project was built as part of my programming journey, covering concepts such as:

- Consuming REST APIs with Python
- Handling JSON responses
- Using the `requests` library
- Basic Python project organization

---

## 🙋‍♀️ Author

**Maria Rita Amaral**  
Aspiring developer, currently learning programming and building hands-on projects.

[![GitHub](https://img.shields.io/badge/GitHub-mritaamaral-181717?style=flat&logo=github)](https://github.com/mritaamaral)

---

## 📄 License

This project was built for educational purposes. Feel free to study and draw inspiration from the code! 😊

---

> *"Learning by building, one project at a time."*
