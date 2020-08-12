# Prueba Tecnica Tsakana

_La entrega incluye punto 1, punto 2 y el punto 3._

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

_Para el PUNTO 1 se deben tener en cuenta los siguientes pasos:_

```
// instalar e iniciar un ambiente virtual:
python3 -m venv venv
. venv/bin/activate

// instalar flask y sqlalchemy:
pip install Flask
pip install SQLAlchemy

// inicializar base de datos
// 1. ejecutar python dentro de la carpeta commerceretail
// 2. ejecutar las siguientes lineas
from commerceretail.database import init_db
init_db()

// para ejecutar el proyecto, ingresar a la carpeta commerceretail y ejecutar:
export FLASK_ENV=development
export FLASK_APP=commerceretail
flask run

// por ultimo, se debe registrar en la aplicacion y luego iniciar sesion
```

_Para el PUNTO 2 solo se requiere ejecutar el script de python:_

```
python punto2.py
```

_Para el PUNTO 3 solo se requiere visualizar la imagen:_

## Autores ✒️

sergio.garcia.loz@gmail.com
