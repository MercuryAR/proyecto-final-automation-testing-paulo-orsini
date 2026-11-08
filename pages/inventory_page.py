"""Page Object del catálogo de productos (inventory) de SauceDemo."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils.logger import obtener_logger

log = obtener_logger()


class InventoryPage:
    """Representa https://www.saucedemo.com/inventory.html."""

    URL = "https://www.saucedemo.com/inventory.html"

    _TITLE = (By.CSS_SELECTOR, ".title")
    _ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    _ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    _ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    _SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    _CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    _CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        """Guarda el driver y crea la espera explícita de 10 s."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @staticmethod
    def _id_boton(prefijo, nombre):
        """Arma el id del botón agregar/quitar a partir del nombre del producto."""
        return (By.ID, f"{prefijo}-{nombre.lower().replace(' ', '-')}")

    # --- Acciones ---------------------------------------------------------
    def agregar_producto(self, nombre):
        """Agrega al carrito el producto con ese nombre."""
        log.info("InventoryPage: agregando '%s' al carrito", nombre)
        self.wait.until(EC.element_to_be_clickable(self._id_boton("add-to-cart", nombre))).click()
        return self

    def quitar_producto(self, nombre):
        """Quita del carrito el producto desde el catálogo."""
        log.info("InventoryPage: quitando '%s' del carrito", nombre)
        self.wait.until(EC.element_to_be_clickable(self._id_boton("remove", nombre))).click()
        return self

    def ordenar_por(self, valor):
        """Ordena el catálogo. Valores: az, za, lohi, hilo."""
        log.info("InventoryPage: ordenando por '%s'", valor)
        Select(self.wait.until(EC.element_to_be_clickable(self._SORT_SELECT))).select_by_value(valor)
        return self

    def ir_al_carrito(self):
        """Abre el carrito y devuelve ``CartPage``."""
        from pages.cart_page import CartPage  # import diferido

        self.wait.until(EC.element_to_be_clickable(self._CART_LINK)).click()
        self.wait.until(EC.url_contains("/cart.html"))
        self.wait.until(EC.visibility_of_element_located(CartPage._TITLE))
        return CartPage(self.driver)

    def hacer_logout(self):
        """Cierra sesión desde el menú lateral y devuelve ``LoginPage``."""
        from pages.login_page import LoginPage  # import diferido

        log.info("InventoryPage: cerrando sesión")
        self.wait.until(EC.element_to_be_clickable(self._MENU_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self._LOGOUT_LINK)).click()
        self.wait.until(EC.visibility_of_element_located(LoginPage._LOGIN_BUTTON))
        return LoginPage(self.driver)

    # --- Consultas --------------------------------------------------------
    def obtener_titulo(self):
        """Devuelve el título de la sección (ej. 'Products')."""
        return self.wait.until(EC.visibility_of_element_located(self._TITLE)).text

    def obtener_cantidad_productos(self):
        """Devuelve cuántos productos se muestran."""
        self.wait.until(EC.visibility_of_element_located(self._ITEMS))
        return len(self.driver.find_elements(*self._ITEMS))

    def obtener_nombres_productos(self):
        """Devuelve la lista de nombres en el orden mostrado."""
        self.wait.until(EC.visibility_of_element_located(self._ITEM_NAMES))
        return [e.text for e in self.driver.find_elements(*self._ITEM_NAMES)]

    def obtener_precios_productos(self):
        """Devuelve la lista de precios (float) en el orden mostrado."""
        self.wait.until(EC.visibility_of_element_located(self._ITEM_PRICES))
        return [float(e.text.replace("$", "")) for e in self.driver.find_elements(*self._ITEM_PRICES)]

    def obtener_contador_carrito(self):
        """Devuelve el número del badge del carrito (0 si no hay badge)."""
        badges = self.driver.find_elements(*self._CART_BADGE)
        return int(badges[0].text) if badges else 0

    def obtener_url_actual(self):
        """Devuelve la URL actual del navegador."""
        return self.driver.current_url
