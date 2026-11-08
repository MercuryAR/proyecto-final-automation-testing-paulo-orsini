"""Tests del checkout: flujo completo y datos faltantes (datos desde datos/checkout.json)."""
import pytest

from utils.datos import leer_json_checkout_invalidos, leer_json_checkout_validos, leer_json_productos


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.parametrize("comprador", leer_json_checkout_validos())
def test_checkout_completo(usuario_logueado, comprador):
    """Flujo completo: carrito → datos → overview → 'Thank you for your order!'."""
    nombre = leer_json_productos()[0]["nombre"]
    checkout = usuario_logueado.agregar_producto(nombre).ir_al_carrito().proceder_checkout()
    checkout.completar_datos(comprador["nombre"], comprador["apellido"], comprador["codigo_postal"]).continuar()

    assert checkout.obtener_productos_overview() == [nombre]
    assert "Total" in checkout.obtener_total()
    checkout.finalizar_compra()
    assert checkout.obtener_mensaje_confirmacion() == "Thank you for your order!"


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("comprador", leer_json_checkout_invalidos())
def test_checkout_datos_faltantes(usuario_logueado, comprador):
    """Negativo: con un dato obligatorio vacío se muestra el error y no avanza."""
    nombre = leer_json_productos()[0]["nombre"]
    checkout = usuario_logueado.agregar_producto(nombre).ir_al_carrito().proceder_checkout()
    checkout.completar_datos(comprador["nombre"], comprador["apellido"], comprador["codigo_postal"]).continuar()

    assert checkout.hay_error()
    assert checkout.obtener_mensaje_error() == comprador["error"]
    assert "checkout-step-one" in checkout.obtener_url_actual()
