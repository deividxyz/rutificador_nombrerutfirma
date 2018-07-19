# rutificador_nombrerutfirma
### Rutificador automático que descarga información desde sitio [nombrerutyfirma.cl](https://nombrerutyfirma.cl) (Chile), utilizando [Selenium with Python](http://selenium-python.readthedocs.io) y [PhantomJS](http://phantomjs.org).

* * *

## Aviso Importante

El presente proyecto no tiene relación alguna con el sitio [nombrerutyfirma.cl](https://nombrerutyfirma.cl) ni con los datos almacenados en el mismo, ni tampoco con sus creadores/administradores. El presente código sólo sirve como medio de consulta a la base de datos alojada en [nombrerutyfirma.cl](https://nombrerutyfirma.cl). El autor se desliga de cualquier responsabilidad derivada del uso del presente código.

## Rutificador

El código de este repositorio permite, dada una lista de ruts suministrada por el usuario, la descarga automática de su información asociada, en el caso de que dicho(s) RUT(s) se encuentre(n) en la base de datos mantenida por nombrerutyfirma.cl (Esto es: Nombre Completo, RUT, Sexo, Dirección y Comuna).

## Requisitos

### Versión corta

- Python 3.6 (https://www.python.org/getit/).
- Ejecutar <code>pip install selenium</code> en consola/terminal/cmd.exe
- PhantomJS (http://phantomjs.org/download.html), extraer archivo .zip y copiar archivo <code>phantomjs.exe</code> de la carpeta bin en carpeta <code>C:\Windows</code> en **sistemas Windows**. 
  
  **En sistemas Mac/Linux**, copiar archivo <code>phantomjs</code> de la carpeta bin a carpeta <code>/usr/local/bin</code>.

### Explicación larga (TL;DR)

Para ejecutar el proyecto, es preciso tener una instalación de Python 3.6 compatible, con el paquete de Python (instalado con <code>pip</code>) Selenium. Además se debe instalar PhantomJS (http://phantomjs.org/download.html), y copiar el archivo ejecutable a una carpeta del <code>$PATH</code> de sistema (ej. en carpeta /usr/local/bin).

De cualquier modo, al momento de la redacción de este documento, estos requisitos pueden ser instalados de manera relativamente fácil mediante, por ejemplo, utilizando [MacPorts](https://www.macports.org/install.php) o [Homebrew](https://brew.sh/) en sistemas Mac OS X. En sistemas Linux, estos paquetes son instalables mediante apt-get o similares dependiendo de la distribución, y en Windows, la forma recomendada es instalarlos con una distribución Python como [Anaconda](https://www.anaconda.com/download/#macos).

## Uso

Primero, se debe generar un archivo que contenga los ruts a consultar, con extensión csv, el cual en su primera columna deberá contener los ruts, con o sin guión/separadores de miles. Este archivo deberá ser llamado ruts.csv y tiene que ser guardado en la misma carpeta del script y en codificación UTF-8.

**La separación utilizada para el CSV es ";" (punto y coma, semicolon, como quiera llamarlo).**

El script debe ser ejecutado desde una terminal, mediante el comando:

<code> python3 nombre_rut_firma.py </code>

El script leerá los ruts uno a uno y los irá guardando en un archivo de salida ruts_out.csv guardado en la misma carpeta del script. El script finalizará en tanto se hayan terminado los ruts a consultar. Por otra parte, la ejecución puede ser interrumpida en cualquier momento presionando las teclas Ctrl + C en la ventana del terminal. Ello guardará la información hasta el último rut que se haya consultado en el archivo de salida.

El archivo csv de entrada (ruts.csv) debe tener codificación UTF-8. El archivo de salida tiene codificación UTF-8.

**Este repositorio incluye un archivo ruts.csv, con ruts de personajes públicos del país (a modo de ejemplo).**

## TODO (pendientes)

- Lectura de ruts de un archivo distinto a ruts.csv.
- Permitir pausar/reanudar.
- Implementar en contenedor Docker.
- Integrar con TOR para cambiar ip cada n consultas.

## Limitaciones

- Este script puede dejar de funcionar en el momento en el cual el sitio empiece a implementar CAPTCHAs, en este caso, no sería posible la recolección de datos automática dado el avance actual en este tipo de pruebas de Turing.
