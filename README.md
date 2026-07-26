# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend API for a workout tracking application used by personal trainers. The API tracks workouts and their associated exercises, including reps, sets, and duration for each exercise performed within a workout.

## Description

This backend supports:
- Creating, viewing, and deleting **workouts**
- Creating, viewing, and deleting **exercises** (reusable across workouts)
- Adding an exercise to a workout, along with reps, sets, and/or duration for that specific instance

The data model uses a `WorkoutExercise` join table to connect workouts and exercises many-to-many, while also storing per-instance details (reps/sets/duration) that vary each time an exercise is performed within a workout.

## Tech Stack

- Python 3.11
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Harrietnzula/Workout--tracker.git
   cd Workout--tracker
   ```

2. Install dependencies with Pipenv:
   ```
   pipenv install
   pipenv shell
   ```

3. Navigate into the server directory:
   ```
   cd server
   ```

4. Set the Flask app environment variable:
   ```
   set FLASK_APP=app.py
   ```
   (On macOS/Linux, use `export FLASK_APP=app.py` instead.)

5. Run database migrations:
   ```
   flask db upgrade head
   ```

6. Seed the database with example data:
   ```
   python seed.py
   ```

## Running the App

From inside the `server/` directory (with the pipenv shell activated):
```
python app.py
```

The API will be available at `http://127.0.0.1:5555`.

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a single workout, including its associated exercises with reps/sets/duration |
| POST | `/workouts` | Create a new workout (`date`, `duration_minutes`, `notes`) |
| DELETE | `/workouts/<id>` | Delete a workout and its associated workout_exercise records |

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show a single exercise |
| POST | `/exercises` | Create a new exercise (`name`, `category`, `equipment_needed`) |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated workout_exercise records |

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout, with `reps`, `sets`, and/or `duration_seconds` |

## Validations

**Table Constraints**
- `Exercise.name` is unique
- `Workout.duration_minutes` must be greater than 0 (database check constraint)

**Model Validations**
- `Exercise.category` must be one of: `cardio`, `strength`, `flexibility`, `balance`
- `WorkoutExercise` must have at least one of `reps`, `sets`, or `duration_seconds` set

**Schema Validations**
- `Exercise.category` must be one of the allowed categories (mirrors model validation, enforced at the API layer)
- `Workout.duration_minutes` must be at least 1 (mirrors table constraint, enforced at the API layer)

## Resetting the Database

To wipe and reseed the database at any point:
```
python seed.py
```
This clears all existing records and recreates a fresh, consistent set of example data.