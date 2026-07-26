#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    push_up = Exercise(name="Push-up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="flexibility", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)

    db.session.add_all([push_up, squat, plank, running, bench_press])
    db.session.commit()

    print("Seeding workouts...")
    workout_1 = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Morning full-body session")
    workout_2 = Workout(date=date(2026, 7, 22), duration_minutes=30, notes="Quick cardio burst")
    workout_3 = Workout(date=date(2026, 7, 24), duration_minutes=60, notes=None)

    db.session.add_all([workout_1, workout_2, workout_3])
    db.session.commit()

    print("Seeding workout_exercises (linking workouts and exercises)...")
    we_1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3)
    we_2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=squat.id, reps=12, sets=4)
    we_3 = WorkoutExercise(workout_id=workout_1.id, exercise_id=plank.id, duration_seconds=60)
    we_4 = WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, duration_seconds=1200)
    we_5 = WorkoutExercise(workout_id=workout_3.id, exercise_id=bench_press.id, reps=8, sets=5)
    we_6 = WorkoutExercise(workout_id=workout_3.id, exercise_id=push_up.id, reps=20, sets=2)

    db.session.add_all([we_1, we_2, we_3, we_4, we_5, we_6])
    db.session.commit()

    print("Seeding complete!")