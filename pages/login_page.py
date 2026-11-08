"""Page Object de la página de login de SauceDemo."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import obtener_logger

log = obtener_logger()


class LoginPage:
    """Representa https://www.saucedemo.com (pantalla de inicio de sesión)."""

    URL = "https://www.saucedemo.com"

    # Locators privados
    _USER_INPUT = (By.ID, "user-name")
    _PASS_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        """Guarda el driver y crea la espera explícita de 10 s."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Acciones ---------------------------------------------------------
    def abrir(self):
        """Abre la página de login y espera el campo de usuario."""
        log.info("LoginPage: abriendo %s", self.URL)
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        return self

    def completar_usuario(self, usuario):
        """Escribe el usuario en su campo."""
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(usuario)
        return self

    def completar_clave(self, clave):
        """Escribe la clave en su campo."""
        campo = self.wait.until(EC.visibility_of_element_located(self._PASS_INPUT))
        campo.clear()
        campo.send_keys(clave)
        return self

    def hacer_click_login(self):
        """Presiona el botón Login."""
        self.wait.until(EC.element_to_be_clickable(self._LOGIN_BUTTON)).click()
        return self

    def login_completo(self, usuario, clave):
        """Completa usuario y clave y presiona Login.

        Devuelve ``self`` (la página sigue siendo el login). Si el acceso es
        exitoso, ``InventoryPage`` se obtiene con :meth:`ir_a_inventario`.
        """
        log.info("LoginPage: login con usuario '%s'", usuario)
        self.completar_usuario(usuario).completar_clave(clave).hacer_click_login()
        return self

    def ir_a_inventario(self):
        """Espera la URL del inventario y devuelve ``InventoryPage``."""
        from pages.inventory_page import InventoryPage  # import diferido

        self.wait.until(EC.url_contains("/inventory.html"))
        return InventoryPage(self.driver)

    # --- Consultas --------------------------------------------------------
    def hay_error(self):
        """Indica si se muestra un mensaje de error."""
        return len(self.driver.find_elements(*self._ERROR_MSG)) > 0

    def obtener_mensaje_error(self):
        """Devuelve el texto del mensaje de error (espera a que aparezca)."""
        return self.wait.until(EC.visibility_of_element_located(self._ERROR_MSG)).text

    def obtener_url_actual(self):
        """Devuelve la URL actual del navegador."""
        return self.driver.current_url
