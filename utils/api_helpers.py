"""Helpers para pruebas de API: request con log y validación de respuestas."""
import requests

from utils.logger import obtener_logger

log = obtener_logger()

TIMEOUT_HTTP = 10  # segundos máximos de espera por request


def hacer_request(metodo, url, **kwargs):
    """Ejecuta un request y registra método, URL, status y tiempo en el log."""
    kwargs.setdefault("timeout", TIMEOUT_HTTP)
    respuesta = requests.request(metodo, url, **kwargs)
    log.info("API %s %s → %s en %.3f s", metodo.upper(), respuesta.url,
             respuesta.status_code, respuesta.elapsed.total_seconds())
    return respuesta


def validar_respuesta_api(response, status_esperado, campos_esperados=None, tiempo_max=3.0):
    """Valida los 5 niveles: status, cabecera JSON, estructura, tiempo (y devuelve el cuerpo).

    * ``campos_esperados``: conjunto de claves obligatorias (en el objeto o en cada
      elemento si la respuesta es una lista). ``None`` omite el chequeo de estructura.
    * Devuelve el cuerpo JSON para que el test valide el contenido (nivel 4).
    """
    # 1. Código de estado
    assert response.status_code == status_esperado, (
        f"Status {response.status_code}, se esperaba {status_esperado}")
    # 2. Cabeceras
    assert "application/json" in response.headers.get("Content-Type", ""), "Content-Type no es JSON"
    # 5. Tiempo de respuesta
    assert response.elapsed.total_seconds() < tiempo_max, (
        f"Respuesta lenta: {response.elapsed.total_seconds():.2f} s (máx {tiempo_max} s)")
    cuerpo = response.json()
    # 3. Estructura
    if campos_esperados:
        elementos = cuerpo if isinstance(cuerpo, list) else [cuerpo]
        assert elementos, "La respuesta no trae elementos"
        for elemento in elementos:
            assert set(campos_esperados) <= set(elemento.keys()), (
                f"Faltan claves: {set(campos_esperados) - set(elemento.keys())}")
    return cuerpo
