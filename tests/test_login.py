"""Tests de login (UI) parametrizados desde datos/login.csv."""
import pytest

from pages.login_page import LoginPage
from utils.datos import leer_csv_login


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("usuario, clave, debe_funcionar", leer_csv_login())
def test_login_desde_csv(driver, usuario, clave, debe_funcionar):
    """Login con cada fila del CSV.

    Positivo: usuario válido → termina en /inventory.html.
    Negativo: bloqueado, clave mala, inexistente o vacío → mensaje de error y se queda en el login.
    """
    login = LoginPage(driver).abrir().login_completo(usuario, clave)

    if debe_funcionar:
        assert "/inventory.html" in login.ir_a_inventario().obtener_url_actual()
    else:
        assert login.hay_error(), "Se esperaba un mensaje de error"
        assert "Epic sadface" in login.obtener_mensaje_error()
        assert "/inventory.html" not in login.obtener_url_actual()


@pytest.mark.ui
@pytest.mark.smoke
def test_login_valido_smoke(driver):
    """Smoke: el usuario estándar puede iniciar sesión y ve el catálogo."""
    inventario = LoginPage(driver).abrir().login_completo("standard_user", "secret_sauce").ir_a_inventario()
    assert inventario.obtener_titulo() == "Products"


@pytest.mark.ui
@pytest.mark.regression
def test_login_bloqueado_mensaje_especifico(driver):
    """Negativo: el usuario bloqueado ve el mensaje de 'locked out'."""
    login = LoginPage(driver).abrir().login_completo("locked_out_user", "secret_sauce")
    assert "locked out" in login.obtener_mensaje_error()
