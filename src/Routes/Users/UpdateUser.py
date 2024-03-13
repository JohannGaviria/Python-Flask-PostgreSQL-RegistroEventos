from flask import Blueprint, jsonify, request
from src.Core.PasswordHandling import PasswordSecurity
from src.Core.ValidationUser import UsersForm
from src.Models.Users import User
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('updateUser', __name__)


# Ruta encargada de manejar la actualizacion del usuario
@main.put('api/user/<int:user_id>')
def update_user(user_id):
    try:
        # Buscar el usuario por su ID en la base de datos
        user = User.query.get(user_id)

        # Si el usuario no existe, devolver un mensaje de error
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Obtener los datos en formato JSON enviados en la solicitud
        data = request.get_json()

        # Validar los datos del usuario
        form = UsersForm(data=data)

        # Si los datos son validos
        if form.validate():
            # Extraer los datos
            name = form.name.data
            identification_document = form.identification_document.data
            email = form.email.data
            password = form.password.data
            phone = form.phone.data

            # Hashed de la nueva contraseña
            hashed_password = PasswordSecurity.hash_password(password)

            # Actualizar los datos
            user.name = name
            user.identification_document = identification_document
            user.email = email
            user.password = hashed_password
            user.phone = phone

            with db.session() as session:
                # Guardar los cambios en la base de datos
                session.commit()

                return jsonify({"message": "User updated successfully",
                                "User": {
                                    "user_id": user.user_id,
                                    "name": user.name,
                                    "identification_document": user.identification_document,
                                    "email": user.email,
                                    "phone": user.phone
                                }}), 200

        # Si los datos no son validos
        else:
            # Obtener los errors de validación
            errors = form.errors
            return jsonify({"message": "Validation error", "errors": errors}), 400

    except Exception as ex:
        # Registrar cualquier excepción ocurruda durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error updating user. Please try again later"}), 500