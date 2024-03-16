from flask import Blueprint, jsonify, request
from src.Core.FormatDate import FormatDate
from src.Models.Attendances import Attendance
from src.Models.Events import Event
from src.Models.Participants import Participant
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc
from datetime import datetime


main = Blueprint('scanCode', __name__)


# Ruta encargada de escanear los codigos
@main.post('api/event/<int:event_id>/scanCode/<int:user_id>')
def scan_code(event_id, user_id):
    try:
        # Obtener los datos en formato JSON enviados en la solicitud
        join_code = request.json.get('join_code')

        # Verificar si el evento existe
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        # Verificar si el usuario está registrado para el evento
        participant = Participant.query.filter_by(event_id=event_id, user_id=user_id).first()
        if not participant:
            return jsonify({"message": "User not registered for this event"}), 403
        
        # Verificar si el código escaneado coincide con el código de union
        # participant = Participant.query.get(user_id)
        if not join_code == participant.join_code:
            return jsonify({"message": "Join code is incorrect"}), 403
        
        # Verificar si el evento ya ha comenzado
        current_time = datetime.now()
        if current_time < event.start_date:
            return jsonify({"message": "The event has not started yet"}), 403
        
        # Vereficar si el usuario ya ingreso al evento
        attendance = Attendance.query.filter_by(user_id=user_id).first()
        if attendance:
            return jsonify({"message": "The user has already entered the event"}), 409
        
        registration_date = FormatDate.format_date(current_time)
        
        with db.session() as session:
            # Registrar la asistencia del usuario al evento
            new_attendaces = Attendance(user_id, event_id, registration_date)
            session.add(new_attendaces)
            session.commit()

            return jsonify({"message": "Access to event granted",
                            "Attendaces": {
                                "attendance_id": new_attendaces.attendance_id,
                                "user_id": new_attendaces.user_id,
                                "event_id": new_attendaces.event_id,
                                "registration_date": new_attendaces.registration_date
                            }}), 200

    except Exception as ex:
        # Registras cualquier excepción durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error scanning code. Please try agai later"}), 500