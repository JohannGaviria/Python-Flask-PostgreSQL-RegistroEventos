from src.Utils.Database import db


# Definición de la clase Attendace, que representa la tabla de asistencias en la base de datos
class Attendance(db.Model):
    __tablename__ = 'attendances'

    # Columnas de la tabla attendances
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    # user = db.relationship("User", back_populates="attended_events")
    # event = db.relationship("Event", back_populates="attendees")

    # Constructor de la clase Attendance
    def __init__(self, user_id, event_id, registration_date):
        self.user_id = user_id
        self.event_id = event_id
        self.registration_date = registration_date
