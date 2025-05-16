# 🎬 MoviWeb App

MoviWeb is a Flask web application that lets users create and manage personalized movie collections. It integrates with the OMDb API to autofill movie details, including posters and blurbs, with full CRUD support and clean UI styling.

---

## 🔧 Features

- ✅ Add users and view individual movie lists
- ✅ Search for movies using fuzzy OMDb matching
- ✅ Confirm OMDb data before adding
- ✅ Edit movies manually or via OMDb re-search
- ✅ View full movie details with poster and plot
- ✅ Delete movies with confirmation
- ✅ Responsive layout using pure CSS and Flexbox
- ✅ Environment-safe OMDb API integration

---

## 🚀 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/moviweb_app.git
cd moviweb_app
```

2. **Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**

```env
OMDB_API_KEY=your_omdb_api_key_here
```

5. **Run the app**

```bash
python app.py
```

Then visit [http://localhost:5000](http://localhost:5000)

---

## 🛠 Tech Stack

- Python 3
- Flask
- SQLAlchemy (SQLite)
- Jinja2
- OMDb API
- HTML/CSS (Flexbox-based)

---

## 📁 Folder Structure

```
.
├── app.py
├── omdb_utils.py
├── sqlite_data_manager.py
├── templates/
│   └── *.html
├── static/
│   └── style.css
├── moviwebapp.db
├── requirements.txt
├── .env
└── README.md
```

---

## 📌 Notes

- The app avoids JavaScript and is fully functional using multi-step forms.
- The OMDb integration uses a search-first strategy (`s=`) to find likely matches, then retrieves detailed data via IMDb ID (`i=`).
- Designed for fast iteration and extendable functionality (e.g., CSV export, user accounts, rating filters).

---

## ✅ Status

Project is fully functional and ready for refinement or deployment.