from flask import Flask, request, jsonify
import importlib
try:
    flask_migrate = importlib.import_module('flask_migrate')
    Migrate = flask_migrate.Migrate
except ImportError:
    # flask_migrate may not be installed in some environments (IDE linting, CI).
    # Provide a no-op fallback so the app can still run without migrations.
    def Migrate(app=None, db=None):
        return None

try:
    marshmallow = importlib.import_module('marshmallow')
    ValidationError = marshmallow.ValidationError
except ImportError:
    class ValidationError(Exception):
        def __init__(self, messages=None):
            self.messages = messages or {}

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# ---------- WORKOUTS ----------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": f"Workout {id} not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        validated_data = workout_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    workout = Workout(
        date=validated_data['date'],
        duration_minutes=validated_data['duration_minutes'],
        notes=validated_data.get('notes'),
    )

    try:
        db.session.add(workout)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": f"Workout {id} not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": f"Workout {id} deleted successfully"}), 200


# ---------- EXERCISES ----------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": f"Exercise {id} not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    exercise = Exercise(
        name=validated_data['name'],
        category=validated_data['category'],
        equipment_needed=validated_data.get('equipment_needed', False),
    )

    try:
        db.session.add(exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": f"Exercise {id} not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": f"Exercise {id} deleted successfully"}), 200


# ---------- WORKOUT EXERCISES (join) ----------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": f"Workout {workout_id} not found"}), 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": f"Exercise {exercise_id} not found"}), 404

    data = request.get_json() or {}
    try:
        validated_data = workout_exercise_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=validated_data.get('reps'),
        sets=validated_data.get('sets'),
        duration_seconds=validated_data.get('duration_seconds'),
    )

    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)