"""Lectura centralizada de datos de prueba externos (Clase 10).

Los tests nunca abren archivos: usan estas funciones, que devuelven listas
listas para ``@pytest.mark.parametrize`` (con ``pytest.param`` e ``ids``).
"""
import csv
import json
import os

import pytest

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos")


def _ruta(archivo):
    """Devuelve la ruta absoluta de un archivo dentro de ``datos/``."""
    return os.path.join(CARPETA_DATOS, archivo)


def _leer_json(archivo):
    """Lee un archivo JSON de ``datos/`` preservando los tipos."""
    with open(_ruta(archivo), encoding="utf-8") as f:
        return json.load(f)


def leer_csv_login():
    """Lee ``login.csv`` → lista de ``pytest.param(usuario, clave, debe_funcionar, id=descripcion)``."""
    casos = []
    with open(_ruta("login.csv"), newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            debe = fila["debe_funcionar"].strip().lower() == "true"
            casos.append(pytest.param(fila["usuario"], fila["clave"], debe, id=fila["descripcion"]))
    return casos


def leer_json_productos():
    """Lee ``productos.json`` → lista de diccionarios ``{nombre, precio, descripcion}``."""
    return _leer_json("productos.json")


def leer_json_productos_params():
    """Productos como ``pytest.param(producto, id=descripcion)`` para parametrizar."""
    return [pytest.param(p, id=p["descripcion"]) for p in leer_json_productos()]


def leer_json_checkout_validos():
    """Compradores válidos de ``checkout.json`` como ``pytest.param``."""
    return [pytest.param(c, id=c["descripcion"]) for c in _leer_json("checkout.json")["validos"]]


def leer_json_checkout_invalidos():
    """Compradores con datos faltantes de ``checkout.json`` como ``pytest.param``."""
    return [pytest.param(c, id=c["descripcion"]) for c in _leer_json("checkout.json")["invalidos"]]


def leer_json_posts():
    """Lee ``posts.json`` → ``pytest.param(post, id=descripcion)`` para los POST de la API."""
    return [pytest.param(p, id=p["descripcion"]) for p in _leer_json("posts.json")]
