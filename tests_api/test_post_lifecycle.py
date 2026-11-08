"""Encadenamiento de peticiones (Clase 12, ticket QA-132).

Nota: JSONPlaceholder SIMULA las escrituras y no persiste los recursos, por eso
no se hace "crear y luego obtener" (el GET del id creado da 404). Además, el id
que devuelve el POST es 101, y PATCH/DELETE sobre él se responden 200 de forma simulada.
"""
import time

import pytest
from faker import Faker

from utils.api_helpers import hacer_request, validar_respuesta_api

fake = Faker("es_AR")
CAMPOS_POST = {"id", "title", "body", "userId"}


@pytest.mark.api
@pytest.mark.e2e
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_ciclo_de_vida_post(posts_url, post_by_id_url):
    """POST → PATCH → DELETE encadenados, pasando el ``id`` de un paso al siguiente; < 3 s en total."""
    inicio = time.perf_counter()

    # 1. POST: crear y guardar el id devuelto
    payload = {"title": fake.sentence(nb_words=4), "body": fake.paragraph(), "userId": 1}
    creado = validar_respuesta_api(hacer_request("post", posts_url, json=payload), 201, CAMPOS_POST)
    post_id = creado["id"]
    assert isinstance(post_id, int) and post_id > 0
    assert creado["title"] == payload["title"]

    # 2. PATCH: actualizar el título usando el id del paso anterior
    nuevo_titulo = "Título actualizado por QA"
    parcheado = validar_respuesta_api(
        hacer_request("patch", post_by_id_url(post_id), json={"title": nuevo_titulo}), 200, {"title"})
    assert parcheado["title"] == nuevo_titulo

    # 3. DELETE: eliminar el recurso
    validar_respuesta_api(hacer_request("delete", post_by_id_url(post_id)), 200)

    assert time.perf_counter() - inicio < 3, "El flujo completo tardó 3 s o más"


@pytest.mark.api
@pytest.mark.e2e
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_encadenamiento_usuario_y_sus_posts(users_url, posts_url):
    """GET /users → id de un usuario → GET /posts?userId={id}: todos los posts son suyos."""
    usuarios = validar_respuesta_api(hacer_request("get", users_url), 200, {"id", "name", "email"})
    user_id = usuarios[0]["id"]

    posts = validar_respuesta_api(
        hacer_request("get", posts_url, params={"userId": user_id}), 200, CAMPOS_POST)
    assert len(posts) > 0
    assert all(p["userId"] == user_id for p in posts)
