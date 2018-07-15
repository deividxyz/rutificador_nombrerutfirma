# rutificador_nombrerutfirma
Rutificador automático que descarga información desde sitio nombrerutyfirma.cl (Chile), utilizando Selenium y PhantomJS.

# Aviso Importante

El presente proyecto no tiene relación alguna con el sitio https://www.nombrerutyfirma.cl ni con los datos alojados en el mismo ni con sus creadores/administradores. El presente código por si sólo no aloja datos asociados a los rut chilenos; sólo sirve como medio de consulta a la base de datos nombrerutyfirma.cl. El autor se desliga de cualquier responsabilidad derivada del uso de este paquete de software.

# rutificador

El código de este repositorio permite, dada una lista de ruts suministrada por el usuario, la descarga automática de su información asociada en el caso de que dicho RUT se encuentre en la base de datos mantenida por nombrerutyfirma.cl (Esto es, Nombre Completo, RUT, Sexo, Dirección y Comuna).

# Requisitos

Para ejecutar el proyecto, es preciso tener una instalación de Python 3.6 compatible, con el paquete de Python (instalado con pip) Selenium. Además se debe instalar PhantomJS (http://phantomjs.org/download.html), y copiar el archivo ejecutable a una carpeta del $PATH de sistema (ej. en carpeta /usr/local/bin).

De cualquier modo, al momento de la redacción de este documento, estos requisitos pueden ser instalados de manera relativamente fácil mediante MacPorts (https://www.macports.org/install.php, en Mac OS X, requiere XCode).

# Uso

Primero, se debe generar un archivo que contenga los ruts a consultar, con extensión csv, el cual en su primera columna deberá contener los ruts con o sin guión y sin puntos separadores de miles. Este archivo deberá ser llamado ruts.csv y tiene que ser guardado en la misma carpeta del script.

El script debe ser ejecutado desde una terminal (o consola), mediante el comando:

python3 nombre_rut_firma.py

El script leerá los ruts uno a uno y los irá guardando en un archivo de salida ruts_out.csv guardado en la misma carpeta del script. El script finalizará en tanto se hayan terminado los ruts a consultar. Por otra parte, la ejecución puede ser interrumpida en cualquier momento presionando las teclas Ctrl + C. Ello guardará la información hasta el último rut consultado en el archivo de salida.

El archivo csv de entrada (ruts.csv) debe tener codificación UTF-8. El archivo de salida tiene codificación UTF-8.

# TODO (pendientes)

- Lectura de ruts de un archivo distinto a ruts.csv.
- Permitir pausar/reanudar.
- Implementar en contenedor Docker.
- Integrar con TOR para cambiar ip cada n consultas.

# Limitaciones

- Este script puede dejar de funcionar en el momento en el cual el sitio empiece a implementar CAPTCHAs, en este caso, no sería posible la recolección de datos automática dado el avance actual en este tipo de pruebas de Turing.
