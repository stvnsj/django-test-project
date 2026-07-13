# Prueba técnica - Comparación de portafolios

Solución para la prueba técnica de Python/Django.

El proyecto carga información desde un archivo Excel, guarda los datos en una base de datos SQLite, expone una API para consultar la evolución de los portafolios y muestra una vista simple con gráficos comparativos.

La idea fue mantener la solución lo más simple posible, separando la carga de datos, los cálculos y las vistas.

## Tecnologías usadas

- Python
- Django
- SQLite
- openpyxl
- Chart.js

## Estructura general

La aplicación principal es `portfolios`.

Los archivos más importantes son:

- `models.py`: modelos de activos, precios, portafolios y composición de portafolios.
- `etl.py`: carga de datos desde el archivo Excel.
- `services.py`: cálculo de evolución del valor del portafolio y ponderaciones.
- `views.py`: API y vista HTML.
- `templates/`: template usado para mostrar los gráficos.
- `management/commands/`: comando de Django para cargar los datos.

La estructura principal es:

```text
.
├── config/
├── portfolios/
├── manage.py
├── datos.xlsx
├── requirements.txt
└── README.md
```

## Instalación

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Aplicar migraciones:

```bash
python manage.py migrate
```

## Cargar los datos

El archivo Excel usado por el proyecto es `datos.xlsx`.

Para cargar los datos:

```bash
python manage.py load_portfolio_data datos.xlsx
```

Si todo sale bien, debería aparecer:

```text
Portfolio data loaded successfully.
```

Este comando carga los activos, los precios históricos, los portafolios, las ponderaciones iniciales y calcula las cantidades iniciales de cada activo.

## Ejecutar la aplicación

Levantar el servidor de desarrollo:

```bash
python manage.py runserver
```

Luego abrir:

```text
http://127.0.0.1:8000/comparison/
```

La vista permite elegir un rango de fechas y comparar gráficamente ambos portafolios.

## API

La API permite consultar la evolución de un portafolio entre dos fechas:

```text
/api/portfolios/<portfolio_id>/evolution/?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD
```

Ejemplo:

```text
http://127.0.0.1:8000/api/portfolios/1/evolution/?fecha_inicio=2022-02-15&fecha_fin=2023-02-16
```

La vista `/comparison/` obtiene automáticamente los portafolios cargados, por lo que no debería ser necesario buscar los ids manualmente.

## Vista de comparación

La vista muestra tres gráficos:

- Evolución del valor de ambos portafolios.
- Evolución de las ponderaciones del Portafolio 1.
- Evolución de las ponderaciones del Portafolio 2.

Los gráficos se generan con Chart.js consumiendo los datos entregados por la API.

## Algunas validaciones

Durante la carga del Excel se revisan algunos casos básicos:

- Que los precios no estén vacíos.
- Que los precios sean mayores a cero.
- Que las ponderaciones estén entre 0 y 1.
- Que los activos de la hoja de ponderaciones existan también en la hoja de precios.
- Que las cantidades iniciales puedan calcularse correctamente.

En la API también se validan los parámetros `fecha_inicio` y `fecha_fin`.

## Prueba rápida desde cero

Para reconstruir la base de datos y probar el flujo completo:

```bash
rm -f db.sqlite3
python manage.py migrate
python manage.py load_portfolio_data datos.xlsx
python manage.py runserver
```

Luego abrir:

```text
http://127.0.0.1:8000/comparison/
```

## Notas

La base de datos `db.sqlite3` no se incluye en el repositorio. Debe generarse localmente con las migraciones y luego cargarse usando el comando indicado.

Intenté mantener las vistas delgadas: la vista recibe la solicitud, valida parámetros básicos y delega el cálculo a `services.py`.

La carga del Excel está separada en `etl.py` porque es un flujo distinto al cálculo de evolución de portafolios.