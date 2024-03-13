import bcrypt


class PasswordSecurity:
    @staticmethod
    def hash_password(password):
        # Función para hashear una contraseña.
        salt = bcrypt.gensalt()  # Generamos una sal única para la contraseña.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hasheamos la contraseña con la sal generada.
        return hashed_password.decode('utf-8')  # Devolvemos la contraseña hasheada como una cadena decodificada.

    @staticmethod
    def verify_password(hashed_password, input_password):
        # Función para verificar si una contraseña coincide con su versión hasheada.
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))  # Verificamos si la contraseña de entrada coincide con su versión hasheada.
