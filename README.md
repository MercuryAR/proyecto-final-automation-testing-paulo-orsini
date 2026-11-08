[![CI TalentoLab](https://github.com/MercuryAR/proyecto-final-automation-testing-paulo-orsini/actions/workflows/ci.yml/badge.svg)](https://github.com/MercuryAR/proyecto-final-automation-testing-paulo-orsini/actions/workflows/ci.yml)

# proyecto-final-automation-testing-paulo-orsini
Framework de automatización de pruebas en Python con Pytest, Selenium WebDriver (Page Object Model) y Requests para pruebas de UI y API. Incluye datos de prueba externos, capturas automáticas en fallos, reportes HTML, logging y CI con GitHub Actions. Proyecto Final Integrador – Talento Tech.

## 1. Propósito
Demostrar un framework de testing completo: pruebas de **UI** sobre [SauceDemo](https://www.saucedemo.com) y de **API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com), con código mantenible (POM), datos externos, reportes visuales y ejecución automática en CI.

## 2. Tecnologías
Python · Pytest (+ pytest-html, pytest-rerunfailures) · Selenium WebDriver (Selenium Manager) · Requests · Faker · Git · GitHub (+ GitHub Actions).

## 3. Estructura del proyecto
```
├── .github/workflows/ci.yml   # Pipeline "CI TalentoLab"
├── pages/                     # Page Objects: Login, Inventory, Cart, Checkout
├── tests/                     # Tests de UI (Selenium)
├── tests_api/                 # Tests de API (Requests) + encadenamiento
├── datos/                     # login.csv, productos.json, checkout.json, posts.json
├── utils/                     # datos.py (lectura de datos), logger.py, api_helpers.py
├── reports/                   # report.html y screens/ (generados)
├── logs/                      # suite.log (generado)
├── conftest.py                # fixtures, screenshots en fallos, hooks del reporte
├── pytest.ini                 # opciones, markers
└── requirements.txt
```

## 4. Instalación
Requiere **Python 3.10+** y **Google Chrome** instalado.
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## 5. Ejecución de las pruebas
```bash
pytest                 # suite completa
pytest tests/          # solo UI
pytest tests_api/      # solo API
pytest -m smoke        # tests críticos
pytest -m e2e          # flujos completos
pytest -m api          # por marker (smoke, ui, api, regression, e2e)
CI=true pytest         # modo headless (simula GitHub Actions)
```

## 6. Reportes
* **`reports/report.html`**: reporte autocontenido con estado (pasó/falló), duración, columna **URL** de la página al terminar cada test de UI y metadata del autor. Abrirlo con el navegador.
* **`reports/screens/`**: captura PNG de cada test de UI fallido, nombrada `nombre_del_test_AAAAMMDD_HHMMSS.png`; también queda embebida en el reporte HTML.
* **`logs/suite.log`**: log del logger `talentolab` (inicio/fin de tests, acciones de los Page Objects, requests de API con método, URL, status y tiempo, errores y rutas de capturas).
* **En GitHub**: pestaña *Actions* → ejecución del workflow → sección *Artifacts* → descargar `html-report` (reporte + capturas) y `suite-log` (se conservan 90 días).

## 7. Casos de prueba cubiertos
**UI (22 casos parametrizados):** login desde CSV (válido + negativos: bloqueado, clave incorrecta, inexistente, vacío); catálogo (título, productos, precios, 4 ordenamientos); carrito desde JSON (agregar, varios, quitar); logout; checkout completo (e2e) y checkout con datos faltantes (negativo).

**API (12 casos):** GET lista y por id, GET 404, POST (desde JSON y con Faker), PUT, DELETE; encadenamiento POST → PATCH → DELETE (< 3 s) y `GET /users` → `GET /posts?userId=`. Cada respuesta se valida en 5 niveles: status, cabeceras, estructura, contenido y tiempo.

> JSONPlaceholder **simula** las escrituras: no persiste los recursos creados.

## 8. Licencia
MIT – ver [LICENSE](LICENSE).
