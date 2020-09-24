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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me


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

def print_movies_information(catalogo):
    """
    imprime la información de las películas
    """
    movies = catalogo["peliculas"]
    productoras = catalogo["productoras"]
    actores = catalogo["actores"]
    print("Se cargaron " + str(movies["size"]) + " películas")
    print("Se cargaron " + str(productoras["size"]) + " productoras")
    print("El número de actores es "+str(actores["size"]))
    


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

def print_actor_information(actor):
    """
    Imprime la información de un actor
    """
    print("Las películas en las que participó este actor son:\n")
    iterator = it.newIterator(actor["movies"])
    while it.hasNext(iterator):
        movie = it.next(iterator)
        print(movie["original_title"])
    print("\nEl total de películas en las que participó es: "+str(lt.size(actor["movies"])))
    print("\nEl promedio de la calificación de las películas es: "+str(actor["average_rating"]))
    keys = mp.keySet(actor["directores"])
    valores = mp.valueSet(actor["directores"])
    iterator_keys = it.newIterator(keys)
    iterator_values = it.newIterator(valores)
    lista = []
    while it.hasNext(iterator_keys) and it.hasNext(iterator_values):
        key = it.next(iterator_keys)
        value = it.next(iterator_values)
        lista.append([value,key])
    lista.sort()
    director = lista[-1][1]
    numero = lista[-1][0]
    print ("\nEl director con el que éste actor ha hecho más colaboraciones es "+director+", con un total de "+str(numero))

def print_directors_information(director):
    
    print("Las películas producidas por esta compañía de producción son:\n")
    iterator=it.newIterator(director["movies"])
    while it.hasNext(iterator):
        movie=it.next(iterator)
        print(movie["original_title"])
    print("\nEl total de películas producidas es: "+str(lt.size(director["movies"])))
    print("El promedio de la calificación de las películas es: "+str(director["average_rating"]))

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def print_menu():
    print("\nBienvenido")
    print("1. Inicializar catálogo de películas")
    print("2. Cargar detalles y castings de películas")
    print("3. Descubrir directores de cine")
    print("4. Descubrir productoras de cine")
    print("5. Descubrir actor")
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
        controller.loadMovies (catalogo,small_movies_details,small_movies_casting)
        t_stop = process_time()
        print("Archivos cargados")
        print("El tiempo de carga total es de "+str(t_stop-t_start)+" segundos")
        print("Peliculas guardadas en map de tipo "+catalogo["peliculas"]['type'])
        print("productoras guardadas en map de tipo "+catalogo["productoras"]['type'])
        print("Actores guardados en map de tipo "+catalogo["actores"]['type'])
        print_movies_information(catalogo)
        
    elif int(inputs[0]) == 3:
        director=input("Inserte un director: ")
        t_start = process_time()
        director_value=controller.getDirectors(catalogo,director.lower())
        t_stop = process_time()
        if director_value is not None:
            print_directors_information(director_value)
            print("El tiempo de consulta es de "+str(t_stop-t_start)+" segundos\n")
        else:
            print("No se encontró el director")

    elif int(inputs[0]) == 4:
        productora=input("Inserte una productora: ")
        t_start = process_time()
        productora_value=controller.getMoviesbyCompany(catalogo,productora.lower())
        t_stop = process_time()
        if productora_value is not None:
            print_companies_information(productora_value)
            print("El tiempo de consulta es de "+str(t_stop-t_start)+" segundos\n")
        else:
            print("No se encontró la productora")

    elif int(inputs[0]) == 5:
        actor_name = input("Ingrese el nombre de un actor: ")
        actor = controller.getActor_information(catalogo, actor_name.lower())
        if actor is not None:
            t_start = process_time()
            print_actor_information(actor)
            t_stop = process_time()
            print("Este proceso tomó "+str(t_stop-t_start)+" segundos")
    else:
        sys.exit(0)
sys.exit(0) 