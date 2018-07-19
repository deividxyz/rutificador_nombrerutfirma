#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time, sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

print('')
print('Rutificador automático para nombrerutyfirma.cl. Creado por deivid')
print('*****************************************************************')
print('')
print('Para finalizar el proceso de manera anticipada, oprima Ctrl + C ...')
print('')

driver = webdriver.PhantomJS()
driver.get('https://nombrerutyfirma.cl')

driver.implicitly_wait(10)

filas = []

ruts_out = open('ruts_out.csv', 'w')

with open('ruts.csv', newline='', encoding='utf-8-sig') as f:
	reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
	for row in reader:
		
		driver.find_elements_by_xpath("//*[contains(text(),'RUT')]")[0].click()

		busca_rut = driver.find_elements_by_xpath("//input[@placeholder='Buscar por RUT']")[0]
		busca_rut.send_keys(row[0])
		
		print('Procesando rut: ' + row[0])

		boton = driver.find_elements_by_xpath("//div[@class='tab-pane active']//input[@type='submit']")[0]
		boton.click()

		try:

			nombre = driver.find_element_by_xpath("//tr[@tabindex='1']/td[1]").text
			rut = driver.find_element_by_xpath("//tr[@tabindex='1']/td[2]").text
			sexo = driver.find_element_by_xpath("//tr[@tabindex='1']/td[3]").text
			direccion = driver.find_element_by_xpath("//tr[@tabindex='1']/td[4]").text
			comuna = driver.find_element_by_xpath("//tr[@tabindex='1']/td[5]").text

			linea = nombre + ";" + rut + ";" + sexo + ";" + direccion + ";" + comuna

		except NoSuchElementException:

			print('El rut ' + row[0] + ' no existe en la BD, saltando ...')

		print(linea)
		print('')
		ruts_out.write(linea + '\n')

		filas.append(linea)

		sgte = driver.find_element_by_xpath("//*[contains(text(),'Buscar otro')]")
		sgte.click()

ruts_out.close()
