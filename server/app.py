from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify({"message": "list all workouts - not yet implemented"})


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    return jsonify({"message": f"show workout {id} - not yet implemented"})


@app.route('/workouts', methods=['POST'])
def create_workout():
    return jsonify({"message": "create workout - not yet implemented"}), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return jsonify({"message": f"delete workout {id} - not yet implemented"})


@app.route('/exercises', methods=['GET'])
def get_exercises():
    return jsonify({"message": "list all exercises - not yet implemented"})


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return jsonify({"message": f"show exercise {id} - not yet implemented"})


@app.route('/exercises', methods=['POST'])
def create_exercise():
    return jsonify({"message": "create exercise - not yet implemented"}), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return jsonify({"message": f"delete exercise {id} - not yet implemented"})


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    return jsonify({
        "message": f"add exercise {exercise_id} to workout {workout_id} - not yet implemented"
    }), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)