#!/usr/bin/env python3

import argparse
import pathlib
import nombrerutfirma_util as ut
import sys

parser = argparse.ArgumentParser(description="Descarga información de nombrerutyfirma.com", epilog='https://deivid.xyz/')
parser.add_argument('--ruts', type=str, nargs='*', help='RUT(s) a procesar. Estos deben tener el guion y DV, o bien, estar sin guion y sin DV.', required=False)
parser.add_argument('--lista-rut', type=pathlib.Path, help='Ruta a archivo con lista de RUT a procesar. Espera que la primera columna contenga los RUT.', required=False)
parser.add_argument('--delim', type=str, help='Delimitador de texto, para leer lista de RUT. Por defecto es ";".', default=';', required=False)
parser.add_argument('--exportar-bd', type=pathlib.Path, help='Vuelca los contenidos de la BD a un archivo Excel a guardar en la carpeta indicada.', required=False)

p = parser.parse_args()

if p.ruts != None and p.lista_rut != None:
    print("No se permiten ambos argumentos al mismo tiempo, saliendo ...")
    
elif p.ruts != None:
    
    con = ut.connectDB()
    for x in p.ruts:
        
        nombre, rut, sexo, direccion, comuna = ut.buscarRut(ut.cleanse(x))
        ut.insertRUT(con, nombre, rut, sexo, direccion, comuna)
    
    con.close()
    
elif p.lista_rut != None:
    
    con = ut.connectDB()
    ruts = ut.leerListaRUT(p.lista_rut, p.delim)
    ruts_pendientes = ruts.copy(deep=True) # lista con ruts pendientes
    for i, x in ruts.iteritems():
        
        nombre, rut, sexo, direccion, comuna = ut.buscarRut(ut.cleanse(x))
        ut.insertRUT(con, nombre, rut, sexo, direccion, comuna)
        ruts_pendientes.pop(i) # sacamos el rut de los pendientes
        
    con.close()

elif p.exportar_bd != None:

    con = ut.connectDB()
    ut.exportToXLSX(con, p.exportar_bd)
    
else:
    
    parser.print_help(sys.stderr)
    print ("No se indicaron argumentos, saliendo ...")
