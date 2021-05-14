# -*- coding: utf-8 -*-
import sqlite3
import requests
import pandas as pd
import distutils.spawn
from lxml import html
from datetime import datetime
import subprocess
from requests_tor import RequestsTor
from requests.exceptions import ConnectionError
from time import sleep

def invokeTor():
    # checking whether tor exists in system path
    cmd = distutils.spawn.find_executable('tor')
    if cmd == None:
        print('Tal parece que Tor no existe en tu sistema. Prueba iniciandolo manualmente e intenta otra vez.')
        return None
    else:
        popen = subprocess.Popen(cmd,stdout=subprocess.DEVNULL)
        tor_pid = popen.pid
        return tor_pid

def chkTor(intentos):
    try:
        rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)
        ip = rt.get('https://icanhazip.com').text
        print('Tor conectado después de {intentos} intentos. IPv4  asignada: {ip}.'.format(intentos=intentos, ip=ip))
        return rt
    except ConnectionError:
        print('Tor aún no está listo, esperando 1 segundo ...')
        sleep(1)
        return False

def calculaDV(rut):

    # Función calculaDV tomada de https://github.com/jdeloshoyos/genrut/blob/master/genrut.py
    # (c) Junio 2013 por Jaime de los Hoyos M. Liberado bajo la licencia MIT: http://www.opensource.org/licenses/mit-license.php

    rut_str = str(rut)[::-1]  # Invierte string

    # Variables para el cálculo
    multiplicador = 2
    suma = 0
    
    for c in rut_str:
        # Iteramos sobre todos los caracteres del RUT ya,  invertido, sumando los dígitos * el multiplicador
        suma += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
        
    dv = str(11 - (suma % 11))  # 11 - Módulo
    
    # Excepciones
    if dv == '11':
        dv = '0'
    if dv == '10':
        dv = 'K'
        
    return dv
    
def generaRut(numero):

    return str(numero) + '-' + calculaDV(numero)

def buscarRut(respuesta):

    nombre = ''
    rutSalida = ''
    secssso = '' # en la playa hay de too
    direccion = ''
    comuna = ''
    
    for cuenta, celda in enumerate(respuesta):
        # print(cuenta, celda.text_content())
        if cuenta == 0:
            nombre = celda.text_content().replace("'","")
        elif cuenta == 1:
            rutSalida = celda.text_content().replace("'","")
        elif cuenta == 2:
            secssso = celda.text_content().replace("'","")
        elif cuenta == 3:
            direccion = celda.text_content().replace("'","").replace("-f", "")
        elif cuenta == 4:
            comuna = celda.text_content().replace("'","")
    
    return nombre, rutSalida, secssso, direccion, comuna

def getStuff(rut, debug, tor_status, tor_renewflag):

    # esta función genera la petición http al sitio y evaluará su estado, si efectívamente se puede usar, si tuvo un error o si fue baneada. 
    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36", # User Agent de Chrome en Windows. Windows es el SO con mayor cuota, no debiera ser necesario rotar el UA.
        "referer": "https://nombrerutyfirma.com/"
        }
    
    url = "https://nombrerutyfirma.com/rut?term=" + str(rut)

    xpath_columnas = "/html/body/div[2]/div/table/tbody/tr[1]/td" # Forzada a la primera fila de la tabla!
    xpath_titulo = '/html/head/title'

    if tor_status == True:
        rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)
        if tor_renewflag == True:
            rt.new_id()
        response = rt.get(url, headers=headers)

    else:

        response = requests.get(url, headers=headers)  # respuesta de html raw

    parser = html.fromstring(response.text) # parseada
    titulo = parser.xpath(xpath_titulo)[0].text

    if debug == True:

        print("Acá la respuesta en html:")
        print("")
        print(response.text)
        print("")
        print(titulo)
        
    if 'Access denied' in titulo or 'Attention Required!':
        print('Baneado papu! :(, abortando los procesos ...')
        return 'banhammer'
        
    celdas = parser.xpath(xpath_columnas)
    
    if len(celdas) == 0:
        print("No se encontró RUT {rut} en NombreRutYFirma.com, saltando...".format(rut=rut))
        return 'not-found'
    
    else:
        return celdas # celdas ya validadas

def crearTabla(con):

    cursorObj = con.cursor()
    cursorObj.execute("create table \
                          ruts(rut varchar, \
                          nombre varchar, \
                          sexo varchar, \
                          direccion varchar, \
                          comuna varchar) \
                          ")
    con.commit()

def chkTable(con):

    cursorObj = con.cursor()
    cursorObj.execute("\
        SELECT count(name) \
        FROM sqlite_master \
        WHERE type='table' \
        and name='ruts'")
        
    if cursorObj.fetchone()[0] == 1:
        return True
    
    else:
        return False
    
    con = sqlite3.connect('ruts.db')
    if chkTable(con) == False:
        crearTabla(con)
        
def insertRUT(con, nombre, rut, sexo, direccion, comuna):

    if nombre != '':
        cursor = con.cursor()
        cursor.execute("insert into ruts \
                        values('{rut}', '{nombre}', \
                        '{sexo}', '{direccion}', \
                        '{comuna}')".format(rut=rut, nombre=nombre, sexo=sexo, 
                        direccion=direccion, comuna=comuna))
        con.commit()
        print("Rut {} insertado en BD...".format(rut))
        
def cleanse(rut_raw):

    if '-' in rut_raw:
        rut_raw = rut_raw[0:rut_raw.find('-')]
    rut_raw = str(rut_raw).upper().replace(".", "").replace("-", "").replace("K", "")
    return "{:_}".format(int(rut_raw)).replace("_", ".") + '-' + calculaDV(rut_raw)

def connectDB(path):

    return sqlite3.connect('ruts.db')

def leerListaRUT(path, delim):

    if 'xls' in path.suffix:
        return pd.read_excel(path, sheet_name=0,header=None)[0]

    elif 'csv' in path.suffix:
        return pd.read_csv(path, sep=delim, header=None)[0]

def exportToCSV(con, path):

    ruts = pd.read_sql_query("select * from ruts", con)
    archivo_str = "rutsprocesados_{horafecha}.csv".format(horafecha=str(datetime.now())[0:19])
    destino = pathlib.Path(path) / archivo_str
    ruts.to_csv(destino,index=False,sep=';')
    print('Archivo guardado, con nombre: {nombre}'.format(nombre=archivo_str))

def exportPending(lista_rut, path):

    archivo_str = "rutspendientes_{horafecha}.csv".format(horafecha=str(datetime.now())[0:19])
    destino = pathlib.Path(path) / archivo_str
    pd.Series(lista_rut).to_csv(destino, index=False, sep=';', header=False)
    print('Archivo guardado con los ruts pendientes, nombre: {nombre}'.format(nombre=archivo_str))

def guardaRutGenerados(lista_rut_gen, path):
    archivo_str = "rutgen_{horafecha}.csv".format(horafecha=str(datetime.now())[0:19])
    destino = pathlib.Path(path) / archivo_str
    pd.Series(lista_rut_gen).to_csv(destino, index=False, sep=';', header=False)