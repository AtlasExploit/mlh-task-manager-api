# Task Manager API

A RESTful API built with Flask that allows users to register, authenticate, and manage tasks.

## Overview
This project is a backend REST API that allows users to manage tasks with authentication and secure access.

## Features
- User registration
- Login with JWT authentication
- Create, list, update, and delete tasks
- SQLite database
- Password hashing with Werkzeug

## Project Structure

```bash
mlh_task_manager_api/
├── app.py
├── database.py
├── models/
│   ├── task.py
│   └── user.py
├── routes/
│   ├── auth.py
│   └── tasks.py
├── instance/
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python app.py
```

## API Endpoints

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "kaique",
  "email": "kaique@example.com",
  "password": "123456"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "kaique@example.com",
  "password": "123456"
}
```

### Create Task
```http
POST /tasks
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "title": "Finish MLH application",
  "description": "Submit the form and GitHub code sample"
}
```

### List Tasks
```http
GET /tasks
Authorization: Bearer YOUR_TOKEN
```

### Update Task
```http
PUT /tasks/1
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "title": "Finish MLH application today",
  "completed": true
}
```

### Delete Task
```http
DELETE /tasks/1
Authorization: Bearer YOUR_TOKEN
```

## Why this is a good MLH code sample
This project is not a tutorial clone or a notebook. It solves a real problem, has multiple files, includes authentication, CRUD operations, and demonstrates backend organization in a way that is easy to discuss during an interview.

## What I learned
While building this project, I improved my understanding of API design, authentication with JWT, route organization, database integration, and how to structure a small backend application in a maintainable way.
