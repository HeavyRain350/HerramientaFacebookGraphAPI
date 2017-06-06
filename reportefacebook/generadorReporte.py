# coding: utf-8
#290014684349117?fields=insights.period(day).metric(page_impressions_by_city_unique,page_impressions_by_age_gender_unique).since(20-03-2017).until(25-03-2017)
#Generar archivo html apartir de un archivo Rmd(markdown) desde consola
#Rscript -e "require('knitr'); require('markdown'); knit('Nombre archivo.Rmd','Nombre salida.md'); markdownToHTML('nombre Archivo.md','nombre salida.html')"
#Rscript -e "require('knitr'); rmarkdown::render('ReporteSemanalFacebook.Rmd', encoding = 'UTF-8')"
#35 20 15 15 10 5
from facepy import GraphAPI,utils
from dateutil import parser
from datetime import datetime, date, timedelta
import json
import facebook
import time
import csv

class GeneradorReporte:
  def getCountByReaction(self,reaction, idPost):
    graph = self.inicializarGraph()
    response = graph.get(idPost+'?fields=reactions.type('+reaction+').summary(TRUE)', page=True, retry=5)
    count = 0
    for resp in response:
      count = int(resp['reactions']['summary']['total_count'])

    return count

  def calcularCalificacionPost(self,normAlcance, normReactions, normShares, formula):
    result = normAlcance * formula[0] + (normReactions[0] * formula[3]+ normReactions[1] * formula[4] + normReactions[2] * formula[5]
        + normReactions[3] * formula[6] + normReactions[4] * formula[7]+ normReactions[5] * formula[8]) * formula[1] + normShares * formula[2]
    return result

  def normalizarMinMax(self,numero, maximo, minimo):
    result = 0
    try:
      result = float((numero - minimo))/float((maximo - minimo))
    except:
      result = 1.0
    return result

  def inicializarGraph(self):
     access_token = 'EAAUFPkgRnQYBANdbjHV30K9vA1BzPmDZBqm95CZAb8OB6rTCGZBCV7KhcZBqIrLmyLakmKZCgKqWyPvj4Nke5dQUzRXs6pXt72EwPLSw37DLQOYw6l8LXbkgUTNsWs75J5Caqum8moWNaj8ZB6BE5j93TJVZBUeAIY7DyyubOwitAZDZD'
     graph = GraphAPI(access_token,version='2.8')
     return graph

  def generarReporte(self):
    page_id = '290014684349117'
    

    config = {}
    formula = []

    with open("configuracion.txt") as f:
        for line in f:
         (key, val) = line.split()
         if(key== "correos"):
          correos = []
          for v in val.split(","):
            correos.append(v)
          config[key] = correos
         elif(key== "formula"):
          formula.append(float(val))
         else:
          config[key] = datetime.strptime(val,'%Y-%m-%d')

    graph = self.inicializarGraph()

    datos = graph.get(page_id+'/posts?fields=created_time,shares,message,reactions.summary(TRUE),'+
        'insights.metric(post_impressions_unique,post_impressions_by_paid_non_paid_unique)', page=True, retry=5)

    datosCiudades = graph.get(page_id+'?fields=insights.period(day).metric(page_impressions_by_city_unique)'+
            '.since('+config['inicio'].strftime('%d-%m-%Y')+').until('+config['fin'].strftime('%d-%m-%Y')+')', page=True, retry=5)

    datosEdades = graph.get(page_id+'?fields=insights.period(day).metric(page_impressions_by_age_gender_unique)'+
            '.since('+config['inicio'].strftime('%d-%m-%Y')+').until('+config['fin'].strftime('%d-%m-%Y')+')', page=True, retry=5)

    boolean = True

    listaPosts = []
    listaPostsTopThree = []

    listaShares = []
    listaReactions = []
    listaAlcance = []

    listaLikes = []
    listaLoves = []
    listaHahas = []
    listaWows = []
    listaSad = []
    listaAngry = []

    diccionarioPost = {}
    diccionarioCiudades = {}
    diccionarioEdades = {}

    for data in datos:

        for d,x in data.items():  

            for item in x:
              
              try:

                fecha = item['created_time']
                fechaParse = parser.parse(fecha)
                fecha_final = fechaParse.strftime('%d-%m-%Y')

                #Se compara si ese post esta dentro de los 7 dias anteriores
                #Se esta poniendo a la hora 6 porque el resultado que regresa la api de facebook esta 6 horas adelantado
                if str(fechaParse) < config['fin'].strftime('%Y-%m-%d 06:00:00') and str(fechaParse) >= config['inicio'].strftime('%Y-%m-%d 06:00:00'):
                  
                  diccionarioPost = {}
                  boolean = True

                  likesCount = 0
                  loveCount = 0
                  hahaCount = 0
                  wowCount = 0
                  sadCount = 0
                  angryCount = 0


                  likesCount = self.getCountByReaction("LIKE",item['id'])
                  loveCount = self.getCountByReaction("LOVE",item['id'])
                  hahaCount = self.getCountByReaction("HAHA",item['id'])
                  wowCount = self.getCountByReaction("WOW",item['id'])
                  sadCount = self.getCountByReaction("SAD",item['id'])
                  angryCount = self.getCountByReaction("ANGRY",item['id'])
                  
                  alcance = item['insights']['data'][0]['values'][0]['value']
                  alcancePagado = item['insights']['data'][1]['values'][0]['value']['paid']
                  alcanceOrganico = item['insights']['data'][1]['values'][0]['value']['unpaid']
                  
                  reactionsCount = item['reactions']['summary']['total_count']

                  diccionarioPost = {'message':item['message'].encode('utf-8'), 'fecha':fecha_final, 'likesCount':likesCount, 'lovesCount':loveCount, 'hahaCount':hahaCount,
                    'wowCount':wowCount, 'sadCount':sadCount, 'angryCount':angryCount, 'alcance':alcance,'alcancePagado':alcancePagado,
                    'alcanceOrganico':alcanceOrganico, 'shares':0, 'reactionsCount':reactionsCount,'calificacion':0}
                  
                  listaPosts.append(diccionarioPost)

                  diccionarioPost = {'message':item['message'].encode('utf-8'), 'fecha':fecha_final, 'likesCount':likesCount, 'lovesCount':loveCount, 'hahaCount':hahaCount,
                    'wowCount':wowCount, 'sadCount':sadCount, 'angryCount':angryCount, 'alcance':alcance,'alcancePagado':alcancePagado,
                    'alcanceOrganico':alcanceOrganico, 'shares':item['shares']['count'],'reactionsCount':reactionsCount,'calificacion':0}

                  listaPosts.pop()
                  listaPosts.append(diccionarioPost)

              except Exception as e:
                #print e
                pass


    for data in datosCiudades:
      for d,x in data.items():
        try:
          for days in x['data'][0]['values']:
            for ciudad,cantidad in days['value'].items():
              if ciudad in diccionarioCiudades:
                diccionarioCiudades[ciudad.encode('utf-8')] += cantidad
              else:
                diccionarioCiudades[ciudad.encode('utf-8')] = cantidad
        except Exception as e:
          print e
          pass


    for data in datosEdades:
      for d,x in data.items():
        try:
          for days in x['data'][0]['values']:
            for demografia,cantidad in days['value'].items():
              if demografia in diccionarioEdades:
                diccionarioEdades[demografia] += cantidad
              else:
                diccionarioEdades[demografia] = cantidad
        except Exception as e:
          #print e
          pass



    for i in listaPosts:

      listaAlcance.append(i['alcance'])
      listaReactions.append(i['reactionsCount'])
      listaShares.append(i['shares'])

      listaLikes.append(i['likesCount'])
      listaLoves.append(i['lovesCount'])
      listaHahas.append(i['hahaCount'])
      listaWows.append(i['wowCount'])
      listaSad.append(i['sadCount'])
      listaAngry.append(i['angryCount'])

    for i in listaPosts:
      alcanceNorm = self.normalizarMinMax(i['alcance'],max(listaAlcance),min(listaAlcance))
      #reaccionesNorm = normalizarMinMax(i['reactionsCount'],max(listaReactions),min(listaReactions))
      sharesNorm = self.normalizarMinMax(i['shares'],max(listaShares),min(listaShares))

      likeNorm = self.normalizarMinMax(i['likesCount'],max(listaLikes),min(listaLikes))
      loveNorm = self.normalizarMinMax(i['lovesCount'],max(listaLoves),min(listaLoves))
      hahaNorm = self.normalizarMinMax(i['hahaCount'],max(listaHahas),min(listaHahas))
      wowNorm = self.normalizarMinMax(i['wowCount'],max(listaWows),min(listaWows))
      sadNorm = self.normalizarMinMax(i['sadCount'],max(listaSad),min(listaSad))
      angryNorm = self.normalizarMinMax(i['angryCount'],max(listaAngry),min(listaAngry))

      i['calificacion'] = self.calcularCalificacionPost(alcanceNorm,[likeNorm,loveNorm,hahaNorm,wowNorm,sadNorm,angryNorm], sharesNorm, formula)


    listaPosts.sort(key=lambda x: x['calificacion'],
        reverse=True)

    for i in range(3):
      listaPostsTopThree.append(listaPosts[i])


    for i in listaPostsTopThree:
      i['message'] = i['message'].replace("\n"," ")

    with open("Datos Posts.csv", "w") as f:
      archivoDatos_csv = csv.writer(f, delimiter=",")
      archivoDatos_csv.writerow(listaPostsTopThree[0].keys())

      for i in listaPostsTopThree:
        archivoDatos_csv.writerow(i.values())
    f.close()

    listaCities = diccionarioCiudades.items()
    listaCities.sort(key=lambda x: x[1],
        reverse=True)

    listaAges = diccionarioEdades.items()
    listaAges.sort(key=lambda x: x[1],
        reverse=True)

    with open("Datos Ciudades.csv", "w") as f:
      archivoDatos_csv = csv.writer(f, delimiter=",")
      archivoDatos_csv.writerow(["Ciudad","Cantidad"])

      for i in listaCities:
        archivoDatos_csv.writerow(i)
    f.close()

    with open("Datos Demograficos.csv", "w") as f:
      archivoDatos_csv = csv.writer(f, delimiter=",")
      archivoDatos_csv.writerow(["Demografia","Cantidad"])

      for i in listaAges:
        archivoDatos_csv.writerow(i)
    f.close()

    