"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
from time import process_time 
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones y por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________





small_movies_details = "Data/SmallMoviesDetailsCleaned.csv"
small_movies_casting = "Data/MoviesCastingRaw-small.csv"
all_movies_details = "Data/AllMoviesDetailsCleaned.csv"
all_movies_casting = "Data/AllMoviesCastingRaw.csv"
# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def print_movies_information(movies):
    """
    imprime la información de las películas
    """
    print("Se cargaron " + str(lt.size(movies)) + " películas")
    primera=lt.firstElement(movies)
    print("\n")
    print(primera["original_title"])
    print(primera["release_date"])
    print(primera["vote_average"])
    print(primera["vote_count"])
    print(primera["original_language"])
    ultima=lt.lastElement(movies)
    print("\n")
    print(ultima["original_title"])
    print(ultima["release_date"])
    print(ultima["vote_average"])
    print(ultima["vote_count"])
    print(ultima["original_language"])
    print("\n")

def print_movies_country(info):
    print("Película\tDirector:")
    iterator=it.newIterator(info)
    while it.hasNext(iterator):
        movie = it.next(iterator)
        print(movie['nombre']+"\t"+movie['director'])


def print_companies_information(company):
    """
    imprime la información de una compañía de producción expecífica
    """
    print("Las películas producidas por esta compañía de producción son:\n")
    iterator=it.newIterator(company["movies"])
    while it.hasNext(iterator):
        movie=it.next(iterator)
        print(movie["original_title"])
    print("\nEl total de películas producidas es: "+str(lt.size(company["movies"])))
    print("El promedio de la calificación de las películas es: "+str(company["average_rating"]))

def print_genre_information(genre):
    """
    imprime la información de un género específico
    """
    print("Las películas de este género son:\n")
    iterator = it.newIterator(genre['movies'])
    while it.hasNext(iterator):
        movie = it.next(iterator)
        print(movie['original_title'])
    print("\nEl total de películas de este género es: "+str(lt.size(genre['movies'])))
    print("El número de votos promedio para este género es: "+str(genre['vote_count']))
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def print_menu():
    print("Bienvenido")
    print("1. Inicializar catálogo de películas")
    print("2. Cargar e imprimir detalles de películas")
    print("3. Descubrir productoras de cine")
    print("4. Cargar casting de películas")
    print("6. Descubrir un genero")
    print("7. Encontrar películas por país")
    print("0. Salir")

"""
Menú principal
"""
while True:
    print_menu()
    inputs = input("Seleccione una opción para continuar\n")

    if int(inputs[0]) == 1:
        print("Inicizaliando catálogo...")
        catalogo=controller.initCatalog()
        print("Completado")

    elif int(inputs[0]) == 2:
        print("Cargando archivos...")
        t_start = process_time()
        controller.loadMovies(catalogo,all_movies_details)
        t_stop = process_time()
        movies=catalogo['peliculas']
        print("Archivos cargados")
        print("El tiempo de carga es de "+str(t_stop-t_start)+" segundos")
        print(catalogo["productoras"]['type'])
        #print_movies_information(movies)
        

    elif int(inputs[0]) == 3:
        productora=input("Inserte una productora: ")
        t_start = process_time()
        productora_value=controller.getMoviesbyCompany(catalogo,productora.lower())
        t_stop = process_time()
        if productora_value is not None:
            print_companies_information(productora_value)
            print("El tiempo de consulta es de "+str(t_stop-t_start)+" segundos\n")
        else:
            print("No se encontró la productora")

    elif int(inputs[0]) == 4:
        t_start = process_time()
        controller.loadCasting(catalogo,all_movies_casting,sep=";")
        t_stop = process_time()
        print("Este proceso tomó "+str(t_stop-t_start)+" segundos")
        print("El número de actores es "+str(catalogo["actores"]["size"])) 

    elif int(inputs[0]) == 6:
        genre=input("Inserte un género (en inglés): ")
        t_start = process_time()
        genre_value=controller.getMoviesbyGenre(catalogo,genre.lower())
        t_stop = process_time()
        if genre_value is not None:
            print_genre_information(genre_value)
            print("El tiempo de consulta es de "+str(t_stop-t_start)+" segundos\n")
        else:
            print("No se encontró el género")

    elif int(inputs[0]) == 7:
        country=input("Inserte un país (en inglés): ")
        t_start = process_time()
        country_value=controller.getMoviesbyCountry(catalogo,country.lower())
        t_stop = process_time()
        if country_value is not None:
            #print_country_information(country_value)
            print_movies_country(country_value['movies'])
            print("El tiempo de consulta es de "+str(t_stop-t_start)+" segundos\n")
        else:
            print("No se encontró el país")
    
    else:
        sys.exit(0)
sys.exit(0)