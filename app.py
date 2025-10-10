from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Habit, Completion
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.parse

app = Flask(__name__)
app.secret_key = "change_this_secret_in_prod"

# Database config - update if needed. Password was provided and URL-encoded below.
DB_USER = "root"
DB_PASS = urllib.parse.quote_plus("Brannel@55G")  # password provided; kept here encoded
DB_NAME = "habit_db"
DB_HOST = "localhost"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    if not logged_in():
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash("Provide username and password")
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('register'))
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Account created — please log in")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid credentials")
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    habits = Habit.query.filter_by(user_id=user.id).all()
    today = date.today().isoformat()
    completed_today = {c.habit_id for c in Completion.query.filter_by(date=date.today()).all()}
    return render_template('dashboard.html', user=user, habits=habits, today=today, completed_today=completed_today)

@app.route('/habit/add', methods=['GET','POST'])
def add_habit():
    if not logged_in():
        return redirect(url_for('login'))
    if request.method=='POST':
        name = request.form['name'].strip()
        note = request.form.get('note','').strip()
        if not name:
            flash("Name required")
            return redirect(url_for('add_habit'))
        habit = Habit(name=name, note=note, user_id=session['user_id'])
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('habit_form.html', action='Add', habit=None)

@app.route('/habit/edit/<int:hid>', methods=['GET','POST'])
def edit_habit(hid):
    if not logged_in():
        return redirect(url_for('login'))
    habit = Habit.query.get_or_404(hid)
    if habit.user_id != session['user_id']:
        flash("Not allowed")
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        habit.name = request.form['name'].strip()
        habit.note = request.form.get('note','').strip()
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('habit_form.html', action='Edit', habit=habit)

@app.route('/habit/delete/<int:hid>', methods=['POST'])
def delete_habit(hid):
    if not logged_in():
        return redirect(url_for('login'))
    habit = Habit.query.get_or_404(hid)
    if habit.user_id != session['user_id']:
        flash("Not allowed")
        return redirect(url_for('dashboard'))
    Completion.query.filter_by(habit_id=habit.id).delete()
    db.session.delete(habit)
    db.session.commit()
    flash("Habit deleted")
    return redirect(url_for('dashboard'))

@app.route('/habit/toggle/<int:hid>', methods=['POST'])
def toggle_habit(hid):
    if not logged_in():
        return redirect(url_for('login'))
    habit = Habit.query.get_or_404(hid)
    if habit.user_id != session['user_id']:
        return jsonify({'ok':False}), 403
    today = date.today()
    existing = Completion.query.filter_by(habit_id=habit.id, date=today).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'ok':True, 'status':'undone'})
    else:
        c = Completion(habit_id=habit.id, date=today)
        db.session.add(c)
        db.session.commit()
        return jsonify({'ok':True, 'status':'done'})

@app.route('/api/stats')
def api_stats():
    if not logged_in():
        return jsonify({'error':'unauthorized'}), 401
    user_id = session['user_id']
    from datetime import timedelta
    today = date.today()
    days = []
    counts = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        days.append(d.isoformat())
        cnt = Completion.query.join(Habit).filter(Habit.user_id==user_id, Completion.date==d).count()
        counts.append(cnt)
    return jsonify({'days':days, 'counts':counts})

if __name__ == '__main__':
    app.run(debug=True)
