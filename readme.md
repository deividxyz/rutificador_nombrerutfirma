Web Scraper para Nombrerutyfirma.com
====================================

Rutificador automático que descarga información desde sitio nombrerutyfirma.com (Chile), utilizando Python y Requests.

Aviso Importante
================
El presente proyecto no tiene relación alguna con el sitio nombrerutyfirma.com ni con los datos almacenados en el mismo, ni tampoco con sus creadores/administradores.


El presente código sólo sirve como medio de consulta a la base de datos alojada en nombrerutyfirma.cl. El autor se desliga de cualquier responsabilidad derivada del uso del presente código.

Requisitos
=========

* Python 3.6 o superior. Anaconda provee la gran mayoría de los paquetes que se listan abajo, o bien, puedes usar la versión de sistema (Linux, MacOS).
* [Requests](https://docs.python-requests.org/en/master/) (instalar con `pip install requests` o con tu gestor de paquetes preferido).
* [lxml](https://lxml.de/installation.html) (instalar con `pip install lxml` o con tu gestor de paquetes preferido).
* [Pandas](https://pandas.pydata.org/) (instalar con `pip install pandas` o con tu gestor de paquetes preferido).
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) (instalar con `pip install openpyxl` o con tu gestor de paquetes preferido).

Uso
===

El script toma ruts desde un archivo, o bien como argumentos desde `stdin`.

* Para leer los archivos desde un archivo, se llama al script del siguiente modo:


`python3 nombre_rut_firma.py --ruts "rut1" "rut2" "rut3" ... "rut n"`


Esto bajará los rut indicados, insertando los campos en la base SQLite `ruts.db`, tabla `ruts`. De no existir el archivo `ruts.db`
se creará automáticamente junto a la tabla. Si existiera el archivo `ruts.db`, los nuevos registros serán anexados al final de la tabla.

Al tomar desde un archivo, el script debe ser invocado como sigue:


* `python3 nombre_rut_firma.py --lista-rut "ruta a archivo con ruts (csv o xlsx)" --delim "delimitador"`. 


Esto leerá la primera columna del archivo indicado en la ruta y bajará la información de los ruts que existan. 
La opción `--delim` es utilizada para archivos de texto y refiere al delimitador de columnas del archivo. Por defecto y en caso de no indicar la opción, se utiliza `;`.

Para exportar la base de datos del archivo `ruts.db`, se llama al script como sigue:

* `python3 nombre_rut_firma.py --exportar-bd "ruta a carpeta destino"`. 


Esto volcará los datos existentes a un archivo Excel (.xlsx) a la carpeta indicada.

  