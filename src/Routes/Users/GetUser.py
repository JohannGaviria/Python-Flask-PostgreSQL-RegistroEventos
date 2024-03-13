from flask import Blueprint, jsonify
from src.Models.Users import User
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('getUser', __name__)


# Ruta encargada de obtener un usuario por su ID
@main.get('api/user/<int:user_id>')
def get_user(user_id):
    try:
        # Buscar el usuario por su ID en la base de datos
        user = User.query.get(user_id)

        # Si el usuario no existe, devolver un mensaje de error
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Devolver los datos del usuario en formato JSON
        return jsonify({"message": "User geted successfully",
                        "User": {
                            "user_id": user.user_id,
                            "name": user.name,
                            "identification_document": user.identification_document,
                            "email": user.email,
                            "phone": user.phone
                        }}), 200

    except Exception as ex:
        # Registra cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error getting user. Please try again later"}), 500
