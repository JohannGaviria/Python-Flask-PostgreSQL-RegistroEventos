from flask import Blueprint, jsonify, request
from src.Core.PasswordHandling import PasswordSecurity
from src.Core.ValidationUser import UsersForm
from src.Models.Users import User
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('createUser', __name__)


# Ruta encargada de crear los usuarios
@main.post('api/user')
def create_user():
    try:
        # Obtener los datos enviados en la solicitud en formato JSON
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

            # Encriptar la contraseña
            hashed_password = PasswordSecurity.hash_password(password)

            with db.session() as session:
                # Guardar el nuevo usuario en la base de datos
                new_user = User(name, identification_document, email, hashed_password, phone)
                session.add(new_user)
                session.commit()

                return jsonify({"message": "User created successfully",
                                "User": {
                                    "user_id": new_user.user_id,
                                    "name": new_user.name,
                                    "identification_document": new_user.identification_document,
                                    "email": new_user.email,
                                    "phone": new_user.phone
                                }}), 200

        # Si los datos no son validos
        else:
            # Obtener los errors de validación
            errors = form.errors
            return jsonify({"message": "Validation error", "errors": errors}), 400

    except Exception as ex:
        # Registra cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error creating user. Please try again later"}), 500
