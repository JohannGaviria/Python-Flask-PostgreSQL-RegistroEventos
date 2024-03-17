from flask import Blueprint, jsonify
from src.Core.GenerateReports import GeneratorReport
from src.Models.Attendances import Attendance
from src.Models.Events import Event
from src.Models.Participants import Participant
from src.Models.Users import User
from src.Utils.Database import db
from src.Utils.Logger import Logger
from traceback import format_exc


main = Blueprint('generateReport', __name__)


# Ruta encargada de hacer los reportes de los asistentes y no aasitentes a los eventos
@main.get('/api/event/<int:event_id>/generateReport/<int:user_id>')
def generate_report(event_id, user_id):
    try:
        # Buscar el evento por su ID en la base de datos
        event = Event.query.get(event_id)

        # Buscar el usuario por su ID en la base de datos
        user = User.query.get(user_id)

        # Si el evento no existe, devolver un mensaje de error
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        # Verificar si el usuario es el creador del evento
        if user_id != event.creator_id:
            return jsonify({"message": "El usuario no es el creador del evento"}), 403
        
        # Obtener la asistencia al evento
        attendance = Attendance.query.filter_by(event_id=event_id).all()

        # Obtener la lista de usuarios que no asistieron al evento
        participants_attend = [participant.user_id for participant in attendance]

        participants = Participant.query.filter_by(event_id=event_id).all()
        users_not_attend = [participant.user_id for participant in participants if participant.user_id not in participants_attend]

        # Crear un objeto de la clase GeneratorReport y generar el informe
        excel_generator = GeneratorReport(event, attendance, users_not_attend)
        report_path = excel_generator.generate_report()

        # Devolver la ruta del archivo de reporte generado
        return jsonify({"message": "Report generated successfully"})

    except Exception as ex:
        # Registrar cualquier excepción ocurrida durante el proceso
        Logger.add_to_log('error', str(ex))
        Logger.add_to_log('error', format_exc())
        return jsonify({"message": "Error generating report. Please try again later"}), 500
