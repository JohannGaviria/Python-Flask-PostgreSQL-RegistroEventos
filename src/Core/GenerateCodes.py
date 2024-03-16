import random
import string
import qrcode


class GenerateCode:
    # Metodo estatico para generar codigos alfanumericos
    @staticmethod
    def alphanumeric_code():
        numbers = string.digits
        letters = string.ascii_letters.upper()

        # Generar 4 numeros aleatorios
        random_numbers = ''.join(random.choice(numbers) for _ in range(4))

        # Generar 4 letras aleatorias
        random_letters = ''.join(random.choice(letters) for _ in range(4))

        # unir los numero y letras para formar el codigo
        code = random_numbers + " " + random_letters

        return code
    
    # Metodo estatico para generar codigos QR
    @staticmethod
    def code_qr(user):
        # Construir la información del usuario para el código QR
        info_user = f"Usuario ID: {user.user_id}\nNombre: {user.name}\nDocumento de Identificación: {user.identification_document}\nEmail: {user.email}\nTeléfono: {user.phone}"

        # Generar el código QR con la información del usuario
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(info_user)
        qr.make(fit=True)

        image_qr = qr.make_image(fill_color="black", back_color="white")
        return image_qr