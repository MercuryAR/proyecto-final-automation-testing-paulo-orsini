"""Logger centralizado del proyecto (Clase 13).

Escribe en ``logs/suite.log`` con nivel INFO o superior. Todos los módulos
obtienen el mismo logger nombrado ``talentolab`` mediante :func:`obtener_logger`.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

NOMBRE_LOGGER = "talentolab"
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "suite.log")
FORMATO = "%(asctime)s %(levelname)s %(name)s – %(message)s"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger ``talentolab`` configurado (idempotente).

    Crea la carpeta ``logs/`` si no existe y agrega un único handler rotativo.
    """
    logger = logging.getLogger(NOMBRE_LOGGER)
    if not logger.handlers:
        os.makedirs(CARPETA_LOGS, exist_ok=True)
        handler = RotatingFileHandler(ARCHIVO_LOG, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        handler.setFormatter(logging.Formatter(FORMATO))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
