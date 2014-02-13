# -*- coding: utf-8 -*-

import config
import pymongo
from datetime import *
from urllib2 import *
import urllib
import time

def conectar(collection):
	# Connection to Mongo DB
	try:
	    conn=pymongo.MongoClient()
	    print "Conectada la base de datos"
	except pymongo.errors.ConnectionFailure, e:
	   print "FALLO MONGO, MALDITA SEA: %s" % e 
	
	# Busca una base de datos y si no, la crea
	db=conn['db_p3DAI']

	# Busca una colección y si no, la crea
	col = db.users
	if collection == 'users':
		col = db.users
	if collection == 'rssFile':
		col = db.rssFile

	return col


def setUsuario(datos):
	colUsuarios=conectar()

	dto={
		'nombre':datos.nombre,
		'apellidos':datos.apellidos,
		'dni':datos.dni,
		'email':datos.email,
		'dia':datos.dia,
		'mes':datos.mes,
		'anio':datos.anio,
		'direccion':datos.direccion,
		'username':datos.username,
		'password':datos.password1,
		'formaPago':datos.formaPago
		}
	
	if datos.formaPago=="VISA":
		dto['visa']=datos.visa

	colUsuarios.insert(dto)
	print "Usuario insertado correctamente"


def getUsuario(nombreUs):
	colUsuarios=conectar()

	return colUsuarios.find_one({'username':nombreUs})


def modifyUser(nombreUs, datos):

	baseDeDatos = conectar()
	
	if datos.passwordNuevo!='':
		passwd=datos.passwordNuevo
	else:
		user=getUsuario(username)
		passwd=user['password']

	dto={
		'nombre':datos.nombre,
		'apellidos':datos.apellidos,
		'dni':datos.dni,
		'email':datos.email,
		'dia':datos.dia,
		'mes':datos.mes,
		'anio':datos.anio,
		'direccion':datos.direccion,
		'username':username,
		'password':passwd,
		'formaPago':datos.formaPago
		}
	
	if datos.formaPago=="VISA":
		dto['visa']=datos.visa

	baseDeDatos.update({'username':username},dto)

def updateRSSFile(url,fileName):
	# Buscamos el fichero en la BD:
	col=conectar('rssFile')
	file=col.find_one({'fileName':fileName})
	print file

	dto={
		'date':int(time.time()),
		'fileName':fileName
		}

	if file==None:
		print 'Descargando por primera vez RSS'
		#Descaramos el archivo:
		a,b=urllib.urlretrieve(url,r'./'+fileName)
		# Guardamos la info en la BD:
		col.insert(dto)
	else:
		previousDate=file['date']
		actualDate=int(time.time())
		#Comprobamos que la diferencia sea mayor que 10 min para actualizar:
		elapsedTime=int((actualDate-previousDate)/60)
#		if elapsedTime>10:
		print 'Actualizando archivo RSS'
		#Descaramos el archivo:
		a,b=urllib.urlretrieve(url,r'./'+fileName)
		#Actualizamos la info en la BD:
		col.update({'fileName':fileName},dto)
#		else:
#			print 'No es necesario actualizar'