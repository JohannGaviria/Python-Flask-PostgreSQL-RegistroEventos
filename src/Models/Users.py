from src.Utils.Database import db


# Definición de la clase User, que representa la tabla de usuarios en la base de datos
class User(db.Model):
    __tablename__ = 'users'

    # Columnas de la tabla users
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identification_document = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    # attended_events = db.relationship("Attendance", back_populates="user")
    # created_events = db.relationship("Event", back_populates="creator_user")

    # Constructor de la clase User
    def __init__(self, name, identification_document, email, password, phone):
        self.name = name
        self.identification_document = identification_document
        self.email = email
        self.password = password
        self.phone = phone
