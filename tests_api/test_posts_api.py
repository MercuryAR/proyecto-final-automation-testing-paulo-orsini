"""Tests de API sobre /posts (JSONPlaceholder): GET, POST, PUT, DELETE y errores."""
import pytest
from faker import Faker

from utils.api_helpers import hacer_request, validar_respuesta_api
from utils.datos import leer_json_posts

CAMPOS_POST = {"id", "title", "body", "userId"}
fake = Faker("es_AR")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_get_lista_de_posts(posts_url):
    """GET /posts → 200, JSON, lista de 100 posts con estructura y tipos correctos."""
    r = hacer_request("get", posts_url)
    posts = validar_respuesta_api(r, 200, CAMPOS_POST)
    assert isinstance(posts, list) and len(posts) == 100
    assert all(isinstance(p["id"], int) and p["id"] > 0 for p in posts)
    assert all(p["title"].strip() and p["body"].strip() for p in posts)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_get_post_por_id(post_by_id_url, post_id):
    """GET /posts/{id} → 200 y el id devuelto coincide con el pedido."""
    r = hacer_request("get", post_by_id_url(post_id))
    post = validar_respuesta_api(r, 200, CAMPOS_POST)
    assert post["id"] == post_id
    assert isinstance(post["userId"], int)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_get_post_inexistente_devuelve_404(post_by_id_url):
    """Error: GET /posts/99999 → 404 con cuerpo vacío ``{}``."""
    r = hacer_request("get", post_by_id_url(99999))
    cuerpo = validar_respuesta_api(r, 404)
    assert cuerpo == {}


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("datos", leer_json_posts())
def test_post_crea_recurso_desde_json(posts_url, datos):
    """POST /posts con datos de datos/posts.json → 201 y eco de los datos enviados."""
    payload = {k: datos[k] for k in ("title", "body", "userId")}
    r = hacer_request("post", posts_url, json=payload)
    creado = validar_respuesta_api(r, 201, CAMPOS_POST)
    assert creado["title"] == payload["title"]
    assert creado["body"] == payload["body"]
    assert creado["userId"] == payload["userId"]
    assert creado["id"] > 0


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_post_con_datos_faker(posts_url):
    """POST /posts con título y cuerpo aleatorios (Faker) → 201 y contenido coherente."""
    payload = {"title": fake.sentence(nb_words=4), "body": fake.paragraph(), "userId": 1}
    r = hacer_request("post", posts_url, json=payload)
    creado = validar_respuesta_api(r, 201, CAMPOS_POST)
    assert creado["title"] == payload["title"]


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_put_actualiza_post(post_by_id_url):
    """PUT /posts/1 → 200 y devuelve los datos actualizados."""
    payload = {"id": 1, "title": "Título nuevo", "body": "Cuerpo nuevo", "userId": 1}
    r = hacer_request("put", post_by_id_url(1), json=payload)
    actualizado = validar_respuesta_api(r, 200, CAMPOS_POST)
    assert actualizado["title"] == "Título nuevo"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_delete_elimina_post(post_by_id_url):
    """DELETE /posts/1 → 200 (JSONPlaceholder simula el borrado y responde ``{}``)."""
    r = hacer_request("delete", post_by_id_url(1))
    cuerpo = validar_respuesta_api(r, 200)
    assert cuerpo == {}
