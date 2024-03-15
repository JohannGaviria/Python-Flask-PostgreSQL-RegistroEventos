from flask import Blueprint, jsonify, request
from src.Core.FormatDate import FormatDate
from src.Core.ValidateEvent import EventsForm
from src.Models.Events import Event
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('updateEvent', __name__)


# Ruta encargada de actualizar un evento
@main.put('api/event/<int:event_id>')
def update_event(event_id):
    try:
        # Buscar el evento por su ID en la base de datos
        event = Event.query.get(event_id)

        # Si el evento no existe, devolver un mensaje de error
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Obtener los datos en formato JSON enviados en la solicitud
        data = request.get_json()

        # Validar los datos del evento
        form = EventsForm(data=data)

        # Si los datos son correctos
        if form.validate():
            # Obtener los datos
            creator_id = form.creator_id.data
            name = form.name.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            location = form.location.data

            # Formatear las fechas
            start_date = FormatDate.format_date(start_date)
            end_date = FormatDate.format_date(end_date)

            # Actualizar los datos del evento
            event.creator_id = creator_id
            event.name = name
            event.start_date = start_date
            event.end_date = end_date
            event.location = location

            with db.session() as session:
                # Guardar el nuevo evento en la base de datos
                session.commit()

                # Devolver los datos del evento
                return jsonify({"message": "Event updated successfully",
                                "Event": {
                                    "event_id": event.event_id,
                                    "creator_id": event.creator_id,
                                    "name": event.name,
                                    "start_date": event.start_date,
                                    "end_date": event.end_date,
                                    "location": event.location,
                                    "access_code": event.access_code
                                }}), 200

        # Si los datos no son validos
        else:
            # Obtener los errors de validación
            errors = form.errors
            return jsonify({"message": "Validation error", "errors": errors}), 400

    except Exception as ex:
        # Registras cualquier excepción durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error updated event. Please try agai later"}), 500