# -*- coding: utf-8 -*-


import web
import config
import operator
from formulario import *
import database
import re
from view import *
from web.contrib.template import render_mako
from web import form
import tweepy
from lxml import etree

web.config.debug = False


#from mako.template import Template
#from mako.lookup import TemplateLookup

urls = (
    '/formulario', 'formulario',
    '/', 'index',
    '/user_data', 'user_data',
    '/acceder', 'acceder',
    '/user_data', 'user_data',
    '/cerrarSesion', 'cerrarSesion',
    '/chart', 'chart',
    '/maps', 'maps',
    '/twitter', 'twitter',
    '/rss', 'rss'
)

ultimaVisita = ""
penultimaVisita = ""
antepenultimaVisita = ""
visitados = [ultimaVisita, penultimaVisita, antepenultimaVisita]
longitud = 0;

app = web.application(urls, locals())

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':'', 'username':''})

formularioLogin=formularioLogin()
formularioData =formularioUserData()


def comprobarSesion():
    UsuarioActivo = session.usuario
    return UsuarioActivo

class index:
    def GET(self):
        visitados.append('Inicio')
        ultimaVisita = 'Inicio'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
        args={'title':'Inicio', 'texto':'Columna izquierda que se ha pasado como argumento en el archivo code.py','formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        
        usuario = session.usuario
        if usuario:
            args['sesion']=usuario

    	return serve_template('index.html', **args)

class chart:
    def GET(self):
        visitados.append('Inicio')
        ultimaVisita = 'Inicio'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
        args={'title':'Diagramas', 'texto':'Columna izquierda que se ha pasado como argumento en el archivo code.py','formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        usuario = session.usuario
        if usuario:
            args['sesion']=usuario

        return serve_template('chart.html', **args)

class twitter:    
    def GET(self):
        visitados.append('Inicio')
        ultimaVisita = 'Inicio'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
        
        args={'title':'Twitter', 'formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        usuario = session.usuario
        if usuario:
            args['sesion']=usuario

        # Declaración de variables necesarias
        contenidoTimeline=[]
        userCount=dict()

        # Autenticación
        CONSUMER_KEY = 'pIx2uGG2KtL4P7Nqq8S5w'
        CONSUMER_SECRET = '0G8hvgOHsjfIOQtxMoIyJqGTBx2q6dzuULPtEpLnwhQ'

        ACCESS_TOKEN = '425972620-Bbt3hU0wYTCPnu6HZknStmDUCUljD27hSRZzI1WS'
        ACCESS_TOKEN_SECRET = '91403VyyoJKMu8B4la8muTEritAUIp1KXR5gG1RRK7b59'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        timeline = api.home_timeline()

        # Lo guardamos en un diccionario para facilitar su manejo
        for i in range(0, len(timeline)):
            tweet = timeline[i]
            scrname='@'+tweet.user.screen_name
            contenidoTimeline.insert(i, {
                'usuario':tweet.user.screen_name,
                'contenido':unicode(tweet.text),
                'fecha':tweet.created_at,
                })
            if scrname in userCount.keys():
                userCount[scrname]+=1
            else:
                userCount[scrname]=1

        ordena_userCount = sorted(userCount.iteritems(), key=operator.itemgetter(1), reverse=True)

        args['users']=ordena_userCount

        args['Timeline'] = contenidoTimeline

        return serve_template('twitter.html', **args)

class maps:
    def GET(self):
        visitados.append('Inicio')
        ultimaVisita = 'Inicio'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
        
        args={'title':'Maps', 'texto':'Columna izquierda que se ha pasado como argumento en el archivo code.py','formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        usuario = session.usuario
        if usuario:
            args['sesion']=usuario

        return serve_template('maps.html', **args)

class rss:
    def GET(self):

        args={'title':'RSS','formularioLogin':formularioLogin}
        
        #Actualización de los ficheros RSS que se van a utlizar:
        fileName='ultimas_noticias.xml'
        url='http://ep00.epimg.net/rss/tags/ultimas_noticias.xml'
        database.updateRSSFile(url,fileName)
        
        tree=etree.parse(fileName)
        items=tree.xpath('//channel/item')

        #print(items)

        newsDict=dict()
        for i in range(0,len(items)):
            newsDict[i]=dict()

            #Añadir el título
            tit=items[i].xpath('title/text()')
            if len(tit)>0:
                newsDict[i]['titulo']=tit[0]            

            #Añadir el autor
            creator = items[i].xpath('dc:creator/text()', namespaces=items[i].nsmap)
            if len(creator)>0:
                newsDict[i]['autor']=creator[0]            

            #Miniatura:
            thumbnail=items[i].xpath('enclosure/@url')
            if len(thumbnail)>1:
                newsDict[i]['imagen']=thumbnail[1]

            #Contenido:
            content=items[i].xpath('content:encoded/text()', namespaces=items[i].nsmap)
            if len(content)>0:
                newsDict[i]['contenido']=content[0]

            #Enlace:
            link=items[i].xpath('link/text()')
            if len(link)>0:
                newsDict[i]['enlace']=link[0]

        args['RSSFile'] = newsDict            
        return serve_template('rss.html', **args)

class formulario:
    def GET(self):
        visitados.append('Formulario')
        ultimaVisita = 'Formulario'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]

        fInscripcion = formularioInscripcion()

        args={'title':'Inscripci&oacute;n','form':fInscripcion,'formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        usuario = comprobarSesion ()
        if usuario:
            args['sesion']=usuario

        return serve_template('formulario.html',**args)

    def POST(self):
        visitados.append('Inicio')
        ultimaVisita = 'Inicio'
        longitud = len(visitados)
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]

        fInscripcion = formularioInscripcion()


        args={'title':'Inscripci&oacute;n','form':fInscripcion,'formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}

        if fInscripcion.validates():
            datosUsuario = web.input()
            nombreUsuario = datosUsuario.username
            if database.getUsuario(nombreUsuario) == None:
                database.setUsuario(datosUsuario)
                args['Accepted'] = True
            else:
                args['Accepted'] = False
                args['Error'] = 'Nombre de usuario ya utilizado'
        else:
            args['Accepted'] = False
        
        return serve_template('formulario.html',**args)

class user_data:
    def GET(self):
        visitados.append('Datos')
        ultimaVisita = 'Datos'
        longitud = len(visitados)
        if longitud >= 2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
        
        args={'title':'Datos del usuario','form':formularioData,'formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        
        usuario = comprobarSesion ()
        if usuario:
            args['sesion']=usuario

        datos_usuario = database.getUsuario(session.username)

        formularioData.nombre.value=datos_usuario['nombre']
        formularioData.apellidos.value=datos_usuario['apellidos']
        formularioData.dni.value=datos_usuario['dni']
        formularioData.email.value=datos_usuario['email']
        formularioData.dia.value=int(datos_usuario['dia'])
        formularioData.mes.value=int(datos_usuario['mes'])
        formularioData.anio.value=int(datos_usuario['anio'])
        formularioData.direccion.value=datos_usuario['direccion']
        formularioData.username.value=session.username
        formularioData.formaPago.value=datos_usuario['formaPago']
        if 'visa' in datos_usuario.keys():
            formularioData.visa.value=datos_usuario['visa']

        return serve_template('user_data.html', **args)

    def POST(self):

        longitud = len(visitados)
        ultimaVisita = visitados[longitud-1]
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]

        args={'title':'Formulario de inscripci&oacute;n', 'form':formularioData ,'formularioLogin':formularioLogin, 'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
        
        if formularioData.validates(): 
            args['Accepted']=True
            datos=web.input()
            database.modifyUser(session.username,datos)           
        else:
            args['Accepted']=False

        user = comprobarSesion ()

        datos_usuario=database.getUsuario(session.username)

        formularioData.nombre.value=datos_usuario['nombre']
        formularioData.apellidos.value=datos_usuario['apellidos']
        formularioData.dni.value=datos_usuario['dni']
        formularioData.email.value=datos_usuario['email']
        formularioData.dia.value=int(datos_usuario['dia'])
        formularioData.mes.value=int(datos_usuario['mes'])
        formularioData.anio.value=int(datos_usuario['anio'])
        formularioData.direccion.value=datos_usuario['direccion']
        formularioData.username.value=session.username
        formularioData.formaPago.value=datos_usuario['formaPago']
        if 'visa' in datos_usuario.keys():
            formularioData.visa.value=datos_usuario['visa']

        return serve_template('user_data.html',**args)


class acceder:
    def POST(self):
        i = web.input()
        usuario  = i.username
        password = i.password
        longitud = len(visitados)
        ultimaVisita = visitados[longitud-1]
        if longitud >=2:
            penultimaVisita = visitados[longitud-2]
            if longitud>=3:
                antepenultimaVisita = visitados[longitud-3]
    
        datos_usuario=database.getUsuario(usuario)
        if datos_usuario != None:
            passwordCorrecto = datos_usuario['password']
            if password==passwordCorrecto:
                session.usuario = datos_usuario['nombre'] 
                session.username = datos_usuario['username']
                return web.redirect('/')
            else:
                args={'title':'Pr&aacutectica DAI', 'texto':'Columna de la izquierda', 'formularioLogin':formularioLogin,'msg':u'Contraseña incorrectos',  'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
                return serve_template('index.html', **args)
        else:
            args={'title':'Pr&aacutectica DAI', 'texto':'Columna de la izquierda', 'formularioLogin':formularioLogin,'msg':u'El usuario introducido no existe',  'ultimaVisita':ultimaVisita, 'penultimaVisita':penultimaVisita, 'antepenultimaVisita':antepenultimaVisita}
            return serve_template('index.html', **args)
            
class cerrarSesion:
    def GET(self):
        session.kill()
        ultimaVisita = ""
        penultimaVisita = ""
        antepenultimaVisita = ""
        return web.redirect('/')


if __name__ == "__main__":
    app.internalerror = web.debugerror
    app.run()