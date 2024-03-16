from src.Utils.Database import db


# Definición de la clase Participant, que representa la tabla de participantes en la base de datos
class Participant(db.Model):
    __tablename__ = 'participants'

    # Columnas de la tabla participants
    participant_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    join_code = db.Column(db.String(9), unique=True)

    # Constructor de la clase Attendance
    def __init__(self, user_id, event_id, join_code):
        self.user_id = user_id
        self.event_id = event_id
        self.join_code = join_code
