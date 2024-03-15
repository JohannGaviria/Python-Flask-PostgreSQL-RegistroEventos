from flask import Blueprint, jsonify
from src.Models.Events import Event
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('deleteEvent', __name__)


# Ruta encargada de eliminar un evento
@main.delete('api/event/<int:event_id>')
def delete_event(event_id):
    try:
        # Buscar el evento por su ID en la base de datos
        event = Event.query.get(event_id)

        # Si el evento no existe, devolver un mensaje de error
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        with db.session() as session:
            # Eliminar el evento de la base de datos
            session.delete(event)
            session.commit()

            # Devolver los datos del evento que se elimino
            return jsonify({"message": "Event deleted successfully",
                            "Event": {
                                "event_id": event.event_id,
                                "creator_id": event.creator_id,
                                "name": event.name,
                                "start_date": event.start_date,
                                "end_date": event.end_date,
                                "location": event.location,
                                "access_code": event.access_code
                            }}), 200

    except Exception as ex:
        # Registrar cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error deleting event. Please try again later"}), 500