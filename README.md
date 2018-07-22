# rutificador_nombrerutfirma
### Rutificador automático que descarga información desde sitio [nombrerutyfirma.cl](https://nombrerutyfirma.cl) (Chile), utilizando [Selenium with Python](http://selenium-python.readthedocs.io) y [PhantomJS](http://phantomjs.org).

* * *

## Aviso Importante

El presente proyecto no tiene relación alguna con el sitio [nombrerutyfirma.cl](https://nombrerutyfirma.cl) ni con los datos almacenados en el mismo, ni tampoco con sus creadores/administradores. El presente código sólo sirve como medio de consulta a la base de datos alojada en [nombrerutyfirma.cl](https://nombrerutyfirma.cl). El autor se desliga de cualquier responsabilidad derivada del uso del presente código.

## Rutificador

El código de este repositorio permite, dada una lista de ruts suministrada por el usuario, la descarga automática de su información asociada, en el caso de que dicho(s) RUT(s) se encuentre(n) en la base de datos mantenida por nombrerutyfirma.cl (Esto es: Nombre Completo, RUT, Sexo, Dirección y Comuna).

## Requisitos

- [Python 3.6 o superior](https://www.python.org/downloads/).
- [Selenium-Python](http://selenium-python.readthedocs.io) (instalado con <code>pip install selenium</code>).
- [PhantomJS](http://phantomjs.org/download.html). 
  
[Homebrew](https://brew.sh) ofrece a los usuarios Mac instalar todas estas dependencias de manera fácil desde una ventana Terminal, ejecutando:

<code>/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"</code>

Ello instalará Homebrew en el caso que no esté instalado en el sistema. El instalador preguntará contraseña de administrador.

Luego, ejecutar:

<code>brew install python phantomjs</code>

<code>pip3 install selenium</code>

## Uso

Primero, se debe generar un archivo que contenga los ruts a consultar, con extensión csv, el cual en su primera columna deberá contener los ruts, con o sin guión/separadores de miles. Este archivo deberá ser llamado ruts.csv y tiene que ser guardado en la misma carpeta del script y en codificación UTF-8.

**La separación utilizada para el CSV es ";" (punto y coma).**

El script debe ser ejecutado desde una terminal, mediante el comando:

<code> python3 nombre_rut_firma.py </code>

El script leerá los ruts uno a uno y los irá guardando en un archivo de salida ruts_out.csv guardado en la misma carpeta del script. El script finalizará en tanto se hayan terminado los ruts a consultar. Por otra parte, la ejecución puede ser interrumpida en cualquier momento presionando las teclas Ctrl + C en la ventana del terminal. Ello guardará la información hasta el último rut que se haya consultado en el archivo de salida.

El archivo csv de entrada (ruts.csv) debe tener codificación UTF-8. El archivo de salida tiene codificación UTF-8.

**Este repositorio incluye un archivo ruts.csv, con ruts de personajes públicos del país (a modo de ejemplo).**

## TODO (pendientes)

- Lectura de ruts de un archivo distinto a ruts.csv.
- Generador de ruts a partir de rango dado en STDIN.
- Permitir pausar/reanudar.
- Implementar en contenedor Docker.
- Integrar con TOR para cambiar ip cada n consultas.

## Limitaciones

- Este script puede dejar de funcionar en el momento en el cual el sitio empiece a implementar CAPTCHAs, en este caso, no sería posible la recolección de datos automática dado el avance actual en este tipo de pruebas de Turing.
