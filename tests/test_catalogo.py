"""Tests del catálogo de productos: contenido y ordenamiento."""
import pytest


@pytest.mark.ui
@pytest.mark.regression
def test_catalogo_muestra_productos(usuario_logueado):
    """Título 'Products', 6 productos, nombres no vacíos y precios positivos."""
    inventario = usuario_logueado
    assert inventario.obtener_titulo() == "Products"
    assert inventario.obtener_cantidad_productos() == 6
    assert all(nombre.strip() for nombre in inventario.obtener_nombres_productos())
    assert all(precio > 0 for precio in inventario.obtener_precios_productos())


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("valor, clave_orden, inverso", [
    pytest.param("lohi", "precios", False, id="precio_menor_a_mayor"),
    pytest.param("hilo", "precios", True, id="precio_mayor_a_menor"),
    pytest.param("az", "nombres", False, id="nombre_a_z"),
    pytest.param("za", "nombres", True, id="nombre_z_a"),
])
def test_catalogo_ordenamiento(usuario_logueado, valor, clave_orden, inverso):
    """Al ordenar, la lista mostrada coincide con la lista ordenada en Python."""
    inventario = usuario_logueado.ordenar_por(valor)
    obtenidos = (inventario.obtener_precios_productos() if clave_orden == "precios"
                 else inventario.obtener_nombres_productos())
    assert obtenidos == sorted(obtenidos, reverse=inverso)
