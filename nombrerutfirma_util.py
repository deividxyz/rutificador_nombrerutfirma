# -*- coding: utf-8 -*-
import sqlite3
import requests
import pandas as pd
from lxml import html
from datetime import datetime

def buscarRut(rut):
    
        nombre = ''
        rutSalida = ''
        secssso = '' # en la playa hay de too
        direccion = ''
        comuna = ''
        
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36", # user agent de linux
            "referer": "https://nombrerutyfirma.com/"
            }
    
        url = "https://nombrerutyfirma.com/rut?term=" + str(rut)
        xpath_columnas = "/html/body/div[2]/div/table/tbody/tr[1]/td" # Forzada a la primera fila de la tabla!
    
        response = requests.get(url, headers=headers)  # respuesta de html raw
        parser = html.fromstring(response.text) # parseada
        celdas = parser.xpath(xpath_columnas)
    
        if len(celdas) == 0:
    
            print("No se encontró RUT {} en NombreRutYFirma.com, saltando...".format(rut))
    
        else:
    
            for cuenta, celda in enumerate(celdas):
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
    return "{:_}".format(int(rut_raw)).replace("_", ".") + "-0" # nos valemos del hecho que nos deja meter rut con DV = 0

def connectDB():
    return sqlite3.connect('ruts.db')

def leerListaRUT(path, delim):
    if 'xls' in path.suffix:
        return pd.read_excel(path, sheet_name=0,header=None)[0]
    elif 'csv' in path.suffix:
        return pd.read_csv(path, sep=delim, header=None)[0]

def exportToXLSX(con, path):
    ruts = pd.read_sql_query("select * from ruts", con)
    archivo_str = "rutsprocesados_{horafecha}.xlsx".format(horafecha=str(datetime.now())[0:19])
    ruts.to_excel(path / archivo_str, index=False)
    print('Archivo guardado, con nombre: {nombre}'.format(nombre=archivo_str))