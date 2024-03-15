from flask import Blueprint, jsonify, request
from src.Core.FormatDate import FormatDate
from src.Core.ValidateEvent import EventsForm
from src.Models.Events import Event
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc
from uuid import uuid4


main = Blueprint('createEvent', __name__)


# Ruta encargada de crear un evento
@main.post('api/event')
def create_event():
    try:
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
            access_code = str(uuid4())

            # Formatear las fechas
            start_date = FormatDate.format_date(start_date)
            end_date = FormatDate.format_date(end_date)

            with db.session() as session:
                # Guardar el nuevo evento en la base de datos
                new_event = Event(creator_id, name, start_date, end_date, location, access_code)
                session.add(new_event)
                session.commit()

                # Devolver los datos del evento
                return jsonify({"message": "Event created successfully",
                                "Event": {
                                    "event_id": new_event.event_id,
                                    "creator_id": new_event.creator_id,
                                    "name": new_event.name,
                                    "start_date": new_event.start_date,
                                    "end_date": new_event.end_date,
                                    "location": new_event.location,
                                    "access_code": new_event.access_code
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
        return jsonify({"message": "Error created event. Please try agai later"}), 500