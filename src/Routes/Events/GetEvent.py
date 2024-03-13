from flask import Blueprint, jsonify
from src.Models.Events import Event
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('getEvent', __name__)


# Ruta encargada de obtener un evento por su ID
@main.get('api/event/<int:event_id>')
def get_event(event_id):
    try:
        # Buscar el evento por su ID en la base de datos
        event = Event.query.get(event_id)

        # Si el evento no existe, devolver un mensaje de error
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Devolver los datos del evento en formato JSON
        return jsonify({"message": "Event geted successfully",
                        "Event": {
                            "event_id": event.event_id,
                            "creator_id": event.creator_id,
                            "name": event.name,
                            "start_date": event.start_date,
                            "end_date": event.end_date,
                            "location": event.location
                        }}), 200

    except Exception as ex:
        # Registra cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error getting event. Please try again later"}), 500
