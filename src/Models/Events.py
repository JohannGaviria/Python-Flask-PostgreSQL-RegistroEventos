from src.Utils.Database import db


# Definición de la clase Event, que representa la tabla de eventos en la base de datos
class Event(db.Model):
    __tablename__ = 'events'

    # Columnas de la tabla events
    event_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)

    # creator_user = db.relationship("User", back_populates="events_created")
    # attendees = db.relationship("Attendance", back_populates="event")

    # Constructor de la clase Event
    def __init__(self, creator_id,name, start_date, end_date, location):
        self.creator_id = creator_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location