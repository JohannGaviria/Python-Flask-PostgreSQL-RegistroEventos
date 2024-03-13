import logging
import os
import traceback


class Logger():
    def __set_logger(self):
        # Define el directorio y el nombre del archivo de registro
        log_directory = 'src/utils/log'
        log_filename = 'app.log'

        # Configura el logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Define la ruta completa del archivo de registro
        log_path = os.path.join(log_directory, log_filename)

        # Crea un manejador de archivo para escribir en el archivo de registro
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Define el formato del registro
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        # Limpia los manejadores del logger si ya existen
        if logger.hasHandlers():
            logger.handlers.clear()

        # Agrega el manejador de archivo al logger
        logger.addHandler(file_handler)

        return logger

    @classmethod
    def add_to_log(cls, level, message):
        try:
            # Obtiene una instancia del logger
            logger = cls.__set_logger(cls)

            # Registra el mensaje según el nivel especificado
            if level == "critical":
                logger.critical(message)
            elif level == "debug":
                logger.debug(message)
            elif level == "error":
                logger.error(message)
            elif level == "info":
                logger.info(message)
            elif level == "warn":
                logger.warning(message)
        except Exception as ex:
            # Imprime la traza de la excepción y la excepción misma si falla el registro
            print(traceback.format_exc())
            print(ex)
