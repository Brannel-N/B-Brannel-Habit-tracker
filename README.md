# My Habit Tracker (Flask + MySQL)

A simple habit tracker web app built with Flask and MySQL.  
This project was prepared for you with your MySQL password included in `app.py` for convenience —

## What's included
- Flask backend with SQLAlchemy models
- User registration & login (session-based)
- Add / Edit / Delete habits
- Mark daily completion
- 14-day progress chart (Chart.js)
- `db_init.py` script to create the database and tables

## Requirements
- Python 3.8+
- MySQL server
- On Windows: ensure MySQL server is running and accessible

## Quick setup (Windows)
1. How it runs
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the database and tables:
   ```bash
   python db_init.py
   ```
   This will create a database named `habit_db` (default). If you'd like another name, edit `db_init.py` and `app.py`.

5. Run the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## GitHub
To push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - habit tracker"
# create repo on GitHub and follow instructions, or:
git remote add origin https://github.com/<yourname>/<repo>.git
git branch -M main
git push -u origin main
```


