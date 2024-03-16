from flask import Blueprint, jsonify
from src.Core.GenerateCodes import GenerateCode
from src.Models.Participants import Participant
from src.Models.Events import Event
from src.Models.Users import User
from src.Models.Events import Event
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('generateCode', __name__)


# Ruta encargada de generar un codigo alfanumerico y qr para el acceso al evento
@main.get('api/event/<int:event_id>/generateCode/<int:user_id>')
def generate_code(event_id, user_id):
    try:
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
        
        # Verificar si el usuario está registrado en el evento
        participant = Participant.query.filter_by(user_id=user_id, event_id=event_id).first()

        if not participant:
            # Si el usuario no está registrado en el evento, devolver un mensaje de error
            return jsonify({"message": "User not registered in the event"}), 400
        
        # Generar el codigo alfanumerio
        alphanumeric_code = GenerateCode.alphanumeric_code()
        # Generar el codigo QR
        # code_qr = GenerateCode.code_qr(user)

        # Verificar si el codigo ya ha sido generado
        if participant.join_code is not None:
            return jsonify({"message": "already generated join code"}), 409

        # Actualizar el codigo de union
        participant.join_code = alphanumeric_code

        with db.session() as session:
            # Guardar el codigo en la db
            session.commit()

            return jsonify({"message": "Generate codes successfully",
                        "Alphanumeric code": alphanumeric_code}), 200

    except Exception as ex:
        # Registrar cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error generating code. Please try again later"}), 500