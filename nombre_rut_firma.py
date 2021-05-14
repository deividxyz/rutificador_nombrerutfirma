#!/usr/bin/env python3

import argparse
import os
import pathlib
import nombrerutfirma_util as ut
import sys


parser = argparse.ArgumentParser(description="Descarga información de nombrerutyfirma.com", epilog='https://deivid.xyz/')
parser.add_argument('--ruts', type=str, nargs='*', help='RUT(s) a procesar. Estos deben tener el guion y DV, o bien, estar sin guion y sin DV.', required=False)
parser.add_argument('--ruta-bd', type=pathlib.Path, help='Ruta a la base de datos. Por defecto se utiliza el directorio donde se encuentra el script.', required=False)
parser.add_argument('--lista-rut', type=pathlib.Path, help='Ruta a archivo con lista de RUT a procesar. Espera que la primera columna contenga los RUT.', required=False)
parser.add_argument('--delim', type=str, help='Delimitador de texto, para leer lista de RUT. Por defecto es ";".', default=';', required=False)
parser.add_argument('--exportar-bd', type=pathlib.Path, help='Vuelca los contenidos de la BD a un archivo Excel a guardar en la carpeta indicada.', required=False)
parser.add_argument('--generar-ruts', type=int, nargs=2, help='Genera lista de ruts, tomando como intervalo los enteros señalados con el argumento.', required=False)
parser.add_argument('--debug', action='store_true', help='Usar para mostrar información de depuración. Permite ver solicitudes al servidor y depurar errores.', required=False)
parser.add_argument('--habilitar-tor', action='store_true', help='Habilita la integración con Tor para eludir bloqueos de IP. Necesita dependencias.')

p = parser.parse_args()

if p.debug == True:
    print('Estamos depurando!!!')
    debug = True
else:
    debug = False

if p.habilitar_tor == True:
    tor = True
    torPid = ut.invokeTor()
    if torPid is None:
        print('No se pudo llamar a Tor, saliendo')
    else:
        print('Tor activado, PID: {pid}'.format(pid=torPid))
        for intento in range(10):
            print('Intento de conexión: {intento}'.format(intento=intento))
            rt = ut.chkTor(intento)
            if rt != False:
                print('')
                break # ya conectamos
else:
    tor = False

if p.ruts != None and p.lista_rut != None:

    print("No se permiten ambos argumentos al mismo tiempo, saliendo ...")
    
elif p.ruts != None:

    if p.ruta_bd != None:

        con = ut.connectDB(p.ruta_bd)
    else:

        con = ut.connectDB("./ruts.db")

    if ut.chkTable(con) == False:
        ut.crearTabla(con)

    for x in p.ruts:

        # evaluar si estamos ok con la solicitud
        if p.habilitar_tor == True:
            respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=True, tor_renewflag=False)

        else:
            respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=False, tor_renewflag=False)

        if respuesta == 'banhammer' and p.habilitar_tor == False:
            break

        elif respuesta == 'banhammer' and p.habilitar_tor == True:
            while respuesta == 'banhammer':
                respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=True, tor_renewflag=True)

        elif respuesta == 'not-found':
            continue

        else: 
            nombre, rut, sexo, direccion, comuna = ut.buscarRut(respuesta)
            ut.insertRUT(con, nombre, rut, sexo, direccion, comuna)
    
    con.close()
    
elif p.lista_rut != None:
    
    try:

        if p.ruta_bd != None:
            con = ut.connectDB(p.ruta_bd)
        
        else:
            con = ut.connectDB("./ruts.db")
            
        if ut.chkTable(con) == False:
            ut.crearTabla(con)

        ruts = ut.leerListaRUT(p.lista_rut, p.delim)
        ruts_pendientes = ruts.copy(deep=True) # lista con ruts pendientes
        
        for i, x in ruts.iteritems():

            if p.habilitar_tor == True:
                respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=True, tor_renewflag=False)

            else:
                respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=False, tor_renewflag=False)

            if respuesta == 'banhammer' and p.habilitar_tor == False:
                break
            elif respuesta == 'banhammer' and p.habilitar_tor == True:
                while respuesta == 'banhammer':
                    respuesta = ut.getStuff(ut.cleanse(x), debug, tor_status=True, tor_renewflag=True)

            elif respuesta == 'not-found':
                continue
            else: 
                
                nombre, rut, sexo, direccion, comuna = ut.buscarRut(respuesta)
                ut.insertRUT(con, nombre, rut, sexo, direccion, comuna)
                ruts_pendientes.pop(i) # sacamos el rut de los pendientes    
        
        con.close()

    except KeyboardInterrupt:

        print("Cerrando proceso, rescatando ruts pendientes...")
        path = input('Favor indicar ruta donde guardar ruts pendientes: ')
        ut.exportPending(ruts_pendientes, path)
        con.close()

elif p.exportar_bd != None:

    if p.ruta_bd != None:

        con = ut.connectDB(p.ruta_bd)

    else:

        con = ut.connectDB("./ruts.db")

    if ut.chkTable(con) == False:

        print("La tabla ruts no se encuentra en la base de datos. Verifica que el archivo tenga la tabla o que no esté en blanco.")
    
    else:
        
        ut.exportToCSV(con, p.exportar_bd)

elif p.generar_ruts != None:
    
    lista_destino = []
    x = p.generar_ruts[0]
    rut_generado = ''

    try:

        while x <= p.generar_ruts[1]:

            rut_generado = ut.generaRut(x)
            lista_destino.append(rut_generado)
            x = x + 1

        path = input("Favor indicar donde guardar ruts generados: ")
        ut.guardaRutGenerados(lista_destino, path)

    except KeyboardInterrupt:

        print('Guardando ruts generados ...')
        path = input("Favor indicar donde guardar ruts generados: ")
        ut.guardaRutGenerados(lista_destino, path)

else:
    
    parser.print_help(sys.stderr)
    print("")
    print("No se indicaron argumentos, saliendo ...")

    if p.habilitar_tor == True:
        os.kill(torPid,9)
