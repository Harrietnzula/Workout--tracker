from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    VALID_CATEGORIES = ('cardio', 'strength', 'flexibility', 'balance')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True
    )

    @validates('category')
    def validate_category(self, key, value):
        if value not in self.VALID_CATEGORIES:
            raise ValueError(
                f"category must be one of {self.VALID_CATEGORIES}, got '{value}'"
            )
        return value

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True
    )

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}, {self.duration_minutes} min>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: workout={self.workout_id}, exercise={self.exercise_id}>'


@event.listens_for(WorkoutExercise, 'before_insert')
@event.listens_for(WorkoutExercise, 'before_update')
def validate_at_least_one_metric(mapper, connection, target):
    """Ensure a WorkoutExercise carries at least one of reps, sets, or duration_seconds.

    Implemented as a SQLAlchemy event (rather than @validates) because it needs
    to check the object's final state right before it's written to the database,
    not just react to a single attribute being assigned.
    """
    if target.reps is None and target.sets is None and target.duration_seconds is None:
        raise ValueError(
            "WorkoutExercise must have at least one of reps, sets, or duration_seconds set"
        )