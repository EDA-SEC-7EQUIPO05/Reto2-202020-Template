  
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
    catalogo = {'peliculas': None, 'productoras': None, "actores": None, 'generos': None, 'paises':None}  
    catalogo['peliculas'] = mp.newMap(numelements=349100,maptype='CHAINING', loadfactor=2, comparefunction=compareMovieId)
    catalogo['productoras'] = mp.newMap(numelements=36000,maptype='CHAINING', loadfactor=2, comparefunction=compareProductionCompanybyName)
    catalogo['actores'] = mp.newMap(numelements=261000,maptype='CHAINING', loadfactor=2, comparefunction=compareActorbyName)
    catalogo['generos'] = mp.newMap(numelements=50, maptype='PROBING',loadfactor=0.5, comparefunction=compareGenresbyName)
    catalogo['paises'] = mp.newMap(numelements=500,maptype='PROBING', loadfactor=0.5, comparefunction=compareCountriesbyName)
    return catalogo

def newProductionCompany(nombre):
    company = {'name': '', 'movies': None, 'average_rating': 0.0}
    company['name'] = nombre
    company['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompanybyName)
    return company

def newActor(nombre):
    actor = {"name": "", "movies": None, 'average_rating': 0.0, 'directores': None}
    actor["name"] = nombre
    actor["movies"] = lt.newList('SINGLE_LINKED', compareMovieId)
    actor['directores'] = mp.newMap(numelements=1000,maptype='CHAINING', loadfactor=2, comparefunction=compareDirectorByname)
    return actor

def newGenre(genero):
    genre = {'genre': '', 'movies': None, 'vote_count': 0.0}
    genre['genre'] = genero
    genre['movies'] = lt.newList('SINGLE_LINKED', compareGenresbyName)
    return genre

def newCountry(pais):
    country = {'name': '', 'movies': None}
    country['name'] = pais
    country['movies'] = lt.newList('SINGLE_LINKED', compareCountriesbyName)
    return country

# Funciones para agregar informacion al catalogo

def addMovie(catalogo, pelicula):
    mp.put(catalogo["peliculas"], pelicula["id"], pelicula)

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

def addActor(catalogo, actor, movie, casting):
    actores = catalogo["actores"]
    esta = mp.contains(actores, actor)
    if esta:
        entry = mp.get(actores, actor)
        act = me.getValue(entry)
    else:
        act = newActor(actor)
        mp.put(actores, actor, act)
    lt.addLast(act["movies"],movie)
    prom_act = act['average_rating']
    num_mov = lt.size(act['movies'])
    rat_peli = movie['vote_average']
    new_prom = round(((num_mov-1)*prom_act+float(rat_peli))/(num_mov), 2)
    act['average_rating'] = new_prom
    director = casting["director_name"]
    if mp.contains(act['directores'], director):
        direct = mp.get(act["directores"], director)
        valor = me.getValue(direct)
        valor+=1
        mp.put(act["directores"], director, valor)
    else:
        valor = 0
        mp.put(act["directores"], director, valor)
        direct = mp.get(act["directores"], director)
        valor = me.getValue(direct)
        valor+=1
        mp.put(act["directores"], director, valor)
    

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

def addCountryMovie(catalogo, ids, director):
    countries = catalogo['paises']
    movie = me.getValue(mp.get(catalogo['peliculas'], ids))
    nombre_pais = movie['production_countries'].lower()
    esta = mp.contains(countries, nombre_pais)
    if esta:
        entry = mp.get(countries, nombre_pais)
        country = me.getValue(entry)
    else:
        country = newCountry(nombre_pais)
        mp.put(countries, nombre_pais, country)
    info = {'nombre': movie['original_title'], 'director': director}
    lt.addLast(country['movies'], info)


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

def getActor_information(catalogo, actor_name):
    actor_entry = mp.get(catalogo["actores"], actor_name)
    if actor_entry is not None:
        return me.getValue(actor_entry)
    return None

def getMoviesbyGenre(catalogo, genre):
    gen = mp.get(catalogo['generos'], genre)
    if gen is not None:
        return me.getValue(gen)
    return None

def getMoviesbyCountry(catalogo, country):
    coun = mp.get(catalogo['paises'], country)
    if coun is not None:
        return me.getValue(coun)
    return None

# ==============================
# Funciones de Comparacion
# ==============================    

    

def compareMovieId(id_1, id_2):
    entryname = me.getKey(id_2)
    if id_1 == entryname:
        return 0
    elif id_1 > entryname:
        return 1
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

def compareDirectorByname(name, director):
    entryname = me.getKey(director)
    if name == entryname:
        return 0
    elif name > entryname:
        return 1
    else:
        return -1

def compareActorbyName(name, actor):
    entryname = me.getKey(actor)
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

def compareCountriesbyName(country_name, country_element):
    entry_name = me.getKey(country_element)
    if country_name == entry_name:
        return 0
    elif country_name > entry_name:
        return 1
    else:
        return -1