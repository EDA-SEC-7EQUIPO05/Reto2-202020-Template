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
samll_movies_casting = "Data/MoviesCastingRaw-small.csv"
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


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def print_menu():
    print("Bienvenido")
    print("1. Inicializar catálogo de películas")
    print("2. Cargar e imprimir detalles de películas")
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
        controller.loadMovies(catalogo,small_movies_details)
        movies=catalogo['peliculas']
        print("Archivos cargados")
        print_movies_information(movies)
    
    else:
        sys.exit(0)
sys.exit(0)