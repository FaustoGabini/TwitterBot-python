import json
import requests
from os import remove
import tweepy

# Credenciales de tweepy  
consumer_key = "**********"
consumer_secret = "**********"
access_token="**********"
access_token_secret="**********"

# Obtener noticias desde Google News 
url = ('http://newsapi.org/v2/top-headlines?'
       'country=ar&'
       'apiKey=44049ad6b82944aea33cc5c7af3daa3c')
response = requests.get(url)

todos = json.loads(response.text)


noticias_totales = len(todos['articles'])
d = {}
noticias = list()

# Añadimos las noticias a la lista 
for i in range(noticias_totales):
       d = {'titulo':todos['articles'][i]['title'],'descripcion':todos['articles'][i]['description'], 
       'imagen':todos['articles'][i]['urlToImage'], 'url':todos['articles'][i]['url']}
       noticias.append(d)

for i in range(noticias_totales):
       print("Noticias nro")
       print(i)
       print(noticias[i]['titulo'])
       print(noticias[i]['descripcion'])
       print(noticias[i]['imagen'])
       print(noticias[i]['url'])


# Descargar imagen de las noticias relevantes
cont = 0
for i in range(noticias_totales):
       
       try: 
              url_imagen = noticias[i]['imagen'] # El link de la imagen
              
              nombre_local_imagen = str(i) + ".jpg" # Nombre de la imagen
              imagen = requests.get(url_imagen).content
              with open(nombre_local_imagen, 'wb') as handler:
                     handler.write(imagen)
                     
              f_imagen= nombre_local_imagen
              

              auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
              auth.set_access_token(access_token, access_token_secret)
              auth.secure = True

              api = tweepy.API(auth)

              tweet = noticias[i]['titulo'] + "\n" + "Fuente: "+  noticias[i]['url']
              api.update_with_media(f_imagen,status=tweet)
              print("Tweet enviado")
              remove(nombre_local_imagen) # Eliminamos la imagen para que no quede guardada
              

       except requests.exceptions.MissingSchema:
              print("Imagen no disponible")
       
       cont = cont + 1 

