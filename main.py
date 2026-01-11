import os
import requests
import pandas as pd
from textblob import TextBlob
from dotenv import load_dotenv

# 1. Configuración inicial
load_dotenv()
api_key = os.getenv('NEWS_API_KEY')

def obtener_datos(tema):
    url = f'https://newsapi.org/v2/everything?q={tema}&language=es&apiKey={api_key}'
    response = requests.get(url)
    return response.json().get('articles', [])

def procesar_con_filtros(articulos, filtro_sentimiento=0):
    lista_procesada = [] 
    for art in articulos:
        texto = art['title']
        polaridad = TextBlob(texto).sentiment.polarity
        
        if polaridad >= filtro_sentimiento:
            # Todo esto debe llevar 3 niveles de tabulación (12 espacios)
            lista_procesada.append({
                'titulo': texto,
                'sentimiento': round(polaridad, 2),
                'fuente': art['source']['name']
            })
    return pd.DataFrame(lista_procesada)

# 2. Ejecución del programa
if __name__ == "__main__":
    tema = input("¿Qué tema quieres investigar? ")
    min_sentimiento = float(input("Filtro de sentimiento (de -1 a 1, ej. 0.1 para solo positivas): "))

    noticias_crudas = obtener_datos(tema)
    
    if noticias_crudas:
        df_final = procesar_con_filtros(noticias_crudas, min_sentimiento)
        print("\n--- Resultados Encontrados ---")
        print(df_final.head())
    else:
        print("No se encontraron noticias. Revisa tu API Key o el tema.")