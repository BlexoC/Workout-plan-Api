# Workout Log API

## Project Description

A secure Flask REST API backend for a productivity tool that lets users track
their personal workout history. Users can sign up, log in, and manage their
own workout log entries (title, category, duration, date, and notes).
Authentication is handled with JWT (JSON Web Tokens) via
`flask-jwt-extended`, passwords are hashed with `flask-bcrypt`, and every
workout log route is scoped to the logged-in user so no one can view or
modify another user's records.

## Endpoints

### Auth

| Method | Route     | Auth required 
|--------|-----------|:--------------:
| POST   | `/signup` | No              
| GET    | `/me`     | Yes             
### Workout Logs (user-owned resource)

All routes below require a valid JWT and only ever return/modify workout
logs belonging to the authenticated user. Requesting or modifying another
user's log (or one that doesn't exist) returns a `404`.

| Method | Route                 | Auth required  
|--------|-----------------------|:--------------:
| GET    | `/workout_logs`       | Yes              
| POST   | `/workout_logs`       | Yes             
| GET    | `/workout_logs/<id>`  | Yes                                    
| PATCH  | `/workout_logs/<id>`  | Yes                     
| DELETE | `/workout_logs/<id>`  | Yes             
### Example: paginated response shape



## Project Structure
workout-log-api/
├── .venv/
├── server/
│   ├── migrations/
│   ├── app.db
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── pipfile
│   ├── requirements.txt
│   └── seed.py
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md


