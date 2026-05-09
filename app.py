from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import config
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from extensions import db, socketio
from models.user import User
from werkzeug.security import check_password_hash
from flask import redirect
from models.task import Task
from flask import jsonify
import pandas as pd
import numpy as np
from flask_login import current_user
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
socketio.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/')
def home():

    if current_user.is_authenticated:
        return redirect('/dashboard')

    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered"

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return "User Registered Successfully"

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')
@app.route('/dashboard')
@login_required
def dashboard():

    search = request.args.get('search', '')

    priority = request.args.get('priority', '')

    query = Task.query.filter_by(
        user_id=current_user.id
    )

    if search:

        query = query.filter(
            Task.title.ilike(f'%{search}%')
        )

    if priority:

        query = query.filter_by(
            priority=priority
        )

    tasks = query.order_by(
        Task.created_date.desc()
    ).all()

    return render_template(
        'dashboard.html',
        tasks=tasks
    )
@app.route('/add-task', methods=['POST'])
@login_required
def add_task():

    title = request.form['title']

    description = request.form['description']

    priority = request.form['priority']

    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        user_id=current_user.id
    )

    db.session.add(new_task)

    db.session.commit()
    socketio.emit('task_update', {
    'message': 'New task added'
})
    return redirect('/dashboard')
@app.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return "Unauthorized"

    db.session.delete(task)

    db.session.commit()
    socketio.emit('task_update', {
    'message': 'Task deleted'
})
    return redirect('/dashboard')
@app.route('/update-task/<int:task_id>')
@login_required
def update_task(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return "Unauthorized"

    task.status = "Completed"

    db.session.commit()
    socketio.emit('task_update', {
    'message': 'Task completed'
})
    return redirect('/dashboard')
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    task_list = []

    for task in tasks:

        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_date': str(task.created_date)
        }

        task_list.append(task_data)

    return jsonify(task_list)
@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task_api():

    data = request.get_json()

    new_task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        user_id=current_user.id
    )

    db.session.add(new_task)

    db.session.commit()

    return jsonify({
        'message': 'Task Created Successfully'
    })
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task_api(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return jsonify({
            'error': 'Unauthorized'
        }), 403

    db.session.delete(task)

    db.session.commit()

    return jsonify({
        'message': 'Task Deleted'
    })
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task_api(task_id):

    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        return jsonify({
            'error': 'Unauthorized'
        }), 403

    data = request.get_json()

    task.status = data['status']

    db.session.commit()

    return jsonify({
        'message': 'Task Updated'
    })
@app.route('/analytics')
@login_required
def analytics():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    task_data = []

    for task in tasks:

        task_data.append({
            'title': task.title,
            'priority': task.priority,
            'status': task.status
        })

    df = pd.DataFrame(task_data)

    total_tasks = len(df)

    completed_tasks = len(
        df[df['status'] == 'Completed']
    )

    pending_tasks = len(
        df[df['status'] == 'Pending']
    )

    completion_rate = 0

    if total_tasks > 0:

        completion_rate = (
            completed_tasks / total_tasks
        ) * 100

    high_priority_tasks = len(
        df[df['priority'] == 'High']
    )

    analytics_data = {
        'total_tasks': int(total_tasks),
        'completed_tasks': int(completed_tasks),
        'pending_tasks': int(pending_tasks),
        'completion_rate': round(completion_rate, 2),
        'high_priority_tasks': int(high_priority_tasks)
    }

    return jsonify(analytics_data)
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect('/login')
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True)