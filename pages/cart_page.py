"""Page Object del carrito de compras de SauceDemo."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import obtener_logger

log = obtener_logger()


class CartPage:
    """Representa https://www.saucedemo.com/cart.html."""

    URL = "https://www.saucedemo.com/cart.html"

    _TITLE = (By.CSS_SELECTOR, ".title")
    _ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def __init__(self, driver):
        """Guarda el driver y crea la espera explícita de 10 s."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Acciones ---------------------------------------------------------
    def quitar_producto(self, nombre):
        """Quita un producto desde el carrito."""
        log.info("CartPage: quitando '%s'", nombre)
        locator = (By.ID, f"remove-{nombre.lower().replace(' ', '-')}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.wait.until(EC.invisibility_of_element_located(locator))
        return self

    def proceder_checkout(self):
        """Presiona Checkout y devuelve ``CheckoutPage``."""
        from pages.checkout_page import CheckoutPage  # import diferido

        log.info("CartPage: procediendo al checkout")
        self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BUTTON)).click()
        self.wait.until(EC.url_contains("/checkout-step-one.html"))
        return CheckoutPage(self.driver)

    def seguir_comprando(self):
        """Vuelve al catálogo y devuelve ``InventoryPage``."""
        from pages.inventory_page import InventoryPage  # import diferido

        self.wait.until(EC.element_to_be_clickable(self._CONTINUE_SHOPPING)).click()
        self.wait.until(EC.url_contains("/inventory.html"))
        return InventoryPage(self.driver)

    # --- Consultas --------------------------------------------------------
    def obtener_titulo(self):
        """Devuelve el título de la sección (ej. 'Your Cart')."""
        return self.wait.until(EC.visibility_of_element_located(self._TITLE)).text

    def obtener_nombres_productos(self):
        """Devuelve los nombres de los productos del carrito."""
        return [e.text for e in self.driver.find_elements(*self._ITEM_NAMES)]

    def obtener_cantidad_productos(self):
        """Devuelve cuántos productos hay en el carrito."""
        return len(self.driver.find_elements(*self._ITEM_NAMES))
