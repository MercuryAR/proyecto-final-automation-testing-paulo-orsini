"""Page Object del checkout de SauceDemo (datos, overview y confirmación)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import obtener_logger

log = obtener_logger()


class CheckoutPage:
    """Cubre los tres pasos: datos del comprador, overview y compra completa."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _FINISH_BUTTON = (By.ID, "finish")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")
    _SUMMARY_TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    _OVERVIEW_ITEMS = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    _COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")

    def __init__(self, driver):
        """Guarda el driver y crea la espera explícita de 10 s."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _escribir(self, locator, texto):
        """Escribe ``texto`` en el campo indicado (ignora None)."""
        campo = self.wait.until(EC.visibility_of_element_located(locator))
        campo.clear()
        if texto:
            campo.send_keys(texto)

    # --- Acciones ---------------------------------------------------------
    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa los datos del comprador (admite vacíos para casos negativos)."""
        log.info("CheckoutPage: datos nombre='%s' apellido='%s' cp='%s'", nombre, apellido, codigo_postal)
        self._escribir(self._FIRST_NAME, nombre)
        self._escribir(self._LAST_NAME, apellido)
        self._escribir(self._POSTAL_CODE, codigo_postal)
        return self

    def continuar(self):
        """Presiona Continue (si hay error, la página sigue siendo la misma)."""
        self.wait.until(EC.element_to_be_clickable(self._CONTINUE_BUTTON)).click()
        return self

    def finalizar_compra(self):
        """Desde el overview presiona Finish."""
        log.info("CheckoutPage: finalizando compra")
        self.wait.until(EC.url_contains("/checkout-step-two.html"))
        self.wait.until(EC.element_to_be_clickable(self._FINISH_BUTTON)).click()
        self.wait.until(EC.url_contains("/checkout-complete.html"))
        return self

    # --- Consultas --------------------------------------------------------
    def hay_error(self):
        """Indica si se muestra un mensaje de error."""
        return len(self.driver.find_elements(*self._ERROR_MSG)) > 0

    def obtener_mensaje_error(self):
        """Devuelve el texto del mensaje de error."""
        return self.wait.until(EC.visibility_of_element_located(self._ERROR_MSG)).text

    def obtener_productos_overview(self):
        """Devuelve los nombres de productos listados en el overview."""
        self.wait.until(EC.url_contains("/checkout-step-two.html"))
        # Espera a que el overview termine de renderizar los productos
        self.wait.until(EC.visibility_of_element_located(self._OVERVIEW_ITEMS))
        return [e.text for e in self.driver.find_elements(*self._OVERVIEW_ITEMS)]

    def obtener_total(self):
        """Devuelve el texto del total del overview (ej. 'Total: $32.39')."""
        return self.wait.until(EC.visibility_of_element_located(self._SUMMARY_TOTAL)).text

    def obtener_mensaje_confirmacion(self):
        """Devuelve el texto de confirmación ('Thank you for your order!')."""
        return self.wait.until(EC.visibility_of_element_located(self._COMPLETE_HEADER)).text

    def obtener_url_actual(self):
        """Devuelve la URL actual del navegador."""
        return self.driver.current_url
