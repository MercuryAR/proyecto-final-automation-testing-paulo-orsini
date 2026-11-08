"""Configuración global de pytest: fixtures, screenshots y hooks del reporte.

Contiene:
* fixture ``driver`` (Selenium, un navegador nuevo por test) y ``usuario_logueado``;
* hook de captura de pantalla en fallos (nombre del test + fecha/hora);
* hooks del reporte HTML (columna URL y metadata de autor);
* registro en el log del inicio y fin de cada test.
"""
import os
import re
from datetime import datetime

import pytest
import pytest_html
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.logger import obtener_logger

log = obtener_logger()

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_SCREENS = os.path.join(RAIZ, "reports", "screens")


# ---------------------------------------------------------------------------
# Metadata del reporte HTML
# ---------------------------------------------------------------------------
def pytest_configure(config):
    """Agrega la metadata de autor al reporte HTML."""
    config.stash[metadata_key]["Autor"] = "Paulo Orsini"
    config.stash[metadata_key]["Proyecto"] = "Proyecto Final – Automation Testing (Talento Tech)"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver():
    """Abre Chrome (Selenium Manager) y lo cierra siempre al terminar el test.

    Si existe la variable de entorno ``CI`` (GitHub Actions la define sola)
    se ejecuta en modo headless; en local el navegador se ve.
    """
    opciones = Options()
    opciones.add_argument("--window-size=1920,1080")
    # Evita los popups de contraseñas de Chrome que tapan la página de SauceDemo
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
    if os.environ.get("CI"):
        for argumento in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage"):
            opciones.add_argument(argumento)
    navegador = webdriver.Chrome(options=opciones)
    log.info("Navegador Chrome iniciado (headless=%s)", bool(os.environ.get("CI")))
    yield navegador
    navegador.quit()
    log.info("Navegador Chrome cerrado")


@pytest.fixture
def usuario_logueado(driver):
    """Deja al usuario ``standard_user`` logueado en el inventario y devuelve su página."""
    from pages.login_page import LoginPage  # import diferido: evita ciclos

    return LoginPage(driver).abrir().login_completo("standard_user", "secret_sauce")


@pytest.fixture(autouse=True)
def registrar_test(request):
    """Registra en el log el inicio y el fin de cada test."""
    log.info("INICIO test: %s", request.node.nodeid)
    yield
    log.info("FIN test: %s", request.node.nodeid)


# ---------------------------------------------------------------------------
# Hook de capturas de pantalla en fallos (Clase 13 + consigna: nombre + fecha/hora)
# ---------------------------------------------------------------------------
def _nombre_seguro(texto: str) -> str:
    """Sanea el nombre del test para usarlo como nombre de archivo."""
    return re.sub(r"[^\w\-\[\].]+", "_", texto)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test de UI falla, guarda un PNG y lo adjunta al reporte HTML."""
    outcome = yield
    reporte = outcome.get_result()
    extras = getattr(reporte, "extras", [])

    if reporte.when == "call":
        navegador = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
        # URL final de la página (columna "URL" del reporte)
        if navegador is not None:
            try:
                item.page_url = navegador.current_url
            except Exception:  # navegador ya caído
                pass
        if reporte.failed and navegador is not None:
            os.makedirs(CARPETA_SCREENS, exist_ok=True)
            marca = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = os.path.join(CARPETA_SCREENS, f"{_nombre_seguro(item.name)}_{marca}.png")
            try:
                navegador.save_screenshot(ruta)
                extras.append(pytest_html.extras.png(navegador.get_screenshot_as_base64()))
                log.error("Test FALLIDO: %s – screenshot: %s", item.nodeid, ruta)
            except Exception as error:
                log.error("No se pudo capturar pantalla de %s: %s", item.nodeid, error)
        elif reporte.failed:
            log.error("Test FALLIDO: %s", item.nodeid)

    reporte.extras = extras
    reporte.page_url = getattr(item, "page_url", "-")


# ---------------------------------------------------------------------------
# Columna "URL" del reporte HTML
# ---------------------------------------------------------------------------
def pytest_html_results_table_header(cells):
    """Agrega la cabecera de la columna URL."""
    cells.insert(2, "<th>URL</th>")


def pytest_html_results_table_row(report, cells):
    """Agrega la URL final de la página (o '-' en tests de API)."""
    cells.insert(2, f"<td>{getattr(report, 'page_url', '-')}</td>")
