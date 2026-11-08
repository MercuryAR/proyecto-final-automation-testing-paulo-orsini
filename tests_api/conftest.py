"""Fixtures de URLs reutilizables para los tests de API (JSONPlaceholder)."""
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    """URL base de la API."""
    return BASE_URL


@pytest.fixture(scope="session")
def posts_url(base_url):
    """URL de la colección ``/posts``."""
    return f"{base_url}/posts"


@pytest.fixture(scope="session")
def post_by_id_url(posts_url):
    """Función que arma la URL de un post: ``post_by_id_url(1)`` → ``/posts/1``."""
    return lambda post_id: f"{posts_url}/{post_id}"


@pytest.fixture(scope="session")
def users_url(base_url):
    """URL de la colección ``/users``."""
    return f"{base_url}/users"
