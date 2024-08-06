# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 19:20:50 2024

@author: Mora
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

# URL del sitio web para extraer datos
URL = 'https://www.scrapethissite.com/pages/simple/'

# Aquí accedemos a la URL
response = requests.get(URL)

# Analizamos el contenido HTML con BeautifulSoup
olla_de_carne = BeautifulSoup(response.text, 'html.parser')

# Buscamos todos los divs que contienen información de países
paises = olla_de_carne.find_all('div', class_='col-md-4 country')

# Creamos las "cajitas" para almacenar los datos que vamos a extraer
nombres_paises = []
capitales = []
poblaciones = []
areas = []

# Recorremos cada div de país para extraer la información necesaria
for pais in paises:
    nombre_pais = pais.find('h3', class_='country-name').get_text(strip=True)
    info_pais = pais.find('div', class_='country-info')
    
    capital = info_pais.find('span', class_='country-capital').get_text(strip=True)
    poblacion = info_pais.find('span', class_='country-population').get_text(strip=True)
    area = info_pais.find('span', class_='country-area').get_text(strip=True)
    
   # Añadimos los datos a nuestras listass
    nombres_paises.append(nombre_pais)
    capitales.append(capital)
    poblaciones.append(poblacion)
    areas.append(area)

# Creamos un DataFrame
df = pd.DataFrame({
    'Nombre del pais': nombres_paises,
    'Capital': capitales,
    'Poblacion': poblaciones,
    'Area (km^2)': areas
})

# Conectamos a la base de datos SQLite y guardamos el df
conn = sqlite3.connect('countries.db')
df.to_sql('Countries', conn, if_exists='replace', index=False)
conn.close()

# Aquí imprimimos para visualizarlo en el spyder
print(df)

#Aquí quise exportarlo como excel para verlo más en detalle
folder = r"D:/Mora/Documents/CETAV/II Cuatrimestre 2024/Programación para análisis de datos II - Nayib Vargas\Práctica Programada #3 Scraping/"
archivo_salida = "webscraping paises.xlsx"

df.to_excel(f'{folder}{archivo_salida}', index=False, engine='openpyxl')