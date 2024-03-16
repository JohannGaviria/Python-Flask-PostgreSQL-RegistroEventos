from flask import Blueprint, jsonify, request
from src.Models.Participants import Participant
from src.Models.Events import Event
from src.Models.Users import User
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('eventRegister', __name__)


# Ruta encargada de registrar un usuario en un evento
@main.post('api/event/<int:event_id>/register/<int:user_id>')
def event_register(event_id, user_id):
    try:
        # Obtener los datos en formato JSON eviados en la solicitud
        access_code = request.json.get('access_code')

        # Buscar el evento por su ID en la base de datos
        event = Event.query.get(event_id)

        # Buscar el usuario por su ID en la base de datos
        user = User.query.get(user_id)

        # Si el evento no existe, devolver un mensaje de error
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Si el usuario no existe, devolver un mensaje de error
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        # Si el codigo de acceso no es igual al codigo de acceso de la base de datos
        if access_code != event.access_code:
            return jsonify({"message": "Access code is incorrect"}), 403
        
        # Si el usuario ya se registro al evento
        participant = Participant.query.filter_by(user_id=user_id).first()
        if participant:
            return jsonify({"message": "The user has already registered for the event"}), 409
        
        with db.session() as session:
            new_participant = Participant(user_id, event_id, join_code=None)
            session.add(new_participant)
            session.commit()

            return jsonify({"message": "registration for the event successfully",
                            "Event Register": {
                                "participant_id": new_participant.participant_id,
                                "user_id": new_participant.user_id,
                                "event_id": new_participant.event_id
                            }}), 200
        
    except Exception as ex:
        # Registrar cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error registering in event. Please try again later"}), 500