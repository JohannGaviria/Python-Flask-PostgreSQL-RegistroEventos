from datetime import datetime


# Clase para formatear fechas
class FormatDate:
    # Metodo de formateo de fecha
    @staticmethod
    def format_date(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")