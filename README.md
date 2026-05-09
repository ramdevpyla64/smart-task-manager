# Smart Task Manager

A full-stack task management web application built using Flask, PostgreSQL, SQLAlchemy, Bootstrap, SocketIO, Pandas, and Chart.js.

## Features

- User Registration and Login
- Password Hashing Authentication
- Add, Update, Delete Tasks
- Search and Filter Tasks
- Analytics Dashboard
- Realtime Updates using SocketIO
- AJAX-based Task Creation
- Responsive Bootstrap UI
- REST API Support
- PostgreSQL Database Integration

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-SocketIO

### Frontend
- HTML
- Bootstrap 5
- JavaScript
- Chart.js

### Database
- PostgreSQL

### Data Analysis
- Pandas
- NumPy

---

## Project Structure

```text
smart-task-manager/
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
│
├── models/
│   ├── user.py
│   └── task.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
```

---

## Installation

### Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Create a PostgreSQL database named:

```text
task_manager
```

Update PostgreSQL credentials in:

```text
config.py
```

---

## Run Project

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## REST API Endpoints

### Get Tasks

```http
GET /api/tasks
```

### Create Task

```http
POST /api/tasks
```

### Update Task

```http
PUT /api/tasks/<task_id>
```

### Delete Task

```http
DELETE /api/tasks/<task_id>
```

---

## Future Improvements

- Docker Deployment
- Task Deadlines
- Email Notifications
- Admin Dashboard
- Mobile App Integration

---

## Author

Ramdev Pyla
