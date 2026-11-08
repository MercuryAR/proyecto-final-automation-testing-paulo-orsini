"""Tests del carrito: agregar y quitar productos (datos desde datos/productos.json)."""
import pytest

from utils.datos import leer_json_productos, leer_json_productos_params


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("producto", leer_json_productos_params())
def test_agregar_producto_al_carrito(usuario_logueado, producto):
    """Un producto agregado suma 1 al badge y aparece en el carrito con su nombre."""
    inventario = usuario_logueado.agregar_producto(producto["nombre"])
    assert inventario.obtener_contador_carrito() == 1
    carrito = inventario.ir_al_carrito()
    assert carrito.obtener_nombres_productos() == [producto["nombre"]]


@pytest.mark.ui
@pytest.mark.regression
def test_agregar_varios_productos(usuario_logueado):
    """Agregar todos los productos del JSON: badge y carrito reflejan la misma cantidad."""
    nombres = [p["nombre"] for p in leer_json_productos()]
    for nombre in nombres:
        usuario_logueado.agregar_producto(nombre)
    assert usuario_logueado.obtener_contador_carrito() == len(nombres)
    carrito = usuario_logueado.ir_al_carrito()
    assert sorted(carrito.obtener_nombres_productos()) == sorted(nombres)


@pytest.mark.ui
@pytest.mark.regression
def test_quitar_producto_del_carrito(usuario_logueado):
    """Quitar un producto desde el carrito lo deja vacío."""
    nombre = leer_json_productos()[0]["nombre"]
    carrito = usuario_logueado.agregar_producto(nombre).ir_al_carrito()
    carrito.quitar_producto(nombre)
    assert carrito.obtener_cantidad_productos() == 0


@pytest.mark.ui
@pytest.mark.regression
def test_logout(usuario_logueado):
    """Cerrar sesión devuelve a la pantalla de login."""
    login = usuario_logueado.hacer_logout()
    assert login.obtener_url_actual().rstrip("/") == "https://www.saucedemo.com"
