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

def print_directors_information(director):
    
    lista=[]

    iterator=it.newIterator(director["movies"])
    while it.hasNext(iterator):
        movie=it.next(iterator)
        id=movie.get("id")
        lista.append(id)
    print(director["movies"])
    return lista

    
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def print_menu():
    print("Bienvenido")
    print("1. Inicializar catálogo de películas")
    print("2. Cargar e imprimir detalles de películas")
    print("3. Descubrir productoras de cine")
    print("4. Descubrir directores de cine")
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
        controller.loadCasting(catalogo,small_movies_casting)
        controller.loadDetails(catalogo,small_movies_details)
        movies=catalogo['peliculas']
        print("Los archivos cargados fueron un total de: ",controller.moviesSize(catalogo,small_movies_casting,small_movies_details))
        

    elif int(inputs[0]) == 3:
        productora=input("Inserte una productora: ")
        productora_value=controller.getMoviesbyCompany(catalogo,productora)
        if productora_value is not None:
            print_companies_information(productora_value)
        else:
            print("No se encontró la productora")

    elif int(inputs[0]) == 4:
        director=input("Inserte el nombre de un director: ")
        director_value=controller.getDirectors(catalogo,director)
        if director_value is not None:
            print_directors_information(director_value)
        else:
            print("No se encontró el director")
    else:
        sys.exit(0)
sys.exit(0)
