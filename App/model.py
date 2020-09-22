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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newCatalog():
    catalogo = {'peliculas': None,
                'productoras': None,
                'generos': None}  
    catalogo['peliculas'] = lt.newList('ARRAY_LIST', compareMovieId)
    catalogo['productoras'] = mp.newMap(numelements=36000,maptype='CHAINING', loadfactor=2, comparefunction=compareProductionCompanybyName)
    catalogo['generos'] = mp.newMap(numelements=50, maptype='PROBING',loadfactor=0.5, comparefunction=compareGenresbyName)
    return catalogo

def newProductionCompany(nombre):
    company = {'name': '', 'movies': None, 'average_rating': 0.0}
    company['name'] = nombre
    company['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompanybyName)
    return company

def newGenre(genero):
    genre = {'genre': '', 'movies': None, 'vote_count': 0.0}
    genre['genre'] = genero
    genre['movies'] = lt.newList('SINGLE_LINKED', compareGenresbyName)
    return genre



# Funciones para agregar informacion al catalogo

def addMovie(catalogo, pelicula):
    lt.addLast(catalogo['peliculas'], pelicula)

def addCompanyMovie(catalogo, companyname, movie):
    companies = catalogo['productoras']
    esta = mp.contains(companies, companyname)
    if esta:
        entry = mp.get(companies, companyname)
        comp = me.getValue(entry)
    else:
        comp = newProductionCompany(companyname)
        mp.put(companies, companyname, comp)
    lt.addLast(comp['movies'], movie)
    rat_comp = comp['average_rating']
    num_mov = lt.size(comp['movies'])
    rat_peli = movie['vote_average']
    new_ave = round(((num_mov-1)*rat_comp+float(rat_peli))/(num_mov), 2)
    comp['average_rating'] = new_ave

def addGenreMovie(catalogo, nombre_genero, movie):
    genres = catalogo['generos']
    esta = mp.contains(genres, nombre_genero)
    if esta:
        entry = mp.get(genres, nombre_genero)
        genre = me.getValue(entry)
    else:
        genre = newGenre(nombre_genero)
        mp.put(genres, nombre_genero, genre)
    lt.addLast(genre['movies'], movie)
    count_genre = genre['vote_count']
    size_genre = lt.size(genre['movies'])
    count_movie = movie['vote_count']
    new_count = round(((size_genre-1)*count_genre+float(count_movie))/(size_genre), 2)
    genre['vote_count'] = new_count



# ==============================
# Funciones de consulta
# ==============================

def moviesSize(catalogo):
    return lt.size(catalogo["peliculas"])

def companiesSize(catalogo):
    return mp.size(catalogo['productoras'])

def genresSize(catalogo):
    return mp.size(catalogo['generos'])

def getMoviesbyCompany(catalogo, company_name):
    comp = mp.get(catalogo["productoras"], company_name)
    if comp is not None:
        return me.getValue(comp)
    return None

def getMoviesbyGenre(catalogo, genre):
    gen = mp.get(catalogo['generos'], genre)
    if gen is not None:
        return me.getValue(gen)
    return None

# ==============================
# Funciones de Comparacion
# ==============================

def compareMovieId(id_1, id_2):
    if id_1 > id_2:
        return 1
    elif id_1 == id_2:
        return 0
    else:
        return -1

def compareProductionCompanybyName(name, company):
    entryname = me.getKey(company)
    if name == entryname:
        return 0
    elif name > entryname:
        return 1
    else:
        return -1

def compareGenresbyName(genre_name, genre_element):
    entry_name = me.getKey(genre_element)
    if genre_name == entry_name:
        return 0
    elif genre_name > entry_name:
        return 1
    else:
        return -1